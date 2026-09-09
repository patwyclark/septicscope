#!/usr/bin/env python3
"""Validate SepticScope's quality-first recovery output.

This check parses the robots meta tag instead of searching visible copy for the word
"noindex". Editorial pages legitimately discuss noindex, so substring tests can create
false failures and hide real deployment regressions.
"""
from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ADSENSE = "ca-pub-8782868222380999"
DOMAIN = "https://septicscope.com"


class MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.robots = ""
        self.canonical = ""
        self.h1_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {str(key).lower(): str(value or "") for key, value in attrs}
        if tag.lower() == "meta" and values.get("name", "").lower() == "robots":
            self.robots = values.get("content", "").lower().replace(" ", "")
        elif tag.lower() == "link" and "canonical" in values.get("rel", "").lower().split():
            self.canonical = values.get("href", "").strip()
        elif tag.lower() == "h1":
            self.h1_count += 1


def read(path: Path) -> str:
    if not path.exists():
        raise RuntimeError(f"Required generated file is missing: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="replace")


def page_meta(raw: str) -> MetaParser:
    parser = MetaParser()
    parser.feed(raw)
    return parser


def is_noindex(raw: str) -> bool:
    return "noindex" in page_meta(raw).robots


def page_path(url: str) -> Path:
    route = urlparse(url).path.strip("/")
    return SITE / route / "index.html" if route else SITE / "index.html"


def visible_words(raw: str) -> int:
    main = raw.split("<main", 1)[-1].split("</main>", 1)[0]
    main = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", main, flags=re.I | re.S)
    main = re.sub(r"<[^>]+>", " ", main)
    return len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", main))


def sitemap_urls() -> list[str]:
    root = ET.parse(SITE / "sitemap.xml").getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [(node.text or "").strip() for node in root.findall(".//s:loc", ns)]


def redirect_counts() -> tuple[int, int]:
    static = 0
    dynamic = 0
    for line in read(SITE / "_redirects").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        source = line.split()[0]
        if "*" in source or re.search(r"/:[A-Za-z]", source):
            dynamic += 1
        else:
            static += 1
    return static, dynamic


def check() -> int:
    errors: list[str] = []

    required = (
        SITE / "deployment-manifest.txt",
        SITE / "build-info.json",
        SITE / "data/national-coverage-manifest.json",
        SITE / "data/keyword-map.json",
        SITE / "data/source-catalog.json",
        SITE / "data/project-audit-summary.json",
        SITE / "data/project-audit-summary.txt",
        SITE / "data/hourly-seo-build-report.json",
        SITE / "data/adsense-quality-recovery.json",
        SITE / "data/adsense-quality-recovery.txt",
        SITE / "data/county-lookup.json",
        SITE / "assets/county-lookup.js",
        SITE / "index.html",
        SITE / "counties/index.html",
        SITE / "guides/index.html",
        SITE / "faq/index.html",
        SITE / "about/index.html",
        SITE / "privacy/index.html",
        SITE / "contact/index.html",
        SITE / "providers/index.html",
        SITE / "septic-services-near-me/index.html",
        SITE / "guides/buying-a-house-with-septic/index.html",
        SITE / "guides/septic-maintenance-checklist/index.html",
        SITE / "guides/septic-inspection-checklist/index.html",
        SITE / "guides/septic-drainfield-repair-replacement/index.html",
        SITE / "guides/types-of-septic-systems/index.html",
        SITE / "guides/septic-system-lifespan/index.html",
    )
    for path in required:
        if not path.exists():
            errors.append(f"Missing required output: {path.relative_to(ROOT)}")

    if errors:
        print("QUALITY RECOVERY ERRORS:")
        for error in errors:
            print(" -", error)
        return 1

    recovery = json.loads(read(SITE / "data/adsense-quality-recovery.json"))
    baseline = json.loads(read(ROOT / "data/quality-baseline.json"))
    summary = json.loads(read(SITE / "data/project-audit-summary.json"))
    build_info = json.loads(read(SITE / "build-info.json"))
    lookup = json.loads(read(SITE / "data/county-lookup.json"))
    service_status = json.loads(read(SITE / "data/service-directory-status.json"))
    counts = summary.get("counts", {})

    approved = int(recovery.get("quality_approved_counties", -1))
    retained_guides = int(recovery.get("retained_long_form_guides", -1))
    expected_sitemap = int(recovery.get("sitemap_urls", -1))
    if not recovery.get("recovery_mode"):
        errors.append("Quality recovery mode is not active")
    if recovery.get("strict_gate") is None:
        errors.append("Strict county quality gate is missing from the recovery report")
    if approved < int(baseline["minimum_verified_counties"]):
        errors.append(f"Only {approved} county guides pass the quality floor")
    if approved > int(baseline["maximum_indexable_county_guides"]):
        errors.append(f"{approved} county guides exceed the public-footprint ceiling")
    if retained_guides < int(baseline["minimum_retained_long_form_guides"]):
        errors.append(f"Only {retained_guides} substantive guides survived")
    if not 1 <= expected_sitemap <= int(baseline["maximum_recovery_sitemap_urls"]):
        errors.append(f"Focused sitemap count is invalid: {expected_sitemap}")
    if int(counts.get("verified_county_guides", -2)) != approved:
        errors.append("Inventory/recovery county count drift")
    if int(build_info.get("verified_county_guides", -3)) != approved:
        errors.append("Build-info/recovery county count drift")
    if int(build_info.get("published_county_or_equivalent_pages", 0)) != 3144:
        errors.append("The national county/FIPS lookup no longer covers all 3,144 county-equivalents")

    for key in (
        "pages_without_primary_keywords", "duplicate_title_groups", "duplicate_h1_groups",
        "duplicate_meta_description_groups", "canonical_errors", "canonical_domain_conflicts",
        "accessibility_warnings", "legacy_brand_occurrences",
    ):
        if int(counts.get(key, -1)) != 0:
            errors.append(f"Metadata quality regression: {key}={counts.get(key)}")

    county_rows = lookup.get("counties", [])
    if lookup.get("record_count") != 3144 or len(county_rows) != 3144:
        errors.append("County lookup does not retain all 3,144 county-equivalents")
    if len({row.get("f") for row in county_rows}) != 3144:
        errors.append("County lookup contains duplicate FIPS records")
    if sum(bool(row.get("v")) for row in county_rows) != approved:
        errors.append("County lookup approved-guide flags drift from recovery report")

    home = read(SITE / "index.html")
    for phrase in (
        "Practical septic guidance for real property decisions",
        "Fewer pages, stronger reasons to trust each one",
        "One comprehensive septic FAQ instead of thin answer pages",
        "data-county-lookup-root",
    ):
        if phrase not in home:
            errors.append(f"Quality-first homepage is missing {phrase!r}")
    if ADSENSE not in home:
        errors.append("Substantive homepage lost AdSense site code")
    if is_noindex(home):
        errors.append("Homepage is unexpectedly noindex")
    for href in ('href="/providers/', 'href="/septic-services-near-me/'):
        if href in home.lower():
            errors.append(f"Homepage promotes an unfinished service feature: {href}")

    faq = read(SITE / "faq/index.html")
    if faq.count("<h2") < 10 or '"@type": "FAQPage"' not in faq:
        errors.append("Consolidated FAQ hub is incomplete")
    if visible_words(faq) < 1100:
        errors.append(f"Consolidated FAQ is too thin: {visible_words(faq)} words")
    if ADSENSE not in faq or is_noindex(faq):
        errors.append("Substantive FAQ must be indexable and carry the AdSense site code")

    about = read(SITE / "about/index.html")
    if visible_words(about) < 800 or "How automation is used" not in about or "Advertising and commercial separation" not in about:
        errors.append("Editorial-transparency page is incomplete")
    if ADSENSE in about:
        errors.append("About/editorial-policy page must remain ad-free")
    if is_noindex(about):
        errors.append("About/editorial-policy page is unexpectedly noindex")

    guides_hub = read(SITE / "guides/index.html")
    if "Shorter or overlapping pages have been withheld or consolidated" not in guides_hub:
        errors.append("Quality-reviewed guide hub is not deployed")
    if ADSENSE in guides_hub or is_noindex(guides_hub):
        errors.append("Guide hub must be indexable navigation and ad-free")
    for guide_route in recovery.get("retained_guide_routes", []):
        guide_raw = read(page_path(DOMAIN + guide_route))
        if guide_route not in guides_hub:
            errors.append(f"Guide hub is missing retained guide {guide_route}")
        if is_noindex(guide_raw) or ADSENSE not in guide_raw:
            errors.append(f"Retained guide is not indexable/monetizable: {guide_route}")
    for item in recovery.get("demoted_guides", []):
        route = item.get("route") if isinstance(item, dict) else ""
        if route and route in guides_hub:
            errors.append(f"Guide hub still promotes withheld guide {route}")

    strict = recovery.get("strict_gate", {})
    for item in recovery.get("approved_counties", []):
        raw = read(page_path(item["url"]))
        if is_noindex(raw) or ADSENSE not in raw:
            errors.append(f"Approved county is not indexable/monetizable: {item['url']}")
        if int(item.get("main_words", 0)) < int(strict.get("minimum_main_words", 350)):
            errors.append(f"Approved county lacks main-content depth: {item['url']}")
        if int(item.get("external_sources", 0)) < int(strict.get("minimum_external_sources", 5)):
            errors.append(f"Approved county lacks source depth: {item['url']}")
        if int(item.get("local_sources", 0)) < int(strict.get("minimum_local_sources", 2)):
            errors.append(f"Approved county lacks local sources: {item['url']}")
        if int(item.get("local_detail_score", 0)) < int(strict.get("minimum_local_detail_score", 5)):
            errors.append(f"Approved county lacks local details: {item['url']}")
        if float(item.get("shared_template_ratio", 1)) > float(strict.get("maximum_shared_template_ratio", 0.35)):
            errors.append(f"Approved county remains too template-heavy: {item['url']}")

    # Only an actual robots meta directive determines whether a page is noindex.
    noindex_with_ads = []
    for path in SITE.rglob("*.html"):
        raw = read(path)
        if is_noindex(raw) and ADSENSE in raw:
            noindex_with_ads.append(str(path.relative_to(SITE)))
    if noindex_with_ads:
        errors.append(f"Noindex pages still carry AdSense: {noindex_with_ads[:10]}")

    for relative in (
        "counties/index.html", "guides/index.html", "privacy/index.html", "contact/index.html",
        "about/index.html", "providers/index.html", "septic-services-near-me/index.html",
    ):
        if ADSENSE in read(SITE / relative):
            errors.append(f"Navigation/trust/unfinished page still carries ads: {relative}")
    for path in SITE.glob("counties/*/index.html"):
        raw = read(path)
        if not is_noindex(raw) or ADSENSE in raw:
            errors.append(f"Navigation-only state hub must be noindex/ad-free: {path.relative_to(SITE)}")
    for path in SITE.glob("faq/*/index.html"):
        raw = read(path)
        if not is_noindex(raw) or ADSENSE in raw:
            errors.append(f"Consolidated FAQ leaf must be noindex/ad-free: {path.relative_to(SITE)}")

    for label, relative in (
        ("provider directory", "providers/index.html"),
        ("service locator", "septic-services-near-me/index.html"),
    ):
        raw = read(SITE / relative)
        if not is_noindex(raw) or ADSENSE in raw:
            errors.append(f"Incomplete {label} must be noindex/ad-free")
    if bool(service_status.get("public")):
        errors.append("Global service directory unexpectedly launched")

    growth = json.loads(read(ROOT / "data/growth-links.json"))
    if growth.get("links"):
        errors.append("Repetitive automatic growth links remain active")
    workflow = read(ROOT / ".github/workflows/hourly-growth-maintenance.yml")
    if "cron:" in workflow or "--apply-one" in workflow or "git push origin HEAD:main" in workflow:
        errors.append("Automatic scheduled content mutation is still enabled")

    urls = sitemap_urls()
    if len(urls) != expected_sitemap or len(urls) != len(set(urls)):
        errors.append(f"Focused sitemap drift: {len(urls)} URLs, expected {expected_sitemap}")
    for url in urls:
        raw = read(page_path(url))
        if is_noindex(raw):
            errors.append(f"Noindex page appears in focused sitemap: {url}")
    for forbidden in (f"{DOMAIN}/providers/", f"{DOMAIN}/septic-services-near-me/"):
        if forbidden in urls:
            errors.append(f"Hidden service route remains in sitemap: {forbidden}")

    static_redirects, dynamic_redirects = redirect_counts()
    if static_redirects > 2000 or dynamic_redirects > 100:
        errors.append(f"Cloudflare redirect budget exceeded: {static_redirects} static/{dynamic_redirects} dynamic")

    if errors:
        print(f"QUALITY RECOVERY ERRORS ({len(errors)}):")
        for error in errors[:200]:
            print(" -", error)
        return 1

    print(
        "PASS: quality recovery — "
        f"{approved} locally differentiated county guides, {retained_guides} substantive guides, "
        f"{len(urls)} sitemap URLs, {static_redirects} static redirects"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
