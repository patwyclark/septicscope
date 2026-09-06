#!/usr/bin/env python3
"""Audit SepticScope sitemap URLs for Google-indexing hygiene.

The static audit prevents noindex, redirected/non-canonical, or missing pages from
being published in the sitemap. The production audit checks the live sitemap and
verifies that every listed URL returns 200 without redirecting, is indexable, and
self-canonicalizes. This specifically targets Search Console exclusion classes
such as "Page with redirect" and "Excluded by noindex tag" without forcing
unfinished county-help pages to become indexable.
"""
from __future__ import annotations

import argparse
import concurrent.futures
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = "https://septicscope.com"
DOMAIN = "septicscope.com"


class HeadInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.canonicals: list[str] = []
        self.robots: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs = dict(attrs)
        if tag == "link" and "canonical" in str(attrs.get("rel", "")).lower().split():
            href = str(attrs.get("href", "")).strip()
            if href:
                self.canonicals.append(href)
        elif tag == "meta" and str(attrs.get("name", "")).lower() in {"robots", "googlebot"}:
            self.robots.append(str(attrs.get("content", "")).lower())


def parse_sitemap(xml_text: str) -> list[str]:
    root = ET.fromstring(xml_text)
    urls: list[str] = []
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1] == "loc":
            value = (node.text or "").strip()
            if value:
                urls.append(value)
    return urls


def normalize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    path = parsed.path or "/"
    if path != "/" and not Path(path).suffix and not path.endswith("/"):
        path += "/"
    return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, "", ""))


def local_file(site: Path, url: str) -> Path | None:
    parsed = urllib.parse.urlsplit(url)
    rel = urllib.parse.unquote(parsed.path).lstrip("/")
    if not rel:
        candidates = [site / "index.html"]
    else:
        direct = site / rel
        candidates = [direct]
        if not Path(rel).suffix:
            candidates.append(direct / "index.html")
        if Path(rel).suffix == ".html":
            candidates.append(site / rel)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def inspect_html(text: str) -> tuple[list[str], str]:
    parser = HeadInspector()
    parser.feed(text)
    robots = ",".join(parser.robots).replace(" ", "")
    return parser.canonicals, robots


def redirect_sources(site: Path) -> set[str]:
    path = site / "_redirects"
    if not path.exists():
        return set()
    sources: set[str] = set()
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        source = parts[0]
        if "*" in source or ":" in source:
            # Wildcard/parameter rules are checked by production HTTP behavior.
            continue
        if source.startswith("http://") or source.startswith("https://"):
            parsed = urllib.parse.urlsplit(source)
            if parsed.netloc.lower() == DOMAIN:
                sources.add(normalize_url(source))
        elif source.startswith("/"):
            sources.add(normalize_url(BASE + source))
    return sources


