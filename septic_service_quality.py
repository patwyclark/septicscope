#!/usr/bin/env python3
"""Gate the national service search until every county has reviewed coverage."""
from __future__ import annotations

import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DATA_FILE = SITE / "data" / "septic-services-near-me.json"
STATUS_FILE = SITE / "data" / "service-directory-status.json"
EXPECTED_COUNTIES = 3144
DOMAIN = "https://septicscope.com"
GA_MEASUREMENT_ID = "G-F6RB8YERCM"


def load_data() -> dict:
    if not DATA_FILE.exists():
        raise RuntimeError("Generated provider-search data is missing")
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("Generated provider-search data must be an object")
    return data


def coverage_status(data: dict) -> tuple[int, int, bool]:
    providers = [item for item in data.get("providers", []) if isinstance(item, dict)]
    counties = [item for item in data.get("counties", []) if isinstance(item, dict)]
    valid_fips = {str(item.get("f", "")) for item in counties if re.fullmatch(r"\d{5}", str(item.get("f", "")))}
    covered = {
        str(fips)
        for provider in providers
        for fips in provider.get("fips", [])
        if str(fips) in valid_fips
    }
    complete = len(valid_fips) == EXPECTED_COUNTIES and len(covered) == EXPECTED_COUNTIES
    return len(providers), len(covered), complete


def remove_sitemap_urls(urls: set[str]) -> None:
    sitemap = SITE / "sitemap.xml"
    if not sitemap.exists():
        raise RuntimeError("sitemap.xml is missing")
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    tree = ET.parse(sitemap)
    root = tree.getroot()
    for node in list(root):
        loc = node.find(f"{{{ns}}}loc")
        if loc is not None and (loc.text or "").strip() in urls:
            root.remove(node)
    tree.write(sitemap, encoding="utf-8", xml_declaration=True)


def add_sitemap_url(url: str) -> None:
    sitemap = SITE / "sitemap.xml"
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    tree = ET.parse(sitemap)
    root = tree.getroot()
    if any((node.find(f"{{{ns}}}loc") is not None and (node.find(f"{{{ns}}}loc").text or "").strip() == url) for node in root):
        return
    node = ET.SubElement(root, f"{{{ns}}}url")
    ET.SubElement(node, f"{{{ns}}}loc").text = url
    tree.write(sitemap, encoding="utf-8", xml_declaration=True)


def hidden_locator_page(provider_count: int, covered_count: int) -> str:
    percentage = min(100, round(covered_count / EXPECTED_COUNTIES * 100, 1))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>National Septic Service Search in Development | SepticScope</title><meta name="description" content="SepticScope is withholding its national septic service search until every U.S. county and county-equivalent has source-reviewed provider coverage."><meta name="robots" content="noindex,follow"><link rel="canonical" href="{DOMAIN}/septic-services-near-me/"><link rel="stylesheet" href="/assets/septic-services-near-me.css"><script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}');</script><style>.hold-wrap{{max-width:820px;margin:auto;padding:70px 22px}}.hold-card{{border:1px solid var(--line);border-radius:22px;padding:30px;background:#fff;box-shadow:var(--shadow)}}.hold-card h1{{color:var(--forest);font-size:clamp(2.2rem,5vw,3.8rem);line-height:1.06}}.hold-progress{{height:14px;border-radius:999px;background:#e5ece8;overflow:hidden;margin:18px 0}}.hold-progress span{{display:block;height:100%;background:var(--forest2)}}.hold-button{{display:inline-flex;background:var(--forest);color:#fff;padding:12px 16px;border-radius:11px;text-decoration:none;font-weight:900}}</style></head><body><header class="ssn-header"><nav class="ssn-nav"><a class="ssn-brand" href="/"><span class="ssn-mark">SS</span><span>SepticScope</span></a><div class="ssn-links"><a class="ssn-nav-cta" href="/counties/">County lookup</a><a href="/guides/">Guides</a><a href="/faq/">FAQs</a></div></nav></header><main class="hold-wrap"><div class="hold-card"><p class="ssn-eyebrow">Coverage before promotion</p><h1>The national septic service search is still being built.</h1><p>SepticScope is not publishing a ZIP-based service finder that can return an empty result for most of the country. The search will launch only after every U.S. county and county-equivalent has at least one source-reviewed provider relationship.</p><p><strong>{covered_count:,} of {EXPECTED_COUNTIES:,} counties</strong> currently have reviewed coverage from <strong>{provider_count:,} provider records</strong>.</p><div class="hold-progress" aria-label="National provider coverage"><span style="width:{percentage}%"></span></div><p>For now, use the county lookup to find permit contacts, official sources, county FIPS codes, records starting points, and local septic information.</p><p><a class="hold-button" href="/counties/">Find county septic information</a></p></div></main><footer class="ssn-footer"><div class="ssn-footer-inner">© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/contact/">Corrections & feedback</a></div></footer></body></html>'''


