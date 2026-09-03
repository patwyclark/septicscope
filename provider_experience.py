#!/usr/bin/env python3
"""Render source-checked local septic providers into the generated site.

Provider cards may appear on a county page when a source supports that county. The
national provider directory stays hidden and noindex until every county-equivalent has
at least one source-reviewed provider relationship.
"""
from __future__ import annotations

from collections import defaultdict
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
PROVIDER_FILE = ROOT / "data" / "providers.json"
INDEXNOW_KEY_FILE = ROOT / "data" / "indexnow-key.txt"
MANIFEST_FILE = SITE / "data" / "national-coverage-manifest.json"
DOMAIN = "https://septicscope.com"
GA_MEASUREMENT_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"
SECTION_MARKER = 'data-septicscope-provider-section="1"'
STYLE_MARKER = 'data-septicscope-provider-style="1"'
EXPECTED_COUNTIES = 3144

GA_TAG = f'''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}');</script>'''
ADSENSE_TAG = f'''<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>'''

STYLE = r''':root{--ss-ink:#17212b;--ss-muted:#5b6672;--ss-line:#dce3e8;--ss-panel:#f7fafb;--ss-soft:#eaf5f1;--ss-accent:#176b5b;--ss-warm:#fff8ed}*{box-sizing:border-box}.ss-provider-wrap{max-width:1080px;margin:auto;padding:42px 24px 72px}.ss-provider-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}.ss-provider-card{border:1px solid var(--ss-line);border-radius:16px;padding:20px;background:#fff;box-shadow:0 8px 24px rgba(23,33,43,.05)}.ss-provider-card h3{margin:0 0 8px;font-size:1.18rem}.ss-provider-meta{color:var(--ss-muted);font-size:.94rem}.ss-provider-tags{display:flex;flex-wrap:wrap;gap:7px;margin:13px 0}.ss-provider-tag{display:inline-block;background:var(--ss-soft);color:#0f5548;border-radius:999px;padding:4px 9px;font-size:.8rem;font-weight:700}.ss-provider-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}.ss-provider-actions a{display:inline-flex;align-items:center;justify-content:center;padding:9px 12px;border-radius:9px;border:1px solid var(--ss-line);text-decoration:none;font-weight:700}.ss-provider-actions a:first-child{background:var(--ss-accent);color:#fff;border-color:var(--ss-accent)}.ss-provider-note{background:var(--ss-warm);border:1px solid #edd9b7;border-radius:14px;padding:16px;margin:20px 0}.ss-provider-local{border-top:1px solid var(--ss-line);margin-top:38px;padding-top:28px}.ss-provider-local .ss-provider-grid{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}.ss-progress{height:12px;border-radius:999px;background:#e6ece9;overflow:hidden}.ss-progress span{display:block;height:100%;background:var(--ss-accent)}@media(max-width:640px){.ss-provider-actions{display:grid}.ss-provider-actions a{width:100%}}'''

SERVICE_LABELS = {
    "pumping": "Pumping", "septic_pumping": "Pumping", "cleaning": "Tank cleaning",
    "inspection": "Inspection", "inspections": "Inspection", "installation": "Installation",
    "installations": "Installation", "repair": "Repair", "repairs": "Repair",
    "maintenance": "Maintenance", "aerobic": "Aerobic systems",
    "design": "Design / evaluation", "locating": "Tank locating",
    "septic_services": "Septic services",
}


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected an object in {path}")
    return data


def active_providers() -> list[dict]:
    data = load_json(PROVIDER_FILE)
    providers = []
    for raw in data.get("providers", []):
        if not isinstance(raw, dict):
            continue
        if str(raw.get("status", "active")).lower() not in {"active", "verified"}:
            continue
        if not str(raw.get("business_name", "")).strip():
            continue
        providers.append(raw)
    providers.sort(key=lambda item: (str(item.get("business_name", "")).casefold(), str(item.get("id", ""))))
    return providers


def county_fips(provider: dict) -> list[str]:
    values: list[str] = []
    for item in provider.get("counties_served", []):
        value = item.get("fips", "") if isinstance(item, dict) else item
        value = str(value).strip()
        if re.fullmatch(r"\d{5}", value) and value not in values:
            values.append(value)
    return values


