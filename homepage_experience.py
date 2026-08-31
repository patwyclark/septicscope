"""Build SepticScope's national homepage, county directory, and location-search assets.

The location finder supports county/state matching from the local national index. ZIP and
city/state searches use public postal coordinates and then resolve the representative
coordinate to a county FIPS with the FCC API, with the U.S. Census geocoder as fallback.
Postal and municipal boundaries can cross county lines, so the UI always tells users to
confirm the property's actual county before relying on permitting information.
"""
from __future__ import annotations

import base64
from collections import Counter, defaultdict
from datetime import date
import gzip
import html
import json
from pathlib import Path
import re
import unicodedata
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DOMAIN = "https://septicscope.com"
GA_MEASUREMENT_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"
LASTMOD = date.today().isoformat()

STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii",
    "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
    "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def display_name(name: str, lsad: str) -> str:
    label = "Census Area" if lsad == "CA" else lsad
    if not label:
        return name
    return name if label.lower() in name.lower() else f"{name} {label}"


def load_rows() -> list[list[str]]:
    data_dir = ROOT / "nationwide_data"
    payload = "".join(
        (data_dir / f"part{i:02d}.txt").read_text(encoding="utf-8").strip()
        for i in range(8)
    )
    rows = json.loads(gzip.decompress(base64.b64decode(payload, validate=True)).decode("utf-8"))
    if len(rows) != 3144 or len({row[3] for row in rows}) != 3144:
        raise RuntimeError(f"Nationwide county dataset integrity failure: {len(rows)} rows")

    collision_counts = Counter((abbr, slugify(name)) for abbr, name, _lsad, _fips in rows)
    safe_rows: list[list[str]] = []
    for abbr, name, lsad, fips in rows:
        if collision_counts[(abbr, slugify(name))] > 1 and str(lsad).lower() != "county":
            label = "Census Area" if lsad == "CA" else lsad
            if str(label).lower() not in name.lower():
                name = f"{name} {label}"
        safe_rows.append([abbr, name, lsad, fips])
    return safe_rows


def load_providers() -> list[dict]:
    path = ROOT / "data" / "providers.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [p for p in data.get("providers", []) if p.get("status") not in {"closed", "inactive"}]


