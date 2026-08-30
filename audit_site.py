#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SITE = ROOT / 'site'
DOMAIN = 'septicscope.com'
BASE = f'https://{DOMAIN}'


@dataclass
class PageInfo:
    path: Path
    hrefs: list[str] = field(default_factory=list)
    canonicals: list[str] = field(default_factory=list)
    title: str = ''
    description: str = ''
    robots: str = ''
    text_parts: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return ' '.join(self.text_parts)


class Inspector(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.info = PageInfo(path)
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('href'):
            self.info.hrefs.append(attrs['href'].strip())
        elif tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split() and attrs.get('href'):
            self.info.canonicals.append(attrs['href'].strip())
        elif tag == 'meta':
            name = attrs.get('name', '').lower()
            if name == 'description':
                self.info.description = attrs.get('content', '').strip()
            elif name == 'robots':
                self.info.robots = attrs.get('content', '').lower().strip()
        elif tag == 'title':
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False

    def handle_data(self, data):
        value = data.strip()
        if value:
            self.info.text_parts.append(value)
            if self._in_title:
                self.info.title += value


def parse_page(path: Path) -> PageInfo:
    parser = Inspector(path)
    parser.feed(path.read_text(encoding='utf-8', errors='replace'))
    return parser.info


def url_path_to_file(url_path: str) -> Path | None:
    path = urllib.parse.unquote(url_path.split('?', 1)[0].split('#', 1)[0])
    if not path.startswith('/'):
        path = '/' + path
    rel = path.lstrip('/')
    candidates = []
    if not rel:
        candidates = [SITE / 'index.html']
    else:
        direct = SITE / rel
        candidates.extend([direct, direct / 'index.html'])
        if not Path(rel).suffix:
            candidates.append(SITE / f'{rel}.html')
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def internal_path(href: str, source_url_path: str) -> str | None:
    if not href or href.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
        return None
    parsed = urllib.parse.urlparse(href)
    if parsed.scheme in ('http', 'https'):
        if parsed.netloc.lower().split(':')[0] not in (DOMAIN, 'www.' + DOMAIN):
            return None
        return parsed.path or '/'
    if parsed.scheme or parsed.netloc:
        return None
    if href.startswith('/'):
        return parsed.path or '/'
    base = urllib.parse.urljoin(BASE + source_url_path, href)
    return urllib.parse.urlparse(base).path or '/'


def page_url_path(path: Path) -> str:
    rel = path.relative_to(SITE).as_posix()
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-10]
    return '/' + rel


