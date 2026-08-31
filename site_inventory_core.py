"""Generate SepticScope's national coverage, keyword, source, and quality manifests.

The generator inspects the final static output after all county expansions, guides,
trust pages, and advertising safeguards have run. It never upgrades a county to
"verified" based on existence alone: a verified county page must be indexable and
contain both a permitting-authority section and visible official sources.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
import gzip
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DATA_DIR = ROOT / "nationwide_data"
SOURCE_DATA_DIR = ROOT / "data"
OUTPUT_DATA_DIR = SITE / "data"
DOMAIN = "https://septicscope.com"
EXPECTED_COUNTY_EQUIVALENTS = 3144
DEFAULT_MINIMUM_VERIFIED = 429
TODAY = date.today()
GENERATED_AT = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut",
    "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida",
    "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois",
    "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky",
    "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
    "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire",
    "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
    "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming",
}

GUIDE_KEYWORDS = {
    "septic-drainfield-repair-replacement": "septic drainfield repair or replacement",
    "septic-tank-size-calculator": "septic tank size calculator",
    "septic-maintenance-checklist": "septic maintenance checklist",
    "types-of-septic-systems": "types of septic systems",
    "septic-system-winter-care": "winter septic system care",
    "septic-inspection-checklist": "septic inspection checklist",
    "septic-system-lifespan": "septic system lifespan",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.h1_parts: list[str] = []
        self.h2_values: list[str] = []
        self.description = ""
        self.robots = ""
        self.canonical = ""
        self.lang = ""
        self.has_viewport = False
        self.anchors: list[tuple[str, str]] = []
        self._capture: str | None = None
        self._buffer: list[str] = []
        self._anchor_href: str | None = None
        self._anchor_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr = {str(k).lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = attr.get("lang", "")
        elif tag in {"title", "h1", "h2"}:
            self._capture = tag
            self._buffer = []
        elif tag == "meta":
            name = attr.get("name", "").lower()
            if name == "description":
                self.description = attr.get("content", "").strip()
            elif name == "robots":
                self.robots = attr.get("content", "").strip()
            elif name == "viewport":
                self.has_viewport = True
        elif tag == "link" and "canonical" in attr.get("rel", "").lower():
            self.canonical = attr.get("href", "").strip()
        elif tag == "a":
            self._anchor_href = attr.get("href", "").strip()
            self._anchor_text = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buffer.append(data)
        if self._anchor_href is not None:
            self._anchor_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._capture == tag:
            value = clean_text(" ".join(self._buffer))
            if tag == "title":
                self.title_parts.append(value)
            elif tag == "h1":
                self.h1_parts.append(value)
            elif tag == "h2":
                self.h2_values.append(value)
            self._capture = None
            self._buffer = []
        if tag == "a" and self._anchor_href is not None:
            self.anchors.append((self._anchor_href, clean_text(" ".join(self._anchor_text))))
            self._anchor_href = None
            self._anchor_text = []


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower().replace("&", " and ")).strip("-")


def display_name(name: str, lsad: str) -> str:
    if not lsad:
        return name
    label = "Census Area" if lsad == "CA" else lsad
    return name if label.lower() in name.lower() else f"{name} {label}"


def load_county_rows() -> list[list[str]]:
    payload = "".join(
        (DATA_DIR / f"part{i:02d}.txt").read_text(encoding="utf-8").strip()
        for i in range(8)
    )
    rows = json.loads(gzip.decompress(base64.b64decode(payload, validate=True)).decode("utf-8"))
    if len(rows) != EXPECTED_COUNTY_EQUIVALENTS or len({row[3] for row in rows}) != len(rows):
        raise RuntimeError(f"Nationwide county dataset integrity failure: {len(rows)} rows")
    return rows


def page_url(path: Path) -> str:
    relative = path.relative_to(SITE).as_posix()
    if relative == "index.html":
        return f"{DOMAIN}/"
    if relative.endswith("/index.html"):
        return f"{DOMAIN}/{relative[:-10]}"
    return f"{DOMAIN}/{relative}"


def parse_page(path: Path) -> tuple[PageParser, str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    parser = PageParser()
    parser.feed(raw)
    return parser, raw


def is_noindex(parser: PageParser) -> bool:
    return "noindex" in parser.robots.lower()


def visible_review_date(raw: str) -> str | None:
    patterns = (
        r"Official sources checked\s+([^<\n]+)",
        r"Last reviewed(?:\s*:)?\s+([^<\n]+)",
        r"Sources reviewed(?:\s*:)?\s+([^<\n]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, raw, flags=re.IGNORECASE)
        if not match:
            continue
        candidate = clean_text(match.group(1)).strip(" .")
        for fmt in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(candidate, fmt).date().isoformat()
            except ValueError:
                pass
        return candidate
    return None


def authority_from_page(raw: str) -> str:
    match = re.search(
        r"<h2[^>]*>\s*Permitting authority\s*</h2>\s*<p[^>]*>\s*<strong[^>]*>(.*?)</strong>",
        raw,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return ""
    return clean_text(re.sub(r"<[^>]+>", " ", match.group(1)))


def official_status(title: str, url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    lower_title = title.lower()
    if host.endswith(".gov") or host.endswith(".us") or ".gov." in host:
        return "official_government_domain"
    if any(term in lower_title for term in (
        "health department", "public health", "health district",
        "environmental health", "extension", "university",
    )):
        return "reviewed_public_agency_or_institution"
    return "reviewed_source"


def extract_sources(raw: str, parser: PageParser, reviewed: str | None) -> list[dict[str, Any]]:
    lower = raw.lower()
    marker = lower.rfind("official sources")
    source_parser = parser
    if marker >= 0:
        source_parser = PageParser()
        source_parser.feed(raw[marker:])
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for href, label in source_parser.anchors:
        if not href.startswith(("http://", "https://")):
            continue
        host = (urlparse(href).hostname or "").lower()
        if not host or host.endswith("septicscope.com"):
            continue
        if "googletagmanager.com" in host or "googlesyndication.com" in host:
            continue
        normalized = href.strip()
        if normalized in seen:
            continue
        seen.add(normalized)
        title = label or host
        status = official_status(title, normalized)
        result.append({
            "source_title": title,
            "publishing_organization": host.removeprefix("www."),
            "url": normalized,
            "date_accessed": reviewed or TODAY.isoformat(),
            "information_supported": "County septic permitting, regulatory, contact, form, or maintenance information",
            "official_status": status,
            "is_official": status != "reviewed_source",
            "last_successful_link_check": None,
        })
    return result


def expected_canonical(path: Path) -> str:
    return page_url(path)


def classify_page(path: Path) -> tuple[str, str, str]:
    parts = path.relative_to(SITE).parts
    state = ""
    county = ""
    if parts == ("index.html",):
        return "homepage", state, county
    if parts == ("404.html",):
        return "error_page", state, county
    if len(parts) == 3 and parts[0] == "counties" and parts[-1] == "index.html":
        return "state_hub", parts[1], county
    if len(parts) == 4 and parts[0] == "counties" and parts[-1] == "index.html":
        return "county_page", parts[1], parts[2]
    if parts == ("counties", "index.html"):
        return "county_directory", state, county
    if parts == ("guides", "index.html"):
        return "guide_hub", state, county
    if len(parts) == 3 and parts[0] == "guides" and parts[-1] == "index.html":
        return "guide", state, parts[1]
    if parts == ("faq", "index.html"):
        return "faq_hub", state, county
    if len(parts) == 3 and parts[0] == "faq" and parts[-1] == "index.html":
        return "faq_article", state, parts[1]
    if len(parts) == 2 and parts[-1] == "index.html":
        return parts[0].replace("-", "_"), state, county
    return "other", state, county


def choose_keyword(
    page_type: str,
    url: str,
    title: str,
    h1: str,
    state_name: str = "",
    county_name: str = "",
    slug: str = "",
) -> tuple[str, list[str], str]:
    if page_type == "county_page" and state_name and county_name:
        primary = f"septic permit {county_name} {state_name}"
        secondary = [
            f"septic system requirements {county_name} {state_name}",
            f"septic regulations {county_name} {state_name}",
        ]
        return primary, secondary, "Find local septic permitting authority, requirements, forms, and official sources"
    if page_type == "state_hub" and state_name:
        return (
            f"{state_name} septic permits by county",
            [f"{state_name} septic regulations", f"{state_name} county septic requirements"],
            "Browse county-specific septic guidance within a state",
        )
    if page_type == "county_directory":
        return (
            "county septic permit lookup",
            ["septic requirements by county", "local septic permitting authority"],
            "Find the correct county or county-equivalent septic guide",
        )
    if page_type == "homepage":
        return (
            "county septic permit requirements",
            ["local septic regulations", "septic permit lookup"],
            "Find local septic rules and practical homeowner guidance",
        )
    if page_type == "guide_hub":
        return (
            "septic system homeowner guides",
            ["septic maintenance guides", "septic system information"],
            "Browse in-depth septic system guidance",
        )
    if page_type == "guide":
        primary = GUIDE_KEYWORDS.get(slug, clean_text(h1 or title.split("|")[0]))
        return (
            primary,
            [f"{primary} guide", f"{primary} for homeowners"],
            "Learn, compare, calculate, inspect, maintain, or troubleshoot a septic system",
        )
    if page_type == "faq_hub":
        return (
            "septic system frequently asked questions",
            ["septic questions and answers", "septic homeowner FAQ"],
            "Get concise answers to common septic questions",
        )
    if page_type == "faq_article":
        primary = clean_text(h1 or title.split("|")[0])
        return (
            primary,
            [f"{primary} septic answer"],
            "Answer one specific septic-system question",
        )
    if page_type == "privacy":
        return "SepticScope privacy policy", [], "Review privacy and advertising disclosures"
    if page_type in {"contact", "corrections"}:
        return "contact SepticScope", ["report septic information correction"], "Send feedback or a correction"
    if page_type == "about":
        return "about SepticScope", ["how SepticScope verifies septic information"], "Understand the publisher and sourcing process"
    if page_type in {"sources", "guides_sources"}:
        return "SepticScope official sources", [], "Review sourcing standards and references"
    if page_type == "error_page":
        return "", [], "Error recovery"
    base = clean_text(h1 or title.split("|")[0])
    return (base, [f"{base} SepticScope"] if base else [], "Navigate or obtain site information")


def load_provider_data() -> dict[str, Any]:
    provider_file = SOURCE_DATA_DIR / "providers.json"
    if not provider_file.exists():
        return {
            "schema_version": 1,
            "last_updated": TODAY.isoformat(),
            "ordering_policy": "Ordinary listings use neutral ordering; sponsored placement must be clearly labeled.",
            "providers": [],
        }
    data = json.loads(provider_file.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("providers"), list):
        raise RuntimeError("data/providers.json must be an object with a providers array")
    return data


def provider_counts_by_fips(provider_data: dict[str, Any]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for provider in provider_data.get("providers", []):
        if str(provider.get("status", "active")).lower() == "closed":
            continue
        for county in provider.get("counties_served", []):
            if isinstance(county, dict):
                fips = str(county.get("fips", "")).strip()
            else:
                fips = str(county).strip()
            if fips:
                counts[fips] += 1
    return counts


def write_provider_landing(provider_data: dict[str, Any]) -> None:
    providers = provider_data.get("providers", [])
    out = SITE / "providers"
    out.mkdir(parents=True, exist_ok=True)
    robots = "" if providers else '<meta name="robots" content="noindex,follow">'
    status = (
        f"<p>SepticScope currently has <strong>{len(providers)}</strong> verified provider records. "
        "Use county pages and ZIP search as directory coverage is published.</p>"
        if providers
        else "<p>The verified local provider directory is being assembled. No business is listed until its public contact information and service area have been checked.</p>"
    )
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Local Septic Service Provider Directory | SepticScope</title><meta name="description" content="Find verified septic pumping, inspection, repair, installation and related onsite-wastewater providers by county and ZIP code as SepticScope directory coverage grows.">{robots}
<link rel="canonical" href="{DOMAIN}/providers/"><style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.65}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:1000px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}main{{padding-top:42px;padding-bottom:70px}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}}a{{color:var(--accent)}}.card{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}footer{{border-top:1px solid var(--line);color:var(--muted)}}</style></head><body>
<header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><p><a href="/">Home</a> / Provider directory</p><h1>Local septic service provider directory</h1>{status}
<div class="card"><h2>Directory standards</h2><p>Listings must use verifiable public business information. Ordinary listings are not endorsements, use neutral ordering, and do not include copied reviews or unmaintainable ratings. Paid placement will be labeled and paid links will use the appropriate sponsored relationship attribute.</p></div>
<h2>Business corrections and listing requests</h2><p>Business owners and users can <a href="/contact/">report a closed business, incorrect contact information, service-area error, or request review of a listing</a>.</p>
<p>For immediate service, consult the official permitting authority on your <a href="/counties/">county septic guide</a> and independently verify a contractor's current license, registration, insurance and service area where applicable.</p></main>
<footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a> · <a href="/contact/">Contact &amp; Feedback</a></div></footer></body></html>'''
    (out / "index.html").write_text(page, encoding="utf-8")


def source_catalog_from_manifest(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    catalog: dict[str, dict[str, Any]] = {}
    for record in records:
        for source in record.get("official_sources", []):
            url = source["url"]
            item = catalog.setdefault(url, {
                **source,
                "states": [],
                "county_fips": [],
            })
            if record["state"] not in item["states"]:
                item["states"].append(record["state"])
            if record["fips"] not in item["county_fips"]:
                item["county_fips"].append(record["fips"])
    for item in catalog.values():
        item["states"].sort()
        item["county_fips"].sort()
    return sorted(catalog.values(), key=lambda item: item["url"])


def repository_legacy_scan() -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    allowed_suffixes = {".py", ".md", ".json", ".yml", ".yaml", ".html", ".xml", ".txt", ".js", ".css"}
    excluded_roots = {".git", ".septicscope-build", "site", "__pycache__"}
    pattern = re.compile(r"onsiteatlas", re.IGNORECASE)
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in allowed_suffixes:
            continue
        relative_parts = path.relative_to(ROOT).parts
        if any(part in excluded_roots for part in relative_parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        count = len(pattern.findall(text))
        if count:
            findings.append({"path": path.relative_to(ROOT).as_posix(), "occurrences": count})
    return findings


def duplicate_groups(pages: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    display: dict[str, str] = {}
    for page in pages:
        if page["indexability_status"] != "indexable":
            continue
        value = clean_text(str(page.get(field, "")))
        if not value:
            continue
        key = value.casefold()
        grouped[key].append(page["url"])
        display[key] = value
    return [
        {"value": display[key], "urls": urls}
        for key, urls in sorted(grouped.items())
        if len(urls) > 1
    ]


def replace_home_metric(text: str, value: int, label: str) -> tuple[str, bool]:
    escaped_label = re.escape(label)
    patterns = (
        re.compile(rf"(?is)(>\s*)\d+(\s*</[^>]+>\s*<[^>]+>\s*{escaped_label}\b)"),
        re.compile(rf"(?is)(>\s*)\d+(\s*<[^>]*>\s*{escaped_label}\b)"),
    )
    for pattern in patterns:
        updated, count = pattern.subn(lambda match: f"{match.group(1)}{value}{match.group(2)}", text, count=1)
        if count:
            return updated, True
    return text, False


def update_home_metrics(verified_count: int, faq_count: int, guide_count: int) -> None:
    home = SITE / "index.html"
    if not home.exists():
        return
    text = home.read_text(encoding="utf-8", errors="replace")
    text, _ = replace_home_metric(text, verified_count, "verified county guides")
    text, _ = replace_home_metric(text, faq_count, "FAQ articles")
    text, guide_changed = replace_home_metric(text, guide_count, "cornerstone guides")
    if not guide_changed:
        text, _ = replace_home_metric(text, guide_count, "septic guides")
    text = re.sub(r"(?i)\bcornerstone guides\b", "septic guides", text)
    home.write_text(text, encoding="utf-8")


def generate() -> dict[str, Any]:
    if not SITE.is_dir():
        raise RuntimeError("site/ does not exist; run python build_site.py first")
    OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)

    provider_data = load_provider_data()
    write_provider_landing(provider_data)
    provider_counts = provider_counts_by_fips(provider_data)

    county_rows = load_county_rows()
    county_manifest: list[dict[str, Any]] = []
    state_stats: dict[str, dict[str, Any]] = {}
    county_lookup_by_url: dict[str, tuple[str, str]] = {}
    source_review_warning_count = 0

    for abbr, name, lsad, fips in county_rows:
        state = STATE_NAMES[abbr]
        state_slug = slugify(state)
        county_slug = slugify(name)
        county_display = display_name(name, lsad)
        path = SITE / "counties" / state_slug / county_slug / "index.html"
        url = f"{DOMAIN}/counties/{state_slug}/{county_slug}/"
        warnings: list[str] = []
        broken_source_warnings: list[str] = []

        if path.exists():
            parser, raw = parse_page(path)
            noindex = is_noindex(parser)
            verified = (
                not noindex
                and "official sources" in raw.lower()
                and "permitting authority" in raw.lower()
            )
            reviewed = visible_review_date(raw)
            authority = authority_from_page(raw) if verified else ""
            sources = extract_sources(raw, parser, reviewed) if verified else []
            if verified and not reviewed:
                warnings.append("missing_visible_review_date")
            if verified and not authority:
                warnings.append("missing_parsed_permitting_authority")
            if verified and not sources:
                warnings.append("missing_parsed_official_source")
            if parser.canonical != url:
                warnings.append("canonical_mismatch")
            if not parser.title_parts:
                warnings.append("missing_title")
            if not parser.h1_parts:
                warnings.append("missing_h1")
            if not parser.description:
                warnings.append("missing_meta_description")
            if not parser.lang:
                warnings.append("missing_html_lang")
            if not parser.has_viewport:
                warnings.append("missing_viewport")
        else:
            parser = PageParser()
            raw = ""
            noindex = True
            verified = False
            reviewed = None
            authority = ""
            sources = []
            warnings.append("missing_published_page")

        if verified:
            coverage_status = "verified_county_guide"
            research_status = "source_verified"
            verification_status = "verified"
            publication_status = "deployed_indexable"
        elif path.exists():
            coverage_status = "official_help_page"
            research_status = "not_started_or_in_progress"
            verification_status = "unverified"
            publication_status = "deployed_noindex" if noindex else "deployed_indexable_unverified"
            if not noindex:
                warnings.append("unverified_county_page_is_indexable")
        else:
            coverage_status = "missing"
            research_status = "not_started"
            verification_status = "unverified"
            publication_status = "not_deployed"

        if "missing_visible_review_date" in warnings:
            source_review_warning_count += 1

        primary_keyword = f"septic permit {county_display} {state}"
        record = {
            "state": state,
            "state_abbreviation": abbr,
            "county_or_equivalent_name": county_display,
            "source_name": name,
            "legal_statistical_area_description": lsad,
            "fips": str(fips),
            "canonical_slug": county_slug,
            "page_url": url,
            "coverage_status": coverage_status,
            "research_status": research_status,
            "verification_status": verification_status,
            "publication_status": publication_status,
            "official_regulating_authority": authority,
            "primary_official_source": sources[0] if sources else None,
            "official_sources": sources,
            "date_researched": reviewed,
            "date_last_reviewed": reviewed,
            "primary_keyword": primary_keyword,
            "secondary_keywords": [
                f"septic system requirements {county_display} {state}",
                f"septic regulations {county_display} {state}",
            ],
            "local_service_provider_count": provider_counts[str(fips)],
            "zip_codes": [],
            "content_quality_warnings": warnings,
            "broken_source_warnings": broken_source_warnings,
            "next_review_date": (
                (datetime.fromisoformat(reviewed).date() + timedelta(days=180)).isoformat()
                if reviewed and re.fullmatch(r"\d{4}-\d{2}-\d{2}", reviewed)
                else None
            ),
        }
        county_manifest.append(record)
        county_lookup_by_url[url] = (state, county_display)

        stats = state_stats.setdefault(state, {
            "state": state,
            "state_abbreviation": abbr,
            "total_county_equivalents": 0,
            "verified_county_guides": 0,
            "in_progress_help_pages": 0,
            "missing_pages": 0,
        })
        stats["total_county_equivalents"] += 1
        if verified:
            stats["verified_county_guides"] += 1
        elif path.exists():
            stats["in_progress_help_pages"] += 1
        else:
            stats["missing_pages"] += 1

    for stats in state_stats.values():
        verified = stats["verified_county_guides"]
        total = stats["total_county_equivalents"]
        if verified == total:
            stats["coverage_status"] = "complete"
        elif verified:
            stats["coverage_status"] = "partial"
        else:
            stats["coverage_status"] = "not_started"

    verified_count = sum(record["verification_status"] == "verified" for record in county_manifest)
    faq_count = len(list((SITE / "faq").glob("*/index.html"))) if (SITE / "faq").is_dir() else 0
    guide_count = len(list((SITE / "guides").glob("*/index.html"))) if (SITE / "guides").is_dir() else 0
    update_home_metrics(verified_count, faq_count, guide_count)

    html_pages = sorted(SITE.rglob("*.html"))
    keyword_pages: list[dict[str, Any]] = []
    canonical_errors: list[dict[str, str]] = []
    accessibility_warnings: list[dict[str, str]] = []
    canonical_domain_conflicts: list[dict[str, str]] = []

    state_by_slug = {slugify(name): name for name in STATE_NAMES.values()}
    for path in html_pages:
        parser, raw = parse_page(path)
        url = page_url(path)
        page_type, state_slug, leaf_slug = classify_page(path)
        title = parser.title_parts[0] if parser.title_parts else ""
        h1 = parser.h1_parts[0] if parser.h1_parts else ""
        indexable = not is_noindex(parser) and page_type != "error_page"
        state_name = state_by_slug.get(state_slug, "")
        county_name = county_lookup_by_url.get(url, ("", ""))[1]
        primary, secondary, intent = choose_keyword(
            page_type, url, title, h1, state_name, county_name, leaf_slug
        )
        if not indexable:
            primary_for_map = primary
        else:
            primary_for_map = primary.strip()

        expected = expected_canonical(path)
        if indexable and parser.canonical != expected:
            canonical_errors.append({
                "url": url,
                "expected": expected,
                "actual": parser.canonical,
            })
        if indexable and parser.canonical and not parser.canonical.startswith(DOMAIN):
            canonical_domain_conflicts.append({"url": url, "canonical": parser.canonical})
        if not parser.lang:
            accessibility_warnings.append({"url": url, "issue": "missing_html_lang"})
        if not parser.has_viewport:
            accessibility_warnings.append({"url": url, "issue": "missing_viewport"})
        if not h1 and page_type != "error_page":
            accessibility_warnings.append({"url": url, "issue": "missing_h1"})

        keyword_pages.append({
            "url": url,
            "page_type": page_type,
            "state": state_name,
            "county": county_name,
            "primary_keyword": primary_for_map,
            "secondary_keywords": secondary,
            "search_intent": intent,
            "current_title": title,
            "current_h1": h1,
            "meta_description": parser.description,
            "competing_internal_pages": [],
            "indexability_status": "indexable" if indexable else "noindex",
            "date_reviewed": TODAY.isoformat(),
        })

    keyword_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for page in keyword_pages:
        if page["indexability_status"] == "indexable" and page["primary_keyword"]:
            keyword_groups[page["primary_keyword"].casefold()].append(page)
    for group in keyword_groups.values():
        urls = [page["url"] for page in group]
        if len(urls) > 1:
            for page in group:
                page["competing_internal_pages"] = [url for url in urls if url != page["url"]]

    title_duplicates = duplicate_groups(keyword_pages, "current_title")
    h1_duplicates = duplicate_groups(keyword_pages, "current_h1")
    meta_duplicates = duplicate_groups(keyword_pages, "meta_description")
    missing_primary_keywords = [
        page["url"] for page in keyword_pages
        if page["indexability_status"] == "indexable" and not page["primary_keyword"]
    ]
    keyword_cannibalization = [
        {"primary_keyword": group[0]["primary_keyword"], "urls": [page["url"] for page in group]}
        for group in keyword_groups.values()
        if len(group) > 1
    ]

    legacy_findings = repository_legacy_scan()
    generated_legacy_findings = []
    legacy_pattern = re.compile(r"onsiteatlas", re.IGNORECASE)
    for path in html_pages:
        text = path.read_text(encoding="utf-8", errors="ignore")
        count = len(legacy_pattern.findall(text))
        if count:
            generated_legacy_findings.append({
                "path": path.relative_to(SITE).as_posix(),
                "occurrences": count,
            })

    source_catalog = source_catalog_from_manifest(county_manifest)
    completed_states = sum(stats["coverage_status"] == "complete" for stats in state_stats.values())
    partial_states = sum(stats["coverage_status"] == "partial" for stats in state_stats.values())
    not_started_states = sum(stats["coverage_status"] == "not_started" for stats in state_stats.values())
    missing_county_pages = sum(record["publication_status"] == "not_deployed" for record in county_manifest)
    county_pages_with_sources = sum(bool(record["official_sources"]) for record in county_manifest)

    baseline_file = SOURCE_DATA_DIR / "quality-baseline.json"
    baseline = {
        "expected_county_equivalents": EXPECTED_COUNTY_EQUIVALENTS,
        "minimum_verified_counties": DEFAULT_MINIMUM_VERIFIED,
    }
    if baseline_file.exists():
        baseline.update(json.loads(baseline_file.read_text(encoding="utf-8")))

    hard_errors: list[str] = []
    if len(county_manifest) != int(baseline["expected_county_equivalents"]):
        hard_errors.append("county_manifest_count_mismatch")
    if missing_county_pages:
        hard_errors.append("missing_county_equivalent_pages")
    if verified_count < int(baseline["minimum_verified_counties"]):
        hard_errors.append("verified_county_regression")
    if missing_primary_keywords:
        hard_errors.append("indexable_pages_missing_primary_keywords")
    if canonical_errors:
        hard_errors.append("canonical_errors")
    if canonical_domain_conflicts:
        hard_errors.append("canonical_domain_conflicts")
    if legacy_findings or generated_legacy_findings:
        hard_errors.append("legacy_onsiteatlas_branding")
    if title_duplicates:
        hard_errors.append("duplicate_indexable_titles")
    if meta_duplicates:
        hard_errors.append("duplicate_indexable_meta_descriptions")

    commit_sha = (
        os.environ.get("CF_PAGES_COMMIT_SHA")
        or os.environ.get("GITHUB_SHA")
        or os.environ.get("COMMIT_SHA")
        or "unknown"
    )
    summary = {
        "schema_version": 1,
        "generated_at": GENERATED_AT,
        "repository_commit": commit_sha,
        "production_branch": "main",
        "canonical_domain": DOMAIN,
        "counts": {
            "html_pages": len(html_pages),
            "indexable_html_pages": sum(
                page["indexability_status"] == "indexable" for page in keyword_pages
            ),
            "published_county_or_equivalent_pages": len(county_manifest) - missing_county_pages,
            "verified_county_guides": verified_count,
            "in_progress_county_help_pages": sum(
                record["coverage_status"] == "official_help_page" for record in county_manifest
            ),
            "missing_county_equivalent_pages": missing_county_pages,
            "completed_states_and_dc": completed_states,
            "partially_completed_states": partial_states,
            "states_without_verified_guides": not_started_states,
            "county_guides_with_parsed_official_sources": county_pages_with_sources,
            "verified_guides_missing_visible_review_date": source_review_warning_count,
            "faq_articles": faq_count,
            "guide_articles_and_tools": guide_count,
            "provider_listings": len(provider_data.get("providers", [])),
            "pages_with_primary_keywords": sum(
                page["indexability_status"] == "indexable" and bool(page["primary_keyword"])
                for page in keyword_pages
            ),
            "pages_without_primary_keywords": len(missing_primary_keywords),
            "duplicate_title_groups": len(title_duplicates),
            "duplicate_h1_groups": len(h1_duplicates),
            "duplicate_meta_description_groups": len(meta_duplicates),
            "keyword_cannibalization_groups": len(keyword_cannibalization),
            "canonical_errors": len(canonical_errors),
            "canonical_domain_conflicts": len(canonical_domain_conflicts),
            "accessibility_warnings": len(accessibility_warnings),
            "legacy_brand_occurrences": sum(item["occurrences"] for item in legacy_findings)
            + sum(item["occurrences"] for item in generated_legacy_findings),
        },
        "states": sorted(state_stats.values(), key=lambda item: item["state"]),
        "quality_findings": {
            "hard_errors": hard_errors,
            "duplicate_titles": title_duplicates,
            "duplicate_h1s": h1_duplicates,
            "duplicate_meta_descriptions": meta_duplicates,
            "keyword_cannibalization": keyword_cannibalization,
            "canonical_errors": canonical_errors,
            "canonical_domain_conflicts": canonical_domain_conflicts,
            "accessibility_warnings": accessibility_warnings,
            "repository_legacy_branding": legacy_findings,
            "generated_legacy_branding": generated_legacy_findings,
        },
        "known_limitations": [
            "ZIP-to-county many-to-many mapping is not yet populated; county manifests retain an empty zip_codes field until a licensed or public authoritative mapping is integrated.",
            "Provider directory infrastructure is present, but only verified public provider records may be added.",
            "Automated link checks can be blocked or rate-limited by government sites; a blocked response is not treated as proof that a source is broken.",
        ],
    }

    coverage_payload = {
        "schema_version": 1,
        "generated_at": GENERATED_AT,
        "record_count": len(county_manifest),
        "records": county_manifest,
    }
    keyword_payload = {
        "schema_version": 1,
        "generated_at": GENERATED_AT,
        "record_count": len(keyword_pages),
        "records": keyword_pages,
    }
    source_payload = {
        "schema_version": 1,
        "generated_at": GENERATED_AT,
        "record_count": len(source_catalog),
        "records": source_catalog,
    }

    (OUTPUT_DATA_DIR / "national-coverage-manifest.json").write_text(
        json.dumps(coverage_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DATA_DIR / "keyword-map.json").write_text(
        json.dumps(keyword_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DATA_DIR / "source-catalog.json").write_text(
        json.dumps(source_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DATA_DIR / "provider-directory.json").write_text(
        json.dumps(provider_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DATA_DIR / "project-audit-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    counts = summary["counts"]
    text_summary = "\n".join([
        "SepticScope national project audit",
        f"Generated: {GENERATED_AT}",
        f"Commit: {commit_sha}",
        f"HTML pages: {counts['html_pages']}",
        f"Published county/county-equivalent pages: {counts['published_county_or_equivalent_pages']}",
        f"Verified county guides: {counts['verified_county_guides']}",
        f"In-progress county help pages: {counts['in_progress_county_help_pages']}",
        f"Completed states/DC: {counts['completed_states_and_dc']}",
        f"Partially completed states: {counts['partially_completed_states']}",
        f"States without a verified guide: {counts['states_without_verified_guides']}",
        f"Guide articles/tools: {counts['guide_articles_and_tools']}",
        f"FAQ articles: {counts['faq_articles']}",
        f"Provider listings: {counts['provider_listings']}",
        f"Indexable pages missing primary keywords: {counts['pages_without_primary_keywords']}",
        f"Canonical errors: {counts['canonical_errors']}",
        f"Duplicate title groups: {counts['duplicate_title_groups']}",
        f"Duplicate H1 groups: {counts['duplicate_h1_groups']}",
        f"Duplicate meta-description groups: {counts['duplicate_meta_description_groups']}",
        f"Legacy OnsiteAtlas occurrences: {counts['legacy_brand_occurrences']}",
        "Hard errors: " + (", ".join(hard_errors) if hard_errors else "none"),
        "",
    ])
    (OUTPUT_DATA_DIR / "project-audit-summary.txt").write_text(text_summary, encoding="utf-8")

    build_info = {
        "site": "SepticScope",
        "canonical_domain": DOMAIN,
        "production_branch": "main",
        "commit_sha": commit_sha,
        "generated_at": GENERATED_AT,
        "verified_county_guides": verified_count,
        "published_county_or_equivalent_pages": len(county_manifest) - missing_county_pages,
        "guide_articles_and_tools": guide_count,
        "faq_articles": faq_count,
        "provider_listings": len(provider_data.get("providers", [])),
        "quality_gate": "pass" if not hard_errors else "fail",
    }
    (SITE / "build-info.json").write_text(
        json.dumps(build_info, indent=2) + "\n",
        encoding="utf-8",
    )
    print(text_summary, end="")
    return summary


def check() -> None:
    summary_file = OUTPUT_DATA_DIR / "project-audit-summary.json"
    required = (
        OUTPUT_DATA_DIR / "national-coverage-manifest.json",
        OUTPUT_DATA_DIR / "keyword-map.json",
        OUTPUT_DATA_DIR / "source-catalog.json",
        OUTPUT_DATA_DIR / "provider-directory.json",
        summary_file,
        OUTPUT_DATA_DIR / "project-audit-summary.txt",
        SITE / "build-info.json",
    )
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.exists()]
    if missing:
        raise SystemExit("Missing generated inventory files: " + ", ".join(missing))
    summary = json.loads(summary_file.read_text(encoding="utf-8"))
    counts = summary["counts"]
    print(
        "Inventory check: "
        f"{counts['verified_county_guides']} verified counties; "
        f"{counts['published_county_or_equivalent_pages']} published county/equivalent pages; "
        f"{counts['pages_without_primary_keywords']} indexable pages without keywords; "
        f"{counts['canonical_errors']} canonical errors"
    )
    errors = summary.get("quality_findings", {}).get("hard_errors", [])
    if errors:
        raise SystemExit("Project inventory quality gate failed: " + ", ".join(errors))
    print("PASS: national coverage, keyword, canonical, branding, and metadata quality gate")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate an existing generated inventory")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        generate()


if __name__ == "__main__":
    main()