def provider_counts(providers: list[dict]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for provider in providers:
        for item in provider.get("counties_served", []):
            fips = str(item.get("fips", "") if isinstance(item, dict) else item).zfill(5)
            if fips:
                counts[fips] += 1
    return counts


def is_verified_page(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    lower = text.lower()
    return (
        "noindex" not in lower
        and "official sources" in lower
        and "permitting authority" in lower
    )


def analytics_tags() -> str:
    return f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>'''


UI_DIR = ROOT / "ui"
CSS = (UI_DIR / "homepage.css").read_text(encoding="utf-8")
JS = (UI_DIR / "location-search.js").read_text(encoding="utf-8")


def nav_html() -> str:
    return '''<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="nav-shell"><a class="brand" href="/"><span class="brand-mark" aria-hidden="true">SS</span><span>SepticScope</span></a><nav class="desktop-nav" aria-label="Primary"><a href="/counties/">County guides</a><a href="/providers/">Local services</a><a href="/guides/">Homeowner guides</a><a href="/faq/">FAQs</a><a href="/about/">About</a><a class="nav-cta" href="#find-location">Find my county</a></nav><button class="menu-button" type="button" data-menu-button aria-controls="mobile-navigation" aria-expanded="false">Menu</button></div><nav class="mobile-nav" id="mobile-navigation" data-mobile-nav data-open="false" aria-label="Mobile"><a href="/counties/">County guides</a><a href="/providers/">Local services</a><a href="/guides/">Homeowner guides</a><a href="/faq/">FAQs</a><a href="/about/">About</a><a href="#find-location">Find my county</a></nav></header>'''


def footer_html() -> str:
    return '''<footer class="site-footer"><div class="footer-shell" id="septicscope-trust-links-v1"><div class="footer-grid"><div><a class="brand" href="/" style="color:#fff"><span class="brand-mark" style="background:#fff;color:#123d35">SS</span><span>SepticScope</span></a><p class="footer-note">Source-checked county septic permit information, practical homeowner guidance, and a developing directory of publicly documented local service providers.</p></div><div><h3>Find local help</h3><a href="/counties/">County lookup</a><a href="/providers/">Local service directory</a><a href="/contact/">Report a correction</a></div><div><h3>Learn</h3><a href="/guides/">Homeowner guides</a><a href="/faq/">Septic FAQs</a><a href="/guides/septic-maintenance-checklist/">Maintenance checklist</a></div><div><h3>Trust</h3><a href="/about/">About our research</a><a href="/privacy/">Privacy</a><a href="/contact/">Contact &amp; feedback</a></div></div><div class="footer-bottom"><span>© 2026 SepticScope. Independent informational resource; not a government agency.</span><span>Current local agency instructions control.</span></div></div></footer>'''


def search_panel() -> str:
    return '''<div class="search-panel" data-location-search id="find-location"><form class="search-form"><label class="skip-link" for="location-search-input">ZIP code, city and state, or county</label><input class="search-input" id="location-search-input" type="search" inputmode="search" autocomplete="postal-code" placeholder="ZIP, City + State, or County + State" aria-describedby="location-search-help"><button class="search-button" type="submit">Find my county</button></form><div class="search-help" id="location-search-help"><span>Try: <strong>76201</strong>, <strong>Oak Point, TX</strong>, or <strong>Denton County</strong></span><a href="/counties/">Browse all states</a></div><p class="search-status" data-location-status hidden aria-live="polite"></p><div class="search-results" data-location-results></div><div class="location-note">ZIP codes and cities can cross county lines. City and ZIP results use representative coordinates; confirm the property’s actual county before relying on permit rules.</div></div>'''


def state_card_block(state_stats: list[dict], limit: int = 8) -> str:
    selected = sorted(
        state_stats,
        key=lambda item: (-item["verified"], -item["providers"], item["state"]),
    )[:limit]
    return "".join(
        f'<a class="state-card" href="/counties/{item["slug"]}/"><strong>{html.escape(item["state"])}</strong><span>{item["verified"]} verified guides · {item["total"]} locations</span></a>'
        for item in selected
    )


def directory_state_cards(state_stats: list[dict]) -> str:
    return "".join(
        f'<a class="directory-state-card" href="/counties/{item["slug"]}/"><strong>{html.escape(item["state"])}</strong><span>{item["verified"]} verified · {item["total"]} counties/equivalents' + (f' · {item["providers"]} local listings' if item["providers"] else '') + '</span></a>'
        for item in sorted(state_stats, key=lambda item: item["state"])
    )


def ensure_sitemap(urls: list[str]) -> None:
    sitemap = SITE / "sitemap.xml"
    if not sitemap.exists():
        return
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    tree = ET.parse(sitemap)
    root = tree.getroot()
    existing = {
        (node.find(f"{{{ns}}}loc").text or "").strip()
        for node in root.findall(f"{{{ns}}}url")
        if node.find(f"{{{ns}}}loc") is not None
    }
    for url in urls:
        if url in existing:
            continue
        node = ET.SubElement(root, f"{{{ns}}}url")
        ET.SubElement(node, f"{{{ns}}}loc").text = url
        ET.SubElement(node, f"{{{ns}}}lastmod").text = LASTMOD
    tree.write(sitemap, encoding="utf-8", xml_declaration=True)


def build() -> None:
    if not SITE.is_dir():
        raise RuntimeError("Generated site directory is missing")
    rows = load_rows()
    providers = load_providers()
    pcounts = provider_counts(providers)

    location_records: list[dict] = []
    state_totals: Counter[str] = Counter()
    state_verified: Counter[str] = Counter()
    state_provider_ids: dict[str, set[str]] = defaultdict(set)
    verified_total = 0

    provider_ids_by_fips: dict[str, set[str]] = defaultdict(set)
    for provider in providers:
        pid = str(provider.get("id", provider.get("business_name", "")))
        for item in provider.get("counties_served", []):
            fips = str(item.get("fips", "") if isinstance(item, dict) else item).zfill(5)
            if fips:
                provider_ids_by_fips[fips].add(pid)

    for abbr, name, lsad, fips in rows:
        state = STATE_NAMES[abbr]
        state_slug = slugify(state)
        county_slug = slugify(name)
        display = display_name(name, lsad)
        url = f"/counties/{state_slug}/{county_slug}/"
        path = SITE / "counties" / state_slug / county_slug / "index.html"
        verified = is_verified_page(path)
        verified_total += int(verified)
        state_totals[abbr] += 1
        state_verified[abbr] += int(verified)
        state_provider_ids[abbr].update(provider_ids_by_fips.get(fips, set()))
        location_records.append({
            "f": fips,
            "n": display,
            "s": state,
            "a": abbr,
            "u": url,
            "v": verified,
            "p": pcounts.get(fips, 0),
        })

    faq_count = len(list((SITE / "faq").glob("*/index.html")))
    guide_count = len(list((SITE / "guides").glob("*/index.html")))
    state_stats = [
        {
            "state": STATE_NAMES[abbr],
            "slug": slugify(STATE_NAMES[abbr]),
            "total": state_totals[abbr],
            "verified": state_verified[abbr],
            "providers": len(state_provider_ids[abbr]),
        }
        for abbr in STATE_NAMES
    ]

    assets = SITE / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "septicscope-v3.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (assets / "location-search-v3.js").write_text(JS.strip() + "\n", encoding="utf-8")
    data_dir = SITE / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    location_payload = {
        "schema_version": 1,
        "generated_at": LASTMOD,
        "record_count": len(location_records),
        "method_note": "County and state names are local. ZIP and city lookups use postal coordinates and public county geocoding in the browser; property boundaries must be confirmed.",
        "records": location_records,
    }
    (data_dir / "location-index.json").write_text(
        json.dumps(location_payload, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    guide_cards = '''
<article class="guide-card"><div class="guide-top"><span class="guide-tag">Maintenance</span><h3>Septic maintenance checklist</h3></div><div class="guide-body"><p>Monthly, yearly, inspection, and pumping tasks in one printable homeowner plan.</p><a href="/guides/septic-maintenance-checklist/">Open the checklist →</a></div></article>
<article class="guide-card"><div class="guide-top"><span class="guide-tag">Buying a home</span><h3>Septic inspection checklist</h3></div><div class="guide-body"><p>Know what a meaningful inspection should cover before a purchase or major decision.</p><a href="/guides/septic-inspection-checklist/">Review inspection steps →</a></div></article>
<article class="guide-card"><div class="guide-top"><span class="guide-tag">Troubleshooting</span><h3>Drainfield repair or replacement?</h3></div><div class="guide-body"><p>Separate localized repair possibilities from larger soil-treatment-area failures.</p><a href="/guides/septic-drainfield-repair-replacement/">Compare the options →</a></div></article>
<article class="guide-card"><div class="guide-top"><span class="guide-tag">System basics</span><h3>Types of septic systems</h3></div><div class="guide-body"><p>Compare conventional, aerobic, mound, drip, chamber, and sand-filter systems.</p><a href="/guides/types-of-septic-systems/">Identify your system →</a></div></article>
<article class="guide-card"><div class="guide-top"><span class="guide-tag">Planning tool</span><h3>Septic tank size calculator</h3></div><div class="guide-body"><p>Use documented state examples without mistaking a generic chart for a permit-ready design.</p><a href="/guides/septic-tank-size-calculator/">Use the calculator →</a></div></article>
<article class="guide-card"><div class="guide-top"><span class="guide-tag">Long-term ownership</span><h3>How long does a septic system last?</h3></div><div class="guide-body"><p>Plan for aging tanks, pumps, controls, and drainfields without relying on an artificial expiration date.</p><a href="/guides/septic-system-lifespan/">Plan ahead →</a></div></article>'''

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": "Can I find a SepticScope county page by ZIP code?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. SepticScope resolves a ZIP code from a representative postal coordinate to a likely county. Because ZIP areas can cross county lines, confirm the property's actual county before relying on permit information."}},
            {"@type": "Question", "name": "Are local septic providers ranked or recommended?", "acceptedAnswer": {"@type": "Answer", "text": "No. Ordinary listings are neutrally ordered and based on documented public business and service-area information. Homeowners should independently confirm current licensing, insurance, availability, scope, and pricing."}},
            {"@type": "Question", "name": "Does SepticScope issue septic permits?", "acceptedAnswer": {"@type": "Answer", "text": "No. SepticScope is an independent information resource. The applicable county, health department, environmental health office, state program, or other authorized local agency controls permitting decisions."}},
        ],
    }
    site_schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": f"{DOMAIN}/#organization", "name": "SepticScope", "url": f"{DOMAIN}/"},
            {"@type": "WebSite", "@id": f"{DOMAIN}/#website", "url": f"{DOMAIN}/", "name": "SepticScope", "publisher": {"@id": f"{DOMAIN}/#organization"}, "potentialAction": {"@type": "SearchAction", "target": f"{DOMAIN}/counties/?q={{search_term_string}}", "query-input": "required name=search_term_string"}},
        ],
    }

    home = (UI_DIR / "homepage.html").read_text(encoding="utf-8")
    replacements = {
        "@@TAGS@@": analytics_tags(),
        "@@SITE_SCHEMA@@": json.dumps(site_schema, separators=(",", ":")).replace("<", "\\u003c"),
        "@@FAQ_SCHEMA@@": json.dumps(faq_schema, separators=(",", ":")).replace("<", "\\u003c"),
        "@@NAV@@": nav_html(),
        "@@SEARCH@@": search_panel(),
        "@@COUNTIES@@": f"{len(rows):,}",
        "@@VERIFIED@@": f"{verified_total:,}",
        "@@FAQ_COUNT@@": f"{faq_count:,}",
        "@@GUIDE_COUNT@@": f"{guide_count:,}",
        "@@GUIDE_CARDS@@": guide_cards,
        "@@PROVIDER_COUNT@@": f"{len(providers):,}",
        "@@STATE_CARDS@@": state_card_block(state_stats),
        "@@FOOTER@@": footer_html(),
    }
    for key, value in replacements.items():
        home = home.replace(key, value)
    (SITE / "index.html").write_text(home, encoding="utf-8")

    directory = (UI_DIR / "county-directory.html").read_text(encoding="utf-8")
    replacements = {
        "@@TAGS@@": analytics_tags(),
        "@@NAV@@": nav_html().replace('href="#find-location"', 'href="#find-location-directory"'),
        "@@SEARCH@@": search_panel().replace('id="find-location"', 'id="find-location-directory"').replace('for="location-search-input"', 'for="directory-location-search-input"').replace('id="location-search-input"', 'id="directory-location-search-input"'),
        "@@DIRECTORY_STATES@@": directory_state_cards(state_stats),
        "@@FOOTER@@": footer_html(),
    }
    for key, value in replacements.items():
        directory = directory.replace(key, value)
    (SITE / "counties" / "index.html").write_text(directory, encoding="utf-8")

    ensure_sitemap([f"{DOMAIN}/", f"{DOMAIN}/counties/"])

    for path in (SITE / "index.html", SITE / "counties" / "index.html"):
        text = path.read_text(encoding="utf-8")
        if "location-search-v3.js" not in text or "data-location-search" not in text:
            raise RuntimeError(f"Location search integration missing: {path}")
        if 'href="indiana/' in text or 'href="/indiana/' in text:
            raise RuntimeError(f"Launch-era Indiana navigation remains: {path}")
        if text.lower().count("<h1") != 1:
            raise RuntimeError(f"Expected one H1: {path}")
    if len(location_records) != 3144:
        raise RuntimeError("Location index is incomplete")
    print(
        "Homepage experience complete: "
        f"{len(location_records):,} county records; {verified_total:,} verified guides; "
        f"{len(providers):,} provider listings; city/ZIP resolver enabled"
    )


if __name__ == "__main__":
    build()