def check_external(url: str) -> tuple[str, str, int | None]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; SepticScopeLinkAudit/1.0; +https://septicscope.com/)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Range': 'bytes=0-1024',
    }
    req = urllib.request.Request(url, headers=headers, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=18) as resp:
            resp.read(1)
            return url, 'ok', getattr(resp, 'status', 200)
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403, 406, 429):
            return url, 'blocked', exc.code
        if exc.code in (404, 410):
            return url, 'broken', exc.code
        return url, 'warning', exc.code
    except Exception:
        return url, 'warning', None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--external', action='store_true', help='Check unique external anchor URLs over HTTP')
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    html_files = sorted(SITE.rglob('*.html'))
    if not html_files:
        print('ERROR: no generated HTML files found', file=sys.stderr)
        return 1

    pages = {p: parse_page(p) for p in html_files}
    internal_links = 0
    external_urls: set[str] = set()
    canonical_to_page: dict[str, Path] = {}
    lookup_pages = 0
    verified_county_pages = 0

    for path, info in pages.items():
        src_path = page_url_path(path)
        is_404 = path.name == '404.html'
        is_lookup = 'Local guide in progress' in info.text
        is_county_leaf = len(path.relative_to(SITE).parts) == 4 and path.relative_to(SITE).parts[0] == 'counties' and path.name == 'index.html'
        if is_lookup:
            lookup_pages += 1
        elif is_county_leaf:
            verified_county_pages += 1

        if not info.title and not is_404:
            errors.append(f'Missing title: {src_path}')
        if not info.description and not is_404:
            warnings.append(f'Missing meta description: {src_path}')

        if not is_404:
            if len(info.canonicals) != 1:
                errors.append(f'Expected one canonical, found {len(info.canonicals)}: {src_path}')
            else:
                canonical = info.canonicals[0]
                if not canonical.startswith(BASE + '/') and canonical != BASE:
                    errors.append(f'Non-production canonical: {src_path} -> {canonical}')
                other = canonical_to_page.get(canonical)
                if other and other != path:
                    errors.append(f'Duplicate canonical: {canonical} on {other} and {path}')
                canonical_to_page[canonical] = path

        raw = path.read_text(encoding='utf-8', errors='replace')
        if 'septicscope.pages.dev' in raw:
            errors.append(f'pages.dev reference remains in HTML: {src_path}')

        if is_lookup:
            robots = info.robots.replace(' ', '')
            if 'noindex' not in robots or 'follow' not in robots:
                errors.append(f'Lookup page missing noindex,follow: {src_path}')
            if 'Do not rely on this page' in info.text or 'not yet verified' in info.text.lower():
                errors.append(f'Unwelcoming legacy lookup wording remains: {src_path}')
            if 'usa.gov/states/' not in raw or 'epa.gov/septic/state-septic-system-program-contacts' not in raw:
                errors.append(f'Lookup page missing official help links: {src_path}')
        elif is_county_leaf:
            if 'noindex' in info.robots:
                errors.append(f'Verified county page is noindex: {src_path}')
            if 'Official sources' not in info.text:
                errors.append(f'Verified county page missing Official sources section: {src_path}')

        for href in info.hrefs:
            parsed = urllib.parse.urlparse(href)
            if parsed.scheme in ('http', 'https') and parsed.netloc.lower().split(':')[0] not in (DOMAIN, 'www.' + DOMAIN):
                external_urls.add(href)
                continue
            target_path = internal_path(href, src_path)
            if target_path is None:
                continue
            internal_links += 1
            if url_path_to_file(target_path) is None:
                errors.append(f'Broken internal link: {src_path} -> {href}')

    # robots.txt and ads.txt essentials
    robots_path = SITE / 'robots.txt'
    if not robots_path.exists():
        errors.append('robots.txt missing')
    else:
        robots = robots_path.read_text(encoding='utf-8', errors='replace')
        if 'Disallow: /' in robots:
            errors.append('robots.txt blocks the whole site')
        if f'{BASE}/sitemap.xml' not in robots:
            errors.append('robots.txt does not reference production sitemap')

    ads_path = SITE / 'ads.txt'
    expected_ads = 'google.com, pub-8782868222380999, DIRECT, f08c47fec0942fa0'
    if not ads_path.exists() or expected_ads not in ads_path.read_text(encoding='utf-8', errors='replace'):
        errors.append('ads.txt missing or does not contain expected AdSense publisher record')

    # Sitemap integrity and noindex exclusion.
    sitemap_path = SITE / 'sitemap.xml'
    sitemap_urls: list[str] = []
    if not sitemap_path.exists():
        errors.append('sitemap.xml missing')
    else:
        try:
            root = ET.parse(sitemap_path).getroot()
            ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            sitemap_urls = [(n.text or '').strip() for n in root.findall('.//s:loc', ns)]
        except Exception as exc:
            errors.append(f'sitemap.xml cannot be parsed: {exc}')
        if len(sitemap_urls) != len(set(sitemap_urls)):
            errors.append('sitemap.xml contains duplicate URLs')
        for url in sitemap_urls:
            p = urllib.parse.urlparse(url)
            if p.netloc != DOMAIN:
                errors.append(f'Non-production sitemap URL: {url}')
                continue
            local = url_path_to_file(p.path or '/')
            if local is None:
                errors.append(f'Sitemap URL has no generated file: {url}')
                continue
            info = pages.get(local)
            if info and 'noindex' in info.robots:
                errors.append(f'Noindex page appears in sitemap: {url}')

    # Every indexable page with a canonical should be discoverable in the sitemap.
    sitemap_set = set(sitemap_urls)
    for canonical, page in canonical_to_page.items():
        info = pages[page]
        if 'noindex' in info.robots or page.name == '404.html':
            continue
        if canonical not in sitemap_set:
            errors.append(f'Indexable canonical missing from sitemap: {canonical}')

    print('SepticScope full-site audit')
    print(f'HTML pages: {len(html_files):,}')
    print(f'Internal links checked: {internal_links:,}')
    print(f'Verified county leaf pages: {verified_county_pages:,}')
    print(f'In-progress county help pages: {lookup_pages:,}')
    print(f'Sitemap URLs: {len(sitemap_urls):,}')
    print(f'Unique external anchor URLs: {len(external_urls):,}')

    if args.external and external_urls:
        print('Checking external source/help links...')
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=18) as pool:
            for result in pool.map(check_external, sorted(external_urls)):
                results.append(result)
        broken = [(u, code) for u, status, code in results if status == 'broken']
        blocked = [(u, code) for u, status, code in results if status == 'blocked']
        uncertain = [(u, code) for u, status, code in results if status == 'warning']
        print(f'External links OK: {sum(1 for _,s,_ in results if s == "ok"):,}')
        print(f'External links blocked/rate-limited but not proven broken: {len(blocked):,}')
        print(f'External links with transient/uncertain responses: {len(uncertain):,}')
        print(f'External links returning 404/410: {len(broken):,}')
        for url, code in broken:
            errors.append(f'External source link returns {code}: {url}')
        for url, code in blocked:
            warnings.append(f'External checker blocked ({code}): {url}')
        for url, code in uncertain:
            warnings.append(f'External link could not be conclusively checked ({code or "network"}): {url}')

    if warnings:
        print(f'WARNINGS ({len(warnings)}):')
        for warning in warnings[:100]:
            print(' -', warning)
        if len(warnings) > 100:
            print(f' - ... {len(warnings)-100} additional warnings')

    if errors:
        print(f'ERRORS ({len(errors)}):', file=sys.stderr)
        for error in errors:
            print(' -', error, file=sys.stderr)
        return 1

    print('PASS: no hard site-integrity errors found')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
