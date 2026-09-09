#!/usr/bin/env python3
"""Audit the generated site against the quality-first AdSense recovery policy."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
import sys
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DOMAIN = "septicscope.com"
BASE = f"https://{DOMAIN}"
ADSENSE_CLIENT = "ca-pub-8782868222380999"
EDITORIAL_MARKER = 'data-septicscope-editorial-note="1"'


@dataclass
class Page:
    path: Path
    text_parts: list[str] = field(default_factory=list)
    links: list[tuple[str, str]] = field(default_factory=list)
    title: str = ""
    robots: str = ""
    canonical: str = ""
    h1: str = ""
    _capture: str | None = None
    _buffer: list[str] = field(default_factory=list)
    _anchor_href: str | None = None
    _anchor_text: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return " ".join(self.text_parts)

    @property
    def words(self) -> int:
        return len(re.findall(r"\b[\w'-]+\b", self.text))


class Parser(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.page = Page(path)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        tag = tag.lower()
        if tag in {"title", "h1"}:
            self.page._capture = tag
            self.page._buffer = []
        elif tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.page.robots = attrs.get("content", "").lower().strip()
        elif tag == "link" and "canonical" in attrs.get("rel", "").lower():
            self.page.canonical = attrs.get("href", "").strip()
        elif tag == "a" and attrs.get("href"):
            self.page._anchor_href = attrs["href"].strip()
            self.page._anchor_text = []

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.page._capture == tag:
            value = " ".join(self.page._buffer).strip()
            if tag == "title":
                self.page.title = value
            elif tag == "h1":
                self.page.h1 = value
            self.page._capture = None
            self.page._buffer = []
        if tag == "a" and self.page._anchor_href is not None:
            label = " ".join(self.page._anchor_text).strip()
            self.page.links.append((self.page._anchor_href, label))
            self.page._anchor_href = None
            self.page._anchor_text = []

    def handle_data(self, data):
        value = data.strip()
        if value:
            self.page.text_parts.append(value)
        if self.page._capture:
            self.page._buffer.append(data)
        if self.page._anchor_href is not None:
            self.page._anchor_text.append(data)


def parse(path: Path) -> Page:
    parser = Parser(path)
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser.page


def has_adsense(raw: str) -> bool:
    return ADSENSE_CLIENT in raw or "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" in raw


def is_noindex(page: Page) -> bool:
    return "noindex" in page.robots


def is_county_leaf(path: Path) -> bool:
    parts = path.relative_to(SITE).parts
    return len(parts) == 4 and parts[0] == "counties" and parts[-1] == "index.html"


def is_guide_article(path: Path) -> bool:
    parts = path.relative_to(SITE).parts
    return len(parts) == 3 and parts[0] == "guides" and parts[-1] == "index.html"


def monetization_allowed(path: Path, page: Page) -> bool:
    if is_noindex(page) or page.words < 500:
        return False
    parts = path.relative_to(SITE).parts
    return parts == ("index.html",) or is_guide_article(path)


def is_external(href: str) -> bool:
    parsed = urlparse(href)
    host = (parsed.hostname or "").lower()
    return parsed.scheme in {"http", "https"} and host not in {DOMAIN, "www." + DOMAIN}


def page_url(path: Path) -> str:
    relative = path.relative_to(SITE).as_posix()
    if relative == "index.html":
        return BASE + "/"
    if relative.endswith("/index.html"):
        return BASE + "/" + relative[:-10]
    return BASE + "/" + relative


def normalized_county_fingerprint(page: Page) -> str:
    text = page.text.lower()
    text = re.sub(r"\b[a-z][a-z .'-]+ (?:county|parish|borough|city|census area)\b", " location ", text)
    text = re.sub(r"\b\d{3}[-.) ]\d{3}[- ]\d{4}\b", " phone ", text)
    text = re.sub(r"\b\d{1,6}\b", " number ", text)
    text = re.sub(r"\s+", " ", text)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    if not SITE.is_dir():
        print("ERROR: site directory is missing", file=sys.stderr)
        return 1

    html_files = sorted(SITE.rglob("*.html"))
    pages = {path: parse(path) for path in html_files}
    raw_pages = {path: path.read_text(encoding="utf-8", errors="replace") for path in html_files}

    manifest_path = SITE / "data" / "national-coverage-manifest.json"
    lookup_path = SITE / "data" / "county-lookup.json"
    readiness_path = SITE / "data" / "adsense-readiness.json"
    for required in (manifest_path, lookup_path, readiness_path):
        if not required.exists():
            errors.append(f"Missing AdSense recovery artifact: {required.relative_to(SITE)}")
    if errors:
        return _finish(errors, warnings, html_files, pages)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = [row for row in manifest.get("records", []) if isinstance(row, dict)]
    lookup = json.loads(lookup_path.read_text(encoding="utf-8"))
    lookup_rows = [row for row in lookup.get("counties", []) if isinstance(row, dict)]
    readiness = json.loads(readiness_path.read_text(encoding="utf-8"))

    if len(records) != 3144 or len({str(row.get("fips", "")) for row in records}) != 3144:
        errors.append("National manifest does not contain 3,144 unique county FIPS records")
    if lookup.get("record_count") != 3144 or len(lookup_rows) != 3144:
        errors.append("County lookup does not contain all 3,144 county-equivalents")
    if len({str(row.get("f", "")) for row in lookup_rows}) != 3144:
        errors.append("County lookup contains duplicate FIPS records")

    bad_lookup = []
    for row in lookup_rows:
        required = (row.get("f"), row.get("n"), row.get("s"), row.get("g"), row.get("e"))
        if not all(required):
            bad_lookup.append(str(row.get("f", "unknown")))
            continue
        if bool(row.get("v")) != bool(row.get("u")):
            bad_lookup.append(str(row.get("f", "unknown")))
    if bad_lookup:
        errors.append(f"County lookup publication fields are inconsistent: {bad_lookup[:12]}")

    manifest_verified = {
        str(row.get("page_url", ""))
        for row in records
        if row.get("verification_status") == "verified"
    }
    county_pages = [path for path in html_files if is_county_leaf(path)]
    county_urls = {page_url(path) for path in county_pages}
    if county_urls != manifest_verified:
        missing = sorted(manifest_verified - county_urls)
        extra = sorted(county_urls - manifest_verified)
        errors.append(
            f"Published county pages do not match verified manifest records; "
            f"missing={missing[:6]}, extra={extra[:6]}"
        )
    if int(readiness.get("placeholder_county_pages", -1)) != 0:
        errors.append("AdSense readiness report still lists placeholder county pages")
    if int(readiness.get("county_lookup_records", 0)) != 3144:
        errors.append("AdSense readiness report lost national county lookup coverage")

    exempt_construction_routes = {
        SITE / "providers" / "index.html",
        SITE / "septic-services-near-me" / "index.html",
    }
    forbidden_phrases = (
        "local guide in progress",
        "while we finish this local guide",
        "official-help pages still under research",
        "all 3,144 county pages",
    )

    monetized_pages = []
    ad_free_pages = []
    for path, page in pages.items():
        raw = raw_pages[path]
        ads = has_adsense(raw)
        allowed = monetization_allowed(path, page)
        if ads:
            monetized_pages.append(path)
            if not allowed:
                errors.append(f"AdSense code appears on a utility, thin, county or noindex page: /{path.relative_to(SITE)}")
        else:
            ad_free_pages.append(path)
        if allowed and path == SITE / "index.html" and not ads:
            errors.append("Homepage is missing the AdSense site code")
        if path not in exempt_construction_routes:
            lower = raw.lower()
            for phrase in forbidden_phrases:
                if phrase in lower:
                    errors.append(f"Construction/filler language remains on /{path.relative_to(SITE)}: {phrase}")
        if is_noindex(page) and ads:
            errors.append(f"Noindex page contains AdSense code: /{path.relative_to(SITE)}")

    if not monetized_pages:
        errors.append("No substantive page carries the AdSense site code")
    monetized_guides = [path for path in monetized_pages if is_guide_article(path)]
    if len(monetized_guides) < 5:
        warnings.append(
            f"Only {len(monetized_guides)} long-form guide pages currently meet the 500-word monetization threshold"
        )

    fingerprints = Counter()
    for path in county_pages:
        page = pages[path]
        raw = raw_pages[path]
        rel = "/" + path.relative_to(SITE).as_posix()
        external = [(href, label) for href, label in page.links if is_external(href)]
        if is_noindex(page):
            errors.append(f"Published county page is noindex: {rel}")
        if page.words < 180:
            errors.append(f"Published county page is too thin ({page.words} words): {rel}")
        if "Official sources" not in page.text:
            errors.append(f"Published county page lacks an Official sources section: {rel}")
        if "Permitting authority" not in page.text:
            errors.append(f"Published county page lacks a permitting authority: {rel}")
        if "Report outdated county information" not in page.text or 'href="/contact/"' not in raw:
            errors.append(f"Published county page lacks a visible correction route: {rel}")
        if EDITORIAL_MARKER not in raw:
            errors.append(f"Published county page lacks publisher/editorial disclosure: {rel}")
        if len(external) < 2:
            errors.append(f"Published county page has fewer than two external source links: {rel}")
        if has_adsense(raw):
            errors.append(f"County guide carries AdSense code during recovery review: {rel}")
        fingerprints[normalized_county_fingerprint(page)] += 1

    repeated = sorted((count, fp) for fp, count in fingerprints.items() if count >= 5)
    if repeated:
        largest = repeated[-1][0]
        warnings.append(
            f"Repeated county-content fingerprint detected across as many as {largest} published pages; "
            "continue replacing statewide templates with local office, form, records and process details"
        )
        if largest >= 30:
            errors.append(f"A county template is repeated across {largest} published pages")

    about = SITE / "about" / "index.html"
    if not about.exists():
        errors.append("About/editorial standards page is missing")
    else:
        page = pages[about]
        raw = raw_pages[about]
        if page.words < 900:
            errors.append(f"About/editorial standards page is too thin ({page.words} words)")
        for phrase in (
            "SepticScope Editorial Desk",
            "What “source-verified county guide” means",
            "How automation and AI are used",
            "Advertising and editorial independence",
            "Corrections, updates and limitations",
        ):
            if phrase not in raw:
                errors.append(f"About page is missing required disclosure: {phrase}")
        if has_adsense(raw):
            errors.append("About/editorial standards page must remain ad-free")

    privacy = SITE / "privacy" / "index.html"
    if not privacy.exists():
        errors.append("Privacy policy is missing")
    else:
        raw = raw_pages[privacy]
        lower = raw.lower()
        for phrase in (
            "third-party vendors, including google",
            "google ads settings",
            "optional location lookup",
            "does not store the coordinates",
            "google analytics",
            "google adsense",
        ):
            if phrase not in lower:
                errors.append(f"Privacy policy is missing disclosure: {phrase}")
        if has_adsense(raw):
            errors.append("Privacy policy must remain ad-free")

    contact = SITE / "contact" / "index.html"
    if not contact.exists():
        errors.append("Contact and feedback page is missing")
    else:
        raw = raw_pages[contact]
        if "feedback-form" not in raw or "mailto:feedback@septicscope.com" not in raw:
            errors.append("Contact page lacks the public correction route")
        if has_adsense(raw):
            errors.append("Contact page must remain ad-free")

    records_guide = SITE / "guides" / "find-septic-system-records" / "index.html"
    if not records_guide.exists() or pages.get(records_guide, Page(records_guide)).words < 900:
        errors.append("Substantive septic system records guide is missing or too thin")

    sitemap = SITE / "sitemap.xml"
    sitemap_urls: set[str] = set()
    if not sitemap.exists():
        errors.append("sitemap.xml is missing")
    else:
        try:
            root = ET.parse(sitemap).getroot()
            ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            sitemap_urls = {(node.text or "").strip() for node in root.findall(".//s:loc", ns)}
        except Exception as exc:
            errors.append(f"sitemap.xml could not be parsed: {exc}")
        expected_urls = {
            page_url(path)
            for path, page in pages.items()
            if path.name != "404.html"
            and not is_noindex(page)
            and page_url(path) not in {BASE + "/providers/", BASE + "/septic-services-near-me/"}
        }
        if sitemap_urls != expected_urls:
            missing = sorted(expected_urls - sitemap_urls)
            extra = sorted(sitemap_urls - expected_urls)
            errors.append(f"Sitemap publication mismatch; missing={missing[:8]}, extra={extra[:8]}")

    ads = SITE / "ads.txt"
    expected_ads = "google.com, pub-8782868222380999, DIRECT, f08c47fec0942fa0"
    if not ads.exists() or expected_ads not in ads.read_text(encoding="utf-8", errors="replace"):
        errors.append("ads.txt is missing the authorized Google publisher record")

    print("SepticScope AdSense low-value recovery audit")
    print(f"HTML pages: {len(html_files):,}")
    print(f"County lookup records: {len(lookup_rows):,}")
    print(f"Published source-verified county guides: {len(county_pages):,}")
    print(f"Unpublished lookup-only counties: {len(records) - len(county_pages):,}")
    print(f"AdSense-enabled substantive pages: {len(monetized_pages):,}")
    print(f"Ad-free pages: {len(ad_free_pages):,}")
    print(f"Sitemap URLs: {len(sitemap_urls):,}")
    return _finish(errors, warnings, html_files, pages)


def _finish(errors: list[str], warnings: list[str], html_files, pages) -> int:
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(" -", warning)
    if errors:
        print(f"ERRORS ({len(errors)}):", file=sys.stderr)
        for error in errors[:300]:
            print(" -", error, file=sys.stderr)
        if len(errors) > 300:
            print(f" - ... {len(errors) - 300} more", file=sys.stderr)
        return 1
    print("PASS: low-value placeholders are unpublished and AdSense is limited to substantive content")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
