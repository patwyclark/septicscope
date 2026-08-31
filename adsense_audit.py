#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DOMAIN = "septicscope.com"
BASE = f"https://{DOMAIN}"
ADSENSE_CLIENT = "ca-pub-8782868222380999"
FEEDBACK_EMAIL = "feedback@septicscope.com"


@dataclass
class Page:
    path: Path
    text_parts: list[str] = field(default_factory=list)
    links: list[tuple[str, str]] = field(default_factory=list)
    title: str = ""
    robots: str = ""
    _in_title: bool = False
    _anchor_href: str | None = None
    _anchor_text: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return " ".join(self.text_parts)


class Parser(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.page = Page(path)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.page._in_title = True
        elif tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.page.robots = attrs.get("content", "").lower().strip()
        elif tag == "a" and attrs.get("href"):
            self.page._anchor_href = attrs["href"].strip()
            self.page._anchor_text = []

    def handle_endtag(self, tag):
        if tag == "title":
            self.page._in_title = False
        elif tag == "a" and self.page._anchor_href is not None:
            label = " ".join(self.page._anchor_text).strip()
            self.page.links.append((self.page._anchor_href, label))
            self.page._anchor_href = None
            self.page._anchor_text = []

    def handle_data(self, data):
        value = data.strip()
        if not value:
            return
        self.page.text_parts.append(value)
        if self.page._in_title:
            self.page.title += value
        if self.page._anchor_href is not None:
            self.page._anchor_text.append(value)


def parse(path: Path) -> Page:
    p = Parser(path)
    p.feed(path.read_text(encoding="utf-8", errors="replace"))
    return p.page


def is_external(href: str) -> bool:
    p = urllib.parse.urlparse(href)
    return p.scheme in {"http", "https"} and p.netloc.lower().split(":")[0] not in {DOMAIN, "www." + DOMAIN}


def is_verified_county(path: Path, page: Page) -> bool:
    parts = path.relative_to(SITE).parts
    return (
        len(parts) == 4
        and parts[0] == "counties"
        and parts[-1] == "index.html"
        and "noindex" not in page.robots
        and "Official sources" in page.text
    )


def local_source_candidate(label: str, href: str) -> bool:
    value = f"{label} {href}".lower()
    local_terms = (
        "county", "parish", "borough", "municipal", "city of", "town of",
        "health department", "public health", "environmental health", "local health",
        "district health", "health district", "field office", "regional office",
        "development services", "permit department", "planning and zoning",
    )
    if any(term in value for term in local_terms):
        return True
    # State-administered counties can legitimately use a regional/field office rather
    # than a separate county website. Treat a clearly local government program link as
    # local evidence when it is not a generic federal resource.
    host = urllib.parse.urlparse(href).netloc.lower()
    if host.endswith(".gov") and not host.endswith("epa.gov") and "usa.gov" not in host:
        path = urllib.parse.urlparse(href).path.lower()
        if any(term in path for term in ("county", "local", "district", "office", "health", "environment", "septic", "onsite", "ossf")):
            return True
    return False


def normalized_county_fingerprint(page: Page) -> str:
    text = page.text.lower()
    text = re.sub(r"\b[a-z][a-z .'-]+ county\b", " county ", text)
    text = re.sub(r"\b\d{3}[-.) ]\d{3}[- ]\d{4}\b", " phone ", text)
    text = re.sub(r"\b\d{3,6}\b", " number ", text)
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
    verified = [(path, page) for path, page in pages.items() if is_verified_county(path, page)]
    lookup = [(path, page) for path, page in pages.items() if "Local guide in progress" in page.text]

    if not verified:
        errors.append("No verified county pages were detected")

    fingerprints = Counter()
    for path, page in verified:
        rel = "/" + path.relative_to(SITE).as_posix()
        raw = path.read_text(encoding="utf-8", errors="replace")
        words = re.findall(r"\b[\w'-]+\b", page.text)
        external = [(href, label) for href, label in page.links if is_external(href)]
        local = [(href, label) for href, label in external if local_source_candidate(label, href)]

        if "Official sources checked" not in page.text:
            errors.append(f"Verified county page lacks visible source-check date: {rel}")
        if "Permitting authority" not in page.text:
            errors.append(f"Verified county page lacks permitting authority: {rel}")
        if "Official sources" not in page.text:
            errors.append(f"Verified county page lacks Official sources section: {rel}")
        if len(words) < 180:
            errors.append(f"Verified county page is too thin ({len(words)} words): {rel}")
        if len(external) < 2:
            errors.append(f"Verified county page has fewer than two official/source links: {rel}")
        if not local:
            errors.append(f"Verified county page lacks a county/local/regional official source link: {rel}")
        if 'href="/contact/"' not in raw or "Report outdated county information" not in page.text:
            errors.append(f"Verified county page lacks correction/feedback route: {rel}")
        if ADSENSE_CLIENT not in raw:
            errors.append(f"Verified content page is missing AdSense site code: {rel}")
        fingerprints[normalized_county_fingerprint(page)] += 1

    # Unresearched county helper pages are intentionally noindex and should not be
    # monetized with Auto ads while their county-specific content is incomplete.
    for path, page in lookup:
        rel = "/" + path.relative_to(SITE).as_posix()
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "noindex" not in page.robots:
            errors.append(f"In-progress county page is indexable: {rel}")
        if ADSENSE_CLIENT in raw or "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" in raw:
            errors.append(f"In-progress/noindex county page still carries AdSense Auto ads code: {rel}")

    privacy = SITE / "privacy" / "index.html"
    if not privacy.exists():
        errors.append("Privacy Policy page is missing")
    else:
        raw = privacy.read_text(encoding="utf-8", errors="replace")
        low = raw.lower()
        required = (
            "third-party vendors, including google",
            "cookies to serve ads based on a user's prior visits",
            "google ads settings",
            "personalized advertising",
            "google analytics",
            "google adsense",
            "feedback and contact information",
        )
        for phrase in required:
            if phrase not in low:
                errors.append(f"Privacy Policy missing required disclosure: {phrase}")
        if "https://adssettings.google.com/" not in raw:
            errors.append("Privacy Policy lacks Google Ads Settings opt-out link")
        if ADSENSE_CLIENT in raw or "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" in raw:
            errors.append("Privacy Policy should remain ad-free")

    contact = SITE / "contact" / "index.html"
    if not contact.exists():
        errors.append("Contact & Feedback page is missing")
    else:
        raw = contact.read_text(encoding="utf-8", errors="replace")
        low = raw.lower()
        if "contact &amp; feedback" not in low and "contact & feedback" not in low:
            errors.append("Contact page lacks clear Contact & Feedback heading")
        if f"mailto:{FEEDBACK_EMAIL}" not in raw:
            errors.append("Contact page lacks the public feedback email route")
        if "feedback-form" not in raw:
            errors.append("Contact page lacks feedback form")
        if ADSENSE_CLIENT in raw or "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" in raw:
            errors.append("Contact/feedback utility page should remain ad-free")

    home = SITE / "index.html"
    if home.exists():
        raw = home.read_text(encoding="utf-8", errors="replace")
        for slug in ("privacy", "about", "contact"):
            if f'href="/{slug}/"' not in raw:
                errors.append(f"Homepage does not expose /{slug}/")
    else:
        errors.append("Homepage is missing")

    sitemap = SITE / "sitemap.xml"
    sitemap_urls: set[str] = set()
    if sitemap.exists():
        try:
            root = ET.parse(sitemap).getroot()
            ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            sitemap_urls = {(n.text or "").strip() for n in root.findall(".//s:loc", ns)}
        except Exception as exc:
            errors.append(f"Sitemap could not be parsed by AdSense audit: {exc}")
        for slug in ("privacy", "about", "contact"):
            url = f"{BASE}/{slug}/"
            if url not in sitemap_urls:
                errors.append(f"Trust page missing from sitemap: {url}")
        for path, _page in lookup:
            parts = path.relative_to(SITE).parts
            url = f"{BASE}/" + "/".join(parts[:-1]) + "/"
            if url in sitemap_urls:
                errors.append(f"Noindex/in-progress county is present in sitemap: {url}")
    else:
        errors.append("sitemap.xml is missing")

    ads = SITE / "ads.txt"
    expected_ads = "google.com, pub-8782868222380999, DIRECT, f08c47fec0942fa0"
    if not ads.exists() or expected_ads not in ads.read_text(encoding="utf-8", errors="replace"):
        errors.append("ads.txt is missing the current Google publisher record")

    duplicate_groups = sorted((count, fp) for fp, count in fingerprints.items() if count >= 5)
    if duplicate_groups:
        largest = duplicate_groups[-1][0]
        warnings.append(
            f"Near-template fingerprint check found at least one repeated county-content pattern across {largest} verified pages. "
            "Statewide rules may legitimately repeat, but continue adding local process/contact details as sources become available."
        )

    print("SepticScope AdSense readiness audit")
    print(f"HTML pages: {len(html_files):,}")
    print(f"Verified county guides audited: {len(verified):,}")
    print(f"In-progress/noindex county pages audited: {len(lookup):,}")
    print(f"Sitemap URLs: {len(sitemap_urls):,}")
    print("Privacy policy: checked")
    print("Contact & feedback: checked")
    print("Ad placement safeguards: checked")

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(" -", warning)

    if errors:
        print(f"ERRORS ({len(errors)}):", file=sys.stderr)
        for error in errors[:250]:
            print(" -", error, file=sys.stderr)
        if len(errors) > 250:
            print(f" - ... {len(errors)-250} more errors", file=sys.stderr)
        return 1

    print("PASS: AdSense readiness safeguards and county-source quality gates passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