def repair_public_lookup_copy() -> None:
    home = SITE / "index.html"
    counties = SITE / "counties" / "index.html"
    if not home.exists() or not counties.exists():
        raise RuntimeError("Generated homepage or county directory is missing")

    home_text = home.read_text(encoding="utf-8", errors="replace")
    home_text = home_text.replace(
        "/faq/how-do-i-find-my-septic-system-records/",
        "/counties/",
    )
    home.write_text(home_text, encoding="utf-8")
    if "/faq/how-do-i-find-my-septic-system-records/" in home_text:
        raise RuntimeError("Unavailable septic-records route remains on the homepage")

    county_text = counties.read_text(encoding="utf-8", errors="replace")
    if "County FIPS" not in county_text:
        county_text = county_text.replace(
            "<p>Search the property location or a county FIPS code.",
            "<p><strong>County FIPS lookup:</strong> Search the property location or a county FIPS code.",
            1,
        )
    counties.write_text(county_text, encoding="utf-8")
    if "County FIPS" not in county_text:
        raise RuntimeError("County directory is missing visible County FIPS lookup guidance")


def scrub_public_directory_links() -> int:
    changed = 0
    targets = ("/septic-services-near-me/", "/providers/")
    pattern_template = r"<a\b([^>]*?)href=[\"']{target}[^\"']*[\"']([^>]*)>(.*?)</a>"
    for path in SITE.rglob("*.html"):
        if path in {SITE / "septic-services-near-me" / "index.html", SITE / "providers" / "index.html"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        updated = text
        for target in targets:
            pattern = re.compile(pattern_template.format(target=re.escape(target)), flags=re.I | re.S)
            updated = pattern.sub(lambda match: re.sub(r"<[^>]+>", "", match.group(3)), updated)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def public_references() -> list[str]:
    findings = []
    for path in SITE.rglob("*.html"):
        if path in {SITE / "septic-services-near-me" / "index.html", SITE / "providers" / "index.html"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        if 'href="/septic-services-near-me/' in text or "href='/septic-services-near-me/" in text:
            findings.append(path.relative_to(SITE).as_posix() + ": service locator")
        if 'href="/providers/' in text or "href='/providers/" in text:
            findings.append(path.relative_to(SITE).as_posix() + ": provider directory")
    return findings


def hide_incomplete_directories(provider_count: int, covered_count: int) -> None:
    locator = SITE / "septic-services-near-me" / "index.html"
    locator.parent.mkdir(parents=True, exist_ok=True)
    locator.write_text(hidden_locator_page(provider_count, covered_count), encoding="utf-8")
    remove_sitemap_urls({f"{DOMAIN}/septic-services-near-me/", f"{DOMAIN}/providers/"})
    repair_public_lookup_copy()
    scrub_public_directory_links()


def verify_hidden() -> None:
    homepage = (SITE / "index.html").read_text(encoding="utf-8", errors="replace")
    counties = (SITE / "counties" / "index.html").read_text(encoding="utf-8", errors="replace")
    locator = (SITE / "septic-services-near-me" / "index.html").read_text(encoding="utf-8", errors="replace")
    provider = (SITE / "providers" / "index.html").read_text(encoding="utf-8", errors="replace")
    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8", errors="replace")
    if "data-county-lookup-root" not in homepage or "/assets/county-lookup.js" not in homepage:
        raise RuntimeError("Homepage county lookup is missing")
    if "data-county-lookup-root" not in counties or "County FIPS" not in counties or "FIPS 48121" not in counties:
        raise RuntimeError("County information directory is missing the restored ZIP/city/county/FIPS lookup")
    if "noindex,follow" not in locator.replace(" ", "").lower() or "data-provider-card" in locator:
        raise RuntimeError("Incomplete service locator must be noindex and non-searchable")
    provider_body = provider.split("<main", 1)[-1]
    if "noindex,follow" not in provider.replace(" ", "").lower() or '<article class="ss-provider-card">' in provider_body:
        raise RuntimeError("Incomplete global provider directory must be noindex and hide listing cards")
    if f"{DOMAIN}/septic-services-near-me/" in sitemap or f"{DOMAIN}/providers/" in sitemap:
        raise RuntimeError("Incomplete global service pages must not appear in the sitemap")
    references = public_references()
    if references:
        raise RuntimeError("Incomplete service-directory links remain public: " + ", ".join(references[:10]))


def verify_public() -> None:
    repair_public_lookup_copy()
    locator = (SITE / "septic-services-near-me" / "index.html").read_text(encoding="utf-8", errors="replace")
    if "noindex" in locator.lower() or "data-provider-card" not in locator:
        raise RuntimeError("Complete service locator should be public and searchable")
    add_sitemap_url(f"{DOMAIN}/septic-services-near-me/")
    add_sitemap_url(f"{DOMAIN}/providers/")


def main() -> None:
    data = load_data()
    provider_count, covered_count, complete = coverage_status(data)
    STATUS_FILE.write_text(
        json.dumps({
            "schema_version": 1,
            "public": complete,
            "launch_requirement": "At least one source-reviewed provider relationship for every U.S. county and county-equivalent.",
            "provider_records": provider_count,
            "covered_counties": covered_count,
            "required_counties": EXPECTED_COUNTIES,
            "remaining_counties": EXPECTED_COUNTIES - covered_count,
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    if complete:
        verify_public()
        print(f"National service search public: {covered_count}/{EXPECTED_COUNTIES} counties covered")
        return
    hide_incomplete_directories(provider_count, covered_count)
    verify_hidden()
    print(
        f"National service search hidden: {covered_count}/{EXPECTED_COUNTIES} counties covered; "
        "county lookup restored as the primary public location search"
    )


if __name__ == "__main__":
    main()
