"""Validate and publish SepticScope's neutral local septic-service directory.

Provider records are attached to counties only when a public source explicitly supports
that service area. Listings are informational, alphabetically ordered, and never imply
an endorsement, live availability, price, insurance, or current license status.
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
from urllib.parse import urlparse
import unicodedata
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
PROVIDER_FILE = ROOT / "data" / "providers.json"
DOMAIN = "https://septicscope.com"
GA_MEASUREMENT_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"
LASTMOD = date.today().isoformat()
START_MARKER = "<!-- septicscope-local-services:start -->"
END_MARKER = "<!-- septicscope-local-services:end -->"
STYLE_MARKER = "septicscope-local-services-v1"
ALLOWED_STATUSES = {"active", "closed", "uncertain", "needs_review"}
SERVICE_LABELS = {
    "septic_pumping": "Septic pumping",
    "septic_cleaning": "Tank cleaning",
    "septic_installation": "System installation",
    "septic_repair": "System repair",
    "septic_inspection": "Septic inspection",
    "septic_design": "System design / site evaluation",
    "aerobic_maintenance": "Aerobic maintenance",
    "maintenance_contracts": "Maintenance contracts",
    "drainfield_service": "Drainfield service",
    "excavation": "Excavation",
}
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


def load_counties() -> dict[str, dict]:
    data_dir = ROOT / "nationwide_data"
    payload = "".join(
        (data_dir / f"part{i:02d}.txt").read_text(encoding="utf-8").strip()
        for i in range(8)
    )
    rows = json.loads(gzip.decompress(base64.b64decode(payload, validate=True)).decode("utf-8"))
    collision_counts = Counter((abbr, slugify(name)) for abbr, name, _lsad, _fips in rows)
    result: dict[str, dict] = {}
    for abbr, name, lsad, fips in rows:
        if collision_counts[(abbr, slugify(name))] > 1 and str(lsad).lower() != "county":
            label = "Census Area" if lsad == "CA" else lsad
            if str(label).lower() not in name.lower():
                name = f"{name} {label}"
        state = STATE_NAMES[abbr]
        result[fips] = {
            "fips": fips,
            "name": display_name(name, lsad),
            "state": state,
            "abbr": abbr,
            "url": f"/counties/{slugify(state)}/{slugify(name)}/",
            "path": SITE / "counties" / slugify(state) / slugify(name) / "index.html",
        }
    if len(result) != 3144:
        raise RuntimeError(f"County FIPS map is incomplete: {len(result)}")
    return result


def valid_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def load_provider_payload(payload: dict | None = None) -> dict:
    if payload is None:
        if not PROVIDER_FILE.exists():
            raise RuntimeError(f"Provider source file is missing: {PROVIDER_FILE}")
        payload = json.loads(PROVIDER_FILE.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("providers"), list):
        raise RuntimeError("Provider data must contain a providers list")
    return payload


def validate(payload: dict, counties: dict[str, dict]) -> list[dict]:
    providers = payload.get("providers", [])
    ids: set[str] = set()
    names: set[str] = set()
    forbidden_keys = {"rating", "reviews", "review_count", "stars", "rank", "ranking"}
    errors: list[str] = []
    for index, provider in enumerate(providers):
        prefix = f"provider[{index}]"
        if not isinstance(provider, dict):
            errors.append(f"{prefix} is not an object")
            continue
        pid = str(provider.get("id", "")).strip()
        name = str(provider.get("business_name", "")).strip()
        if not pid or not name:
            errors.append(f"{prefix} must include id and business_name")
        if pid in ids:
            errors.append(f"duplicate provider id: {pid}")
        if name.casefold() in names:
            errors.append(f"duplicate provider name: {name}")
        ids.add(pid)
        names.add(name.casefold())
        status = provider.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{name or prefix} has invalid status: {status}")
        website = str(provider.get("website", ""))
        if not valid_https_url(website):
            errors.append(f"{name or prefix} requires an HTTPS website")
        source_urls = provider.get("source_urls", [])
        if not source_urls or any(not valid_https_url(str(url)) for url in source_urls):
            errors.append(f"{name or prefix} requires at least one HTTPS source URL")
        services = provider.get("service_categories", [])
        if not services or any(service not in SERVICE_LABELS for service in services):
            errors.append(f"{name or prefix} has missing or unsupported service categories")
        served = provider.get("counties_served", [])
        if not served:
            errors.append(f"{name or prefix} requires explicit county coverage")
        for item in served:
            fips = str(item.get("fips", "") if isinstance(item, dict) else item).zfill(5)
            if fips not in counties:
                errors.append(f"{name or prefix} references unknown county FIPS: {fips}")
        present_forbidden = forbidden_keys.intersection(provider)
        if present_forbidden:
            errors.append(f"{name or prefix} contains prohibited review/ranking fields: {sorted(present_forbidden)}")
        if provider.get("sponsored") not in {False, True} or provider.get("affiliate") not in {False, True}:
            errors.append(f"{name or prefix} must explicitly set sponsored and affiliate")
        if not provider.get("date_last_verified"):
            errors.append(f"{name or prefix} requires date_last_verified")
        if not provider.get("coverage_basis"):
            errors.append(f"{name or prefix} requires coverage_basis")
    if errors:
        raise RuntimeError("Provider data validation failed:\n - " + "\n - ".join(errors))
    return sorted(
        [p for p in providers if p.get("status") not in {"closed"}],
        key=lambda p: str(p.get("business_name", "")).casefold(),
    )


def service_chips(provider: dict) -> str:
    return "".join(
        f'<span class="ss-service-chip">{html.escape(SERVICE_LABELS[service])}</span>'
        for service in provider.get("service_categories", [])
    )


def credential_note(provider: dict) -> str:
    value = provider.get("license_or_registration")
    if not value:
        return ""
    if isinstance(value, dict):
        published = str(value.get("published_credentials", "")).strip()
        note = str(value.get("verification_note", "")).strip()
        combined = " ".join(part for part in (published, note) if part)
    else:
        combined = str(value).strip()
    if not combined:
        return ""
    return f'<p class="ss-provider-note"><strong>Published credential information:</strong> {html.escape(combined)}</p>'


def provider_contact(provider: dict) -> str:
    parts = []
    phone = str(provider.get("public_phone", "")).strip()
    email = str(provider.get("public_email", "")).strip()
    website = str(provider.get("website", "")).strip()
    if phone:
        tel = re.sub(r"[^0-9+]", "", phone)
        parts.append(f'<a href="tel:{html.escape(tel)}">{html.escape(phone)}</a>')
    if email:
        parts.append(f'<a href="mailto:{html.escape(email)}">Email</a>')
    parts.append(f'<a href="{html.escape(website)}" rel="nofollow external">Provider website</a>')
    return " · ".join(parts)


def provider_source(provider: dict) -> str:
    source = str(provider.get("source_urls", [provider.get("website", "")])[0])
    return f'<a href="{html.escape(source)}" rel="nofollow external">View the public service-area source</a>'


def county_provider_card(provider: dict) -> str:
    location = ", ".join(
        value for value in (
            str(provider.get("city", "")).strip(),
            str(provider.get("state", "")).strip(),
        ) if value
    )
    location_html = f'<p class="ss-provider-location">Based in {html.escape(location)}</p>' if location else ""
    note = credential_note(provider)
    return f'''<article class="ss-provider-card"><div class="ss-provider-heading"><div><h3>{html.escape(provider["business_name"])}</h3>{location_html}</div><span class="ss-source-badge">Service area sourced</span></div><div class="ss-service-chips">{service_chips(provider)}</div>{note}<p class="ss-provider-contact">{provider_contact(provider)}</p><details><summary>Why this listing appears</summary><p>{html.escape(str(provider.get("coverage_basis", "")))}</p><p>{provider_source(provider)}</p><p><small>Last source review: {html.escape(str(provider.get("date_last_verified", "")))}</small></p></details></article>'''


COUNTY_STYLE = (ROOT / "ui" / "county-services.css").read_text(encoding="utf-8")


def county_section(county: dict, providers: list[dict]) -> str:
    cards = "".join(county_provider_card(p) for p in providers)
    count = len(providers)
    return f'''{START_MARKER}<section id="local-septic-services" class="ss-local-services"><p class="ss-local-kicker">Local septic service directory</p><h2>Septic services that publish coverage for {html.escape(county["name"])}</h2><p>These {count} listing{"s" if count != 1 else ""} are connected to this county because a public source explicitly names the county or a documented local service area. Listings are alphabetized and are not rankings or endorsements.</p><div class="ss-local-disclosure"><strong>Before hiring:</strong> confirm that the business currently serves the property, performs the exact service needed, and holds any license, registration, insurance, or authorization required for the work. Get written scope and price information.</div><div class="ss-provider-stack">{cards}</div><p><a href="/providers/?county={html.escape(county["fips"])}">Browse and filter the full provider directory →</a></p></section>{END_MARKER}'''


def inject_county_sections(counties: dict[str, dict], providers: list[dict]) -> tuple[int, int]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for provider in providers:
        for item in provider.get("counties_served", []):
            fips = str(item.get("fips", "") if isinstance(item, dict) else item).zfill(5)
            grouped[fips].append(provider)

    touched = 0
    verified_touched = 0
    for fips, matched in grouped.items():
        county = counties[fips]
        path: Path = county["path"]
        if not path.exists():
            raise RuntimeError(f"Provider county page is missing: {path}")
        text = path.read_text(encoding="utf-8", errors="replace")
        text = re.sub(
            re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
            "",
            text,
            flags=re.DOTALL,
        )
        if STYLE_MARKER not in text:
            if "</head>" not in text:
                raise RuntimeError(f"County page lacks closing head: {path}")
            text = text.replace("</head>", COUNTY_STYLE + "</head>", 1)
        section = county_section(county, sorted(matched, key=lambda p: p["business_name"].casefold()))
        if "</main>" not in text:
            raise RuntimeError(f"County page lacks closing main: {path}")
        text = text.replace("</main>", section + "</main>", 1)
        path.write_text(text, encoding="utf-8")
        touched += 1
        lower = text.lower()
        if "noindex" not in lower and "official sources" in lower:
            verified_touched += 1
    return touched, verified_touched


def analytics_tags() -> str:
    return f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}');</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>'''


def directory_card(provider: dict, counties: dict[str, dict]) -> str:
    county_links = []
    fips_values = []
    for item in provider.get("counties_served", []):
        fips = str(item.get("fips", "") if isinstance(item, dict) else item).zfill(5)
        county = counties[fips]
        fips_values.append(fips)
        county_links.append(f'<a href="{county["url"]}">{html.escape(county["name"])}</a>')
    services = " ".join(provider.get("service_categories", []))
    search = " ".join([
        provider.get("business_name", ""), provider.get("city", ""), provider.get("state", ""),
        " ".join(county["name"] for county in (counties[fips] for fips in fips_values)),
        " ".join(SERVICE_LABELS[s] for s in provider.get("service_categories", [])),
    ]).lower()
    location = ", ".join(x for x in (provider.get("city", ""), provider.get("state", "")) if x)
    coverage = ", ".join(county_links)
    return f'''<article class="provider-card" data-provider-card data-search="{html.escape(search)}" data-services="{html.escape(services)}" data-counties="{html.escape(' '.join(fips_values))}"><div class="provider-heading"><div><h2>{html.escape(provider["business_name"])}</h2><p class="provider-location">{html.escape(location)}</p></div><span class="source-badge">Service area sourced</span></div><div class="service-chips">{service_chips(provider)}</div><p><strong>Published county coverage:</strong> {coverage}</p>{credential_note(provider)}<p class="provider-contact">{provider_contact(provider)}</p><details><summary>Listing source and review details</summary><p>{html.escape(str(provider.get("coverage_basis", "")))}</p><p>{provider_source(provider)}</p><p><small>Last source review: {html.escape(str(provider.get("date_last_verified", "")))}</small></p></details></article>'''


DIRECTORY_CSS = (ROOT / "ui" / "provider-directory.css").read_text(encoding="utf-8")
DIRECTORY_JS = (ROOT / "ui" / "provider-directory.js").read_text(encoding="utf-8")


def write_provider_directory(provider_data: dict | None = None) -> None:
    counties = load_counties()
    payload = load_provider_payload(provider_data)
    providers = validate(payload, counties)
    out = SITE / "providers"
    out.mkdir(parents=True, exist_ok=True)
    noindex = '<meta name="robots" content="noindex,follow">' if not providers else ""
    cards = "".join(directory_card(provider, counties) for provider in providers)
    options = "".join(
        f'<option value="{html.escape(key)}">{html.escape(label)}</option>'
        for key, label in SERVICE_LABELS.items()
        if any(key in provider.get("service_categories", []) for provider in providers)
    )
    page = (ROOT / "ui" / "provider-directory.html").read_text(encoding="utf-8")
    replacements = {
        "@@NOINDEX@@": noindex,
        "@@CSS@@": DIRECTORY_CSS,
        "@@TAGS@@": analytics_tags() if providers else analytics_tags().replace(f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>', ""),
        "@@COUNT@@": f"{len(providers):,}",
        "@@OPTIONS@@": options,
        "@@CARDS@@": cards if cards else '<div class="empty">Local provider records are being source-checked before publication.</div>',
        "@@JS@@": DIRECTORY_JS,
    }
    for key, value in replacements.items():
        page = page.replace(key, value)
    (out / "index.html").write_text(page, encoding="utf-8")
    ensure_provider_sitemap(bool(providers))


def ensure_provider_sitemap(indexable: bool) -> None:
    sitemap = SITE / "sitemap.xml"
    if not sitemap.exists():
        return
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    tree = ET.parse(sitemap)
    root = tree.getroot()
    target = f"{DOMAIN}/providers/"
    nodes = []
    for node in root.findall(f"{{{ns}}}url"):
        loc = node.find(f"{{{ns}}}loc")
        if loc is not None and (loc.text or "").strip() == target:
            nodes.append(node)
    if indexable and not nodes:
        node = ET.SubElement(root, f"{{{ns}}}url")
        ET.SubElement(node, f"{{{ns}}}loc").text = target
        ET.SubElement(node, f"{{{ns}}}lastmod").text = LASTMOD
    elif not indexable:
        for node in nodes:
            root.remove(node)
    tree.write(sitemap, encoding="utf-8", xml_declaration=True)


def apply() -> None:
    if not SITE.is_dir():
        raise RuntimeError("Generated site directory is missing")
    counties = load_counties()
    payload = load_provider_payload()
    providers = validate(payload, counties)
    touched, verified_touched = inject_county_sections(counties, providers)
    write_provider_directory(payload)
    print(
        "Local service directory complete: "
        f"{len(providers)} source-checked listings across {touched} counties; "
        f"{verified_touched} verified county guides enriched"
    )


if __name__ == "__main__":
    apply()