def service_labels(provider: dict) -> list[str]:
    labels: list[str] = []
    for raw in provider.get("service_categories", []):
        key = re.sub(r"[^a-z0-9]+", "_", str(raw).lower()).strip("_")
        label = SERVICE_LABELS.get(key, str(raw).replace("_", " ").strip().title())
        if label and label not in labels:
            labels.append(label)
    return labels or ["Septic services"]


def outbound_rel(provider: dict) -> str:
    return "sponsored noopener" if provider.get("sponsored") or provider.get("affiliate") else "nofollow noopener"


def provider_card(provider: dict, county_links: dict[str, tuple[str, str]] | None = None, compact: bool = False) -> str:
    name = escape(str(provider.get("business_name", "")).strip())
    website = str(provider.get("website", "")).strip()
    phone = str(provider.get("public_phone", "")).strip()
    city = str(provider.get("city", "")).strip()
    state = str(provider.get("state", "")).strip()
    zip_code = str(provider.get("zip_code", "")).strip()
    location = ", ".join(part for part in (city, state) if part)
    if zip_code:
        location = f"{location} {escape(zip_code)}".strip()
    tags = "".join(f'<span class="ss-provider-tag">{escape(label)}</span>' for label in service_labels(provider))
    actions: list[str] = []
    if website.startswith(("https://", "http://")):
        actions.append(f'<a href="{escape(website)}" rel="{outbound_rel(provider)}">Visit website</a>')
    if phone:
        dial = re.sub(r"[^0-9+]", "", phone)
        actions.append(f'<a href="tel:{escape(dial)}">{escape(phone)}</a>')
    county_html = ""
    if county_links:
        links = []
        for fips in county_fips(provider):
            if fips in county_links:
                label, url = county_links[fips]
                links.append(f'<a href="{escape(url)}">{escape(label)}</a>')
        if links:
            county_html = '<p class="ss-provider-meta"><strong>Local pages:</strong> ' + ", ".join(links) + "</p>"
    verified = escape(str(provider.get("date_last_verified", "")).strip())
    source_urls = [str(url).strip() for url in provider.get("source_urls", []) if str(url).strip().startswith(("http://", "https://"))]
    source_html = ""
    if source_urls and not compact:
        source_html = f'<p class="ss-provider-meta"><a href="{escape(source_urls[0])}" rel="nofollow noopener">Verification source</a>' + (f" · checked {verified}" if verified else "") + "</p>"
    elif verified:
        source_html = f'<p class="ss-provider-meta">Public information checked {verified}</p>'
    note = escape(str(provider.get("coverage_notes", "")).strip())
    note_html = f'<p class="ss-provider-meta">{note}</p>' if note and not compact else ""
    return (
        '<article class="ss-provider-card">'
        f"<h3>{name}</h3>"
        + (f'<p class="ss-provider-meta">{escape(location)}</p>' if location else "")
        + f'<div class="ss-provider-tags">{tags}</div>'
        + county_html + note_html + source_html
        + (f'<div class="ss-provider-actions">{"".join(actions)}</div>' if actions else "")
        + "</article>"
    )


def manifest_maps() -> tuple[dict[str, tuple[str, str]], dict[str, Path]]:
    data = load_json(MANIFEST_FILE)
    labels: dict[str, tuple[str, str]] = {}
    paths: dict[str, Path] = {}
    for record in data.get("records", []):
        if not isinstance(record, dict):
            continue
        fips = str(record.get("fips", "")).strip()
        url = str(record.get("page_url", "")).strip()
        state = str(record.get("state", "")).strip()
        county = str(record.get("county_or_equivalent_name", "")).strip()
        if not re.fullmatch(r"\d{5}", fips) or not url.startswith(DOMAIN + "/"):
            continue
        label = f"{county}, {state}" if county and state else county or state
        relative = url.removeprefix(DOMAIN).strip("/")
        labels[fips] = (label, "/" + relative + "/")
        paths[fips] = SITE / relative / "index.html"
    return labels, paths


def covered_counties(providers: list[dict], county_links: dict[str, tuple[str, str]]) -> set[str]:
    valid = set(county_links)
    return {fips for provider in providers for fips in county_fips(provider) if fips in valid}