def audit_static(site: Path) -> list[str]:
    errors: list[str] = []
    sitemap = site / "sitemap.xml"
    if not sitemap.exists():
        return ["Generated sitemap.xml is missing"]
    try:
        urls = parse_sitemap(sitemap.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        return [f"Generated sitemap cannot be parsed: {exc}"]
    if not urls:
        errors.append("Generated sitemap contains no URLs")
        return errors
    if len(urls) != len(set(urls)):
        errors.append("Generated sitemap contains duplicate URLs")

    redirects = redirect_sources(site)
    for raw_url in urls:
        url = normalize_url(raw_url)
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc != DOMAIN:
            errors.append(f"Non-production URL in sitemap: {raw_url}")
            continue
        if url in redirects:
            errors.append(f"Redirect source appears in sitemap: {raw_url}")
        page = local_file(site, url)
        if page is None:
            errors.append(f"Sitemap URL has no generated file: {raw_url}")
            continue
        if page.suffix.lower() != ".html":
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        canonicals, robots = inspect_html(text)
        if "noindex" in robots:
            errors.append(f"Noindex page appears in sitemap: {raw_url}")
        if len(canonicals) != 1:
            errors.append(f"Sitemap page must have one canonical ({len(canonicals)} found): {raw_url}")
        elif normalize_url(canonicals[0]) != url:
            errors.append(f"Sitemap page does not self-canonicalize: {raw_url} -> {canonicals[0]}")
        if re.search(r"<meta[^>]+http-equiv=[\"']?refresh", text, flags=re.I):
            errors.append(f"Meta-refresh page appears in sitemap: {raw_url}")
    return errors


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


def fetch_without_redirect(url: str, *, limit: int = 131072) -> tuple[int, str, dict[str, str]]:
    opener = urllib.request.build_opener(NoRedirect)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; SepticScopeIndexAudit/1.0; +https://septicscope.com/)",
            "Cache-Control": "no-cache",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        method="GET",
    )
    try:
        with opener.open(request, timeout=20) as response:
            body = response.read(limit).decode("utf-8", errors="replace")
            headers = {k.lower(): v for k, v in response.headers.items()}
            return int(getattr(response, "status", 200)), body, headers
    except urllib.error.HTTPError as exc:
        body = exc.read(limit).decode("utf-8", errors="replace") if exc.fp else ""
        headers = {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {}
        return int(exc.code), body, headers


def audit_live_url(url: str) -> str | None:
    try:
        status, body, headers = fetch_without_redirect(url)
    except Exception as exc:
        return f"Live sitemap URL could not be checked: {url} ({type(exc).__name__})"
    if 300 <= status < 400:
        return f"Live sitemap URL redirects ({status}): {url} -> {headers.get('location', 'unknown')}"
    if status != 200:
        return f"Live sitemap URL does not return 200 ({status}): {url}"
    xrobots = headers.get("x-robots-tag", "").lower().replace(" ", "")
    if "noindex" in xrobots:
        return f"Live sitemap URL has X-Robots-Tag noindex: {url}"
    if "text/html" not in headers.get("content-type", "").lower():
        return None
    canonicals, robots = inspect_html(body)
    if "noindex" in robots:
        return f"Live sitemap URL has meta noindex: {url}"
    expected = normalize_url(url)
    if len(canonicals) != 1:
        return f"Live sitemap URL must have one canonical ({len(canonicals)} found): {url}"
    if normalize_url(canonicals[0]) != expected:
        return f"Live sitemap URL canonical mismatch: {url} -> {canonicals[0]}"
    return None


def audit_production() -> tuple[list[str], int]:
    errors: list[str] = []
    try:
        status, xml_text, _headers = fetch_without_redirect(BASE + "/sitemap.xml", limit=4_000_000)
    except Exception as exc:
        return [f"Live sitemap could not be fetched: {type(exc).__name__}: {exc}"], 0
    if status != 200:
        return [f"Live sitemap does not return 200: {status}"], 0
    try:
        urls = parse_sitemap(xml_text)
    except Exception as exc:
        return [f"Live sitemap cannot be parsed: {exc}"], 0
    if len(urls) != len(set(urls)):
        errors.append("Live sitemap contains duplicate URLs")
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        for result in pool.map(audit_live_url, urls):
            if result:
                errors.append(result)
    return errors, len(urls)


def self_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        site = Path(tmp)
        (site / "ok").mkdir()
        (site / "hidden").mkdir()
        (site / "ok" / "index.html").write_text(
            '<html><head><title>OK</title><meta name="robots" content="index,follow">'
            '<link rel="canonical" href="https://septicscope.com/ok/"></head><body>ok</body></html>',
            encoding="utf-8",
        )
        (site / "hidden" / "index.html").write_text(
            '<html><head><meta name="robots" content="noindex,follow">'
            '<link rel="canonical" href="https://septicscope.com/hidden/"></head></html>',
            encoding="utf-8",
        )
        (site / "sitemap.xml").write_text(
            '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            '<url><loc>https://septicscope.com/ok/</loc></url></urlset>',
            encoding="utf-8",
        )
        assert not audit_static(site)
        (site / "sitemap.xml").write_text(
            '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            '<url><loc>https://septicscope.com/hidden/</loc></url></urlset>',
            encoding="utf-8",
        )
        failures = audit_static(site)
        assert any("Noindex page appears in sitemap" in item for item in failures)
    print("PASS: indexing hygiene self-test")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("site"))
    parser.add_argument("--production", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.production:
        errors, count = audit_production()
        label = "live production sitemap"
    else:
        errors = audit_static(args.site)
        try:
            count = len(parse_sitemap((args.site / "sitemap.xml").read_text(encoding="utf-8", errors="replace")))
        except Exception:
            count = 0
        label = "generated sitemap"
    print(f"SepticScope indexing hygiene audit: {label}; URLs checked: {count:,}")
    if errors:
        print(f"ERRORS ({len(errors)}):", file=sys.stderr)
        for error in errors:
            print(" -", error, file=sys.stderr)
        return 1
    print("PASS: sitemap contains only direct, indexable, self-canonical URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