def write_directory(
    providers: list[dict],
    county_links: dict[str, tuple[str, str]],
    public_directory: bool,
    coverage_count: int,
) -> None:
    out = SITE / "providers"
    out.mkdir(parents=True, exist_ok=True)
    robots = "" if public_directory else '<meta name="robots" content="noindex,follow">'
    ads_tag = ADSENSE_TAG if public_directory else ""
    title = (
        "Local Septic Pumping, Inspection & Installation Services | SepticScope"
        if public_directory else "National Septic Service Directory in Development | SepticScope"
    )
    description = (
        "Browse source-checked local septic pumping, inspection, repair, maintenance and installation businesses connected to SepticScope county guides."
        if public_directory else "The SepticScope national service directory remains private while source-reviewed provider coverage is expanded to every U.S. county and county-equivalent."
    )
    cards = "".join(provider_card(provider, county_links) for provider in providers) if public_directory else ""
    if public_directory:
        intro = f"<p>Browse <strong>{len(providers):,}</strong> source-checked local business records. Filter by the county pages and service categories shown on each listing.</p>"
        body = f'<div class="ss-provider-grid">{cards}</div>'
    else:
        percentage = min(100, round(coverage_count / EXPECTED_COUNTIES * 100, 1))
        intro = (
            "<p>The national service search is not public yet. SepticScope will launch it only after every U.S. county and county-equivalent has at least one source-reviewed local-service relationship.</p>"
        )
        body = (
            f'<div class="ss-provider-note"><strong>Coverage build in progress</strong><p><strong>{coverage_count:,}</strong> of {EXPECTED_COUNTIES:,} counties currently have at least one reviewed provider relationship.</p><div class="ss-progress" aria-label="Provider county coverage"><span style="width:{percentage}%"></span></div><p>Use the <a href="/counties/">county septic information lookup</a> for permit contacts, official sources, and local starting points while this directory is completed.</p></div>'
        )
    list_schema = {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": "Local septic service providers" if public_directory else "National septic service directory in development",
        "numberOfItems": len(providers) if public_directory else 0,
        "itemListElement": [
            {"@type": "ListItem", "position": index, "name": provider.get("business_name", ""), "url": provider.get("website") or f"{DOMAIN}/providers/"}
            for index, provider in enumerate(providers, 1)
        ] if public_directory else [],
    }
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><meta name="description" content="{escape(description)}">{robots}<link rel="canonical" href="{DOMAIN}/providers/"><style>{STYLE}</style>{GA_TAG}{ads_tag}<script type="application/ld+json">{json.dumps(list_schema, ensure_ascii=False).replace('<', '\\u003c')}</script></head><body><header style="border-bottom:1px solid var(--ss-line)"><div style="max-width:1080px;margin:auto;padding:18px 24px"><a href="/" style="font-weight:850;color:var(--ss-ink);text-decoration:none">SepticScope</a> · <a href="/counties/">County Lookup</a> · <a href="/guides/">Guides</a></div></header><main class="ss-provider-wrap" data-septicscope-provider-directory="1"><p><a href="/">Home</a> / Service directory</p><h1>{'Local septic service provider directory' if public_directory else 'National septic service directory in development'}</h1>{intro}<div class="ss-provider-note"><strong>Directory standards</strong><p>Businesses are tied to counties only when public source evidence supports the relationship. Ordinary listings are not endorsements or rankings. Current service area, licensing, registration, insurance, availability, job scope, and price must still be confirmed directly.</p></div>{body}<h2>Business corrections and listing research</h2><p>Use the <a href="/contact/">Contact &amp; Feedback page</a> to report a closure, incorrect contact information, service-area error, or a business that should be researched.</p></main><footer style="border-top:1px solid var(--ss-line)"><div style="max-width:1080px;margin:auto;padding:20px 24px;color:var(--ss-muted)">© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a> · <a href="/contact/">Contact &amp; Feedback</a></div></footer></body></html>'''
    (out / "index.html").write_text(page, encoding="utf-8")


def remove_old_sections(text: str) -> str:
    pattern = re.compile(r'<section\s+data-septicscope-provider-section="1"\b.*?</section>', flags=re.I | re.S)
    return pattern.sub("", text)


def ensure_provider_style(text: str) -> str:
    if STYLE_MARKER in text:
        return text
    fragment = f'<style {STYLE_MARKER}>{STYLE}</style>'
    if re.search(r"</head>", text, flags=re.I):
        return re.sub(r"</head>", fragment + "</head>", text, count=1, flags=re.I)
    return text


def inject_county_sections(providers: list[dict], county_paths: dict[str, Path], public_directory: bool) -> int:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for provider in providers:
        for fips in county_fips(provider):
            grouped[fips].append(provider)
    touched = 0
    for fips, path in county_paths.items():
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        cleaned = remove_old_sections(text)
        local = sorted(grouped.get(fips, []), key=lambda item: str(item.get("business_name", "")).casefold())[:12]
        if not local:
            if cleaned != text:
                path.write_text(cleaned, encoding="utf-8")
                touched += 1
            continue
        cards = "".join(provider_card(provider, compact=True) for provider in local)
        cleaned = ensure_provider_style(cleaned)
        directory_note = (
            ' <a href="/providers/">See directory standards and all listings.</a>'
            if public_directory
            else " The national search remains unpublished until every county has reviewed coverage."
        )
        section = f'''<section data-septicscope-provider-section="1" class="ss-provider-local"><h2>Source-reviewed local septic service information</h2><p>These businesses appear on this county page only when a public source supports the location or service-area relationship. Listings are not endorsements or rankings.</p><div class="ss-provider-grid">{cards}</div><div class="ss-provider-note"><strong>Before hiring:</strong> confirm the business currently serves the exact property, performs the exact work needed, and holds any license, registration, maintenance-provider authorization, or insurance required for the job.{directory_note}</div></section>'''
        marker = re.search(r"<h2[^>]*>\s*Official sources\s*</h2>", cleaned, flags=re.I)
        if marker:
            updated = cleaned[: marker.start()] + section + cleaned[marker.start() :]
        elif "</main>" in cleaned:
            updated = cleaned.replace("</main>", section + "</main>", 1)
        else:
            continue
        path.write_text(updated, encoding="utf-8")
        touched += 1
    return touched


def patch_homepage() -> None:
    home = SITE / "index.html"
    if not home.exists():
        return
    text = home.read_text(encoding="utf-8", errors="replace")
    text = re.sub(
        r'<a\b[^>]*href="/counties/indiana(?:/index\.html)?/?"[^>]*>\s*(?:Browse\s+)?Indiana(?:\s+septic)?\s+rules(?:\s*→)?\s*</a>',
        '<a href="/counties/">Browse all county septic guides →</a>',
        text,
        flags=re.I,
    )
    home.write_text(text, encoding="utf-8")


def update_sitemap(include_provider_page: bool) -> None:
    sitemap = SITE / "sitemap.xml"
    if not sitemap.exists():
        return
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    tree = ET.parse(sitemap)
    root = tree.getroot()
    target = f"{DOMAIN}/providers/"
    existing = []
    for node in list(root):
        loc = node.find(f"{{{ns}}}loc")
        if loc is not None and (loc.text or "").strip() == target:
            existing.append(node)
    if include_provider_page and not existing:
        node = ET.SubElement(root, f"{{{ns}}}url")
        ET.SubElement(node, f"{{{ns}}}loc").text = target
    if not include_provider_page:
        for node in existing:
            root.remove(node)
    tree.write(sitemap, encoding="utf-8", xml_declaration=True)


def publish_indexnow_key() -> None:
    if not INDEXNOW_KEY_FILE.exists():
        return
    key = INDEXNOW_KEY_FILE.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[A-Za-z0-9-]{8,128}", key):
        raise RuntimeError("Invalid IndexNow key format")
    (SITE / f"{key}.txt").write_text(key + "\n", encoding="utf-8")


def main() -> None:
    if not SITE.is_dir():
        raise SystemExit("site/ is missing; run python build_site.py first")
    providers = active_providers()
    county_links, county_paths = manifest_maps()
    covered = covered_counties(providers, county_links)
    public_directory = len(county_links) == EXPECTED_COUNTIES and len(covered) == EXPECTED_COUNTIES
    write_directory(providers, county_links, public_directory, len(covered))
    touched = inject_county_sections(providers, county_paths, public_directory)
    patch_homepage()
    update_sitemap(public_directory)
    publish_indexnow_key()
    print(
        f"Provider experience complete: {len(providers)} active listings across {touched} county pages; "
        f"national directory {'public' if public_directory else 'hidden'} at {len(covered)}/{EXPECTED_COUNTIES} counties"
    )


if __name__ == "__main__":
    main()
