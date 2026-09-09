#!/usr/bin/env python3
"""Quality-first recovery for search visibility and AdSense review.

This pass deliberately reduces the public/indexable footprint. It keeps only county
pages that contain substantial, locally differentiated information; consolidates FAQ
answers; removes ads from navigation, trust, noindex, and withheld pages; and prevents
statewide templates or unfinished pages from being presented as finished local content.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import quote_plus, urlparse
import xml.etree.ElementTree as ET

import county_lookup_experience as county_lookup

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DATA = SITE / "data"
MANIFEST = DATA / "national-coverage-manifest.json"
REPORT = DATA / "adsense-quality-recovery.json"
REPORT_TEXT = DATA / "adsense-quality-recovery.txt"
DOMAIN = "https://septicscope.com"
ADSENSE_CLIENT = "ca-pub-8782868222380999"
TODAY = date.today().isoformat()

STATE_NAMES = {
    "alabama": "Alabama", "alaska": "Alaska", "arizona": "Arizona", "arkansas": "Arkansas",
    "california": "California", "colorado": "Colorado", "connecticut": "Connecticut",
    "delaware": "Delaware", "district-of-columbia": "District of Columbia", "florida": "Florida",
    "georgia": "Georgia", "hawaii": "Hawaii", "idaho": "Idaho", "illinois": "Illinois",
    "indiana": "Indiana", "iowa": "Iowa", "kansas": "Kansas", "kentucky": "Kentucky",
    "louisiana": "Louisiana", "maine": "Maine", "maryland": "Maryland",
    "massachusetts": "Massachusetts", "michigan": "Michigan", "minnesota": "Minnesota",
    "mississippi": "Mississippi", "missouri": "Missouri", "montana": "Montana",
    "nebraska": "Nebraska", "nevada": "Nevada", "new-hampshire": "New Hampshire",
    "new-jersey": "New Jersey", "new-mexico": "New Mexico", "new-york": "New York",
    "north-carolina": "North Carolina", "north-dakota": "North Dakota", "ohio": "Ohio",
    "oklahoma": "Oklahoma", "oregon": "Oregon", "pennsylvania": "Pennsylvania",
    "rhode-island": "Rhode Island", "south-carolina": "South Carolina",
    "south-dakota": "South Dakota", "tennessee": "Tennessee", "texas": "Texas",
    "utah": "Utah", "vermont": "Vermont", "virginia": "Virginia",
    "washington": "Washington", "west-virginia": "West Virginia", "wisconsin": "Wisconsin",
    "wyoming": "Wyoming",
}

BAD_COUNTY_PHRASES = (
    "local guide in progress",
    "county-specific details not independently confirmed",
    "we're still source-checking",
    "we’re still source-checking",
    "not yet verified",
    "official help links",
)

LOCAL_TERMS = (
    "county", "parish", "borough", "municipal", "city of", "town of", "village of",
    "health department", "public health", "health district", "district health",
    "regional health", "environmental health", "field office", "regional office",
    "development services", "planning department", "permit office", "sanitarian",
)

GENERIC_SOURCE_HOSTS = {
    "epa.gov", "www.epa.gov", "usa.gov", "www.usa.gov", "ecfr.gov", "www.ecfr.gov",
}

BLOCK_TAGS = {"p", "li", "h2", "h3", "td", "th", "figcaption"}
SKIP_TAGS = {"script", "style", "noscript", "svg", "header", "footer", "nav"}


@dataclass
class ParsedPage:
    title: str = ""
    h1: str = ""
    robots: str = ""
    canonical: str = ""
    text_parts: list[str] = field(default_factory=list)
    blocks: list[str] = field(default_factory=list)
    anchors: list[tuple[str, str]] = field(default_factory=list)

    @property
    def text(self) -> str:
        return clean(" ".join(self.text_parts))


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.page = ParsedPage()
        self._main_depth = 0
        self._skip_depth = 0
        self._capture: str | None = None
        self._capture_parts: list[str] = []
        self._block_tag: str | None = None
        self._block_parts: list[str] = []
        self._anchor_href: str | None = None
        self._anchor_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr = {str(k).lower(): str(v or "") for k, v in attrs}
        if tag == "main":
            self._main_depth += 1
        if tag in SKIP_TAGS or attr.get("data-septicscope-provider-section") == "1" or attr.get("data-septicscope-growth-links") == "1":
            self._skip_depth += 1
        if tag in {"title", "h1"}:
            self._capture = tag
            self._capture_parts = []
        elif tag == "meta":
            name = attr.get("name", "").lower()
            if name == "robots":
                self.page.robots = attr.get("content", "").strip().lower()
        elif tag == "link" and "canonical" in attr.get("rel", "").lower():
            self.page.canonical = attr.get("href", "").strip()
        if self._main_depth and not self._skip_depth and tag in BLOCK_TAGS:
            self._block_tag = tag
            self._block_parts = []
        if self._main_depth and not self._skip_depth and tag == "a" and attr.get("href"):
            self._anchor_href = attr["href"].strip()
            self._anchor_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._capture == tag:
            value = clean(" ".join(self._capture_parts))
            if tag == "title":
                self.page.title = value
            elif tag == "h1":
                self.page.h1 = value
            self._capture = None
            self._capture_parts = []
        if self._block_tag == tag:
            value = clean(" ".join(self._block_parts))
            if value:
                self.page.blocks.append(value)
            self._block_tag = None
            self._block_parts = []
        if tag == "a" and self._anchor_href is not None:
            self.page.anchors.append((self._anchor_href, clean(" ".join(self._anchor_parts))))
            self._anchor_href = None
            self._anchor_parts = []
        if tag in SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
        if tag == "main" and self._main_depth:
            self._main_depth -= 1

    def handle_data(self, data: str) -> None:
        value = clean(data)
        if not value:
            return
        if self._capture:
            self._capture_parts.append(value)
        if self._main_depth and not self._skip_depth:
            self.page.text_parts.append(value)
            if self._block_tag:
                self._block_parts.append(value)
            if self._anchor_href is not None:
                self._anchor_parts.append(value)


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def parse(path: Path) -> ParsedPage:
    parser = Parser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser.page


def word_count(value: str) -> int:
    return len(re.findall(r"\b[a-zA-Z][a-zA-Z'-]*\b", value))


def route(path: Path) -> str:
    rel = path.relative_to(SITE).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-10]
    return "/" + rel


def is_external(href: str) -> bool:
    parsed = urlparse(href)
    return parsed.scheme in {"http", "https"} and parsed.netloc.lower().split(":")[0] not in {"septicscope.com", "www.septicscope.com"}


def normalize_block(block: str, location_terms: set[str]) -> str:
    value = block.lower()
    value = re.sub(r"https?://\S+", " url ", value)
    value = re.sub(r"\b\d{3}[-.) ]\d{3}[- ]\d{4}\b", " phone ", value)
    value = re.sub(r"\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\b", " date ", value)
    value = re.sub(r"\b\d+(?:\.\d+)?\b", " number ", value)
    for term in sorted(location_terms, key=len, reverse=True):
        if len(term) >= 4:
            value = re.sub(rf"\b{re.escape(term)}\b", " place ", value)
    value = re.sub(r"[^a-z# ]+", " ", value)
    return clean(value)


def location_terms(path: Path, page: ParsedPage) -> set[str]:
    parts = path.relative_to(SITE).parts
    state_slug = parts[1]
    county_slug = parts[2]
    values = set(re.findall(r"[a-z]+", state_slug.replace("-", " ") + " " + county_slug.replace("-", " ")))
    values.update(re.findall(r"[a-z]+", page.h1.lower()))
    values.difference_update({"county", "parish", "borough", "census", "area", "city", "septic", "permits", "requirements"})
    return values


def local_source(label: str, href: str, page_path: Path) -> bool:
    parsed = urlparse(href)
    host = parsed.netloc.lower().removeprefix("www.")
    if host in GENERIC_SOURCE_HOSTS:
        return False
    lower = f"{label} {parsed.path}".lower()
    county_slug = page_path.relative_to(SITE).parts[2]
    county_tokens = [token for token in county_slug.split("-") if len(token) >= 4]
    if any(term in lower for term in LOCAL_TERMS):
        return True
    if any(token in host or token in lower for token in county_tokens):
        return True
    if host.endswith(".gov") or host.endswith(".us"):
        return any(term in lower for term in ("office", "district", "health", "onsite", "septic", "wastewater", "permit"))
    return False


def local_detail_score(text: str, local_sources: int) -> tuple[int, list[str]]:
    checks = {
        "public_phone": r"\b\d{3}[-.) ]\d{3}[- ]\d{4}\b",
        "street_or_office_address": r"\b\d{1,6}\s+[A-Z0-9][A-Za-z0-9 .'-]{3,}\b(?:street|st\.?|road|rd\.?|avenue|ave\.?|drive|dr\.?|boulevard|blvd\.?|highway|hwy\.?|lane|ln\.?|parkway|pkwy\.?|suite)\b",
        "application_or_form": r"\b(application|apply|form|portal|submit|submittal)\b",
        "inspection_process": r"\b(inspection|inspect|final approval|certificate of completion)\b",
        "records_or_as_built": r"\b(records?|as[- ]built|site plan|permit history|file request)\b",
        "fees_or_costs": r"\b(fees?|fee schedule|payment|costs?)\b",
        "local_rule_or_code": r"\b(ordinance|code|wac|kar|tac|rule|chapter|regulation)\b",
        "maintenance_or_operating_requirement": r"\b(maintenance agreement|maintenance contract|operating permit|operational permit|renewal|renewable)\b",
    }
    hits = [name for name, pattern in checks.items() if re.search(pattern, text, flags=re.I)]
    if local_sources:
        hits.append("local_or_regional_source")
    return len(hits), hits


def ensure_noindex(raw: str, marker: str) -> str:
    marker_tag = f'<meta name="septicscope-quality-status" content="{marker}">'
    if re.search(r'<meta\s+[^>]*name=["\']robots["\'][^>]*>', raw, flags=re.I):
        raw = re.sub(
            r'<meta\s+[^>]*name=["\']robots["\'][^>]*>',
            '<meta name="robots" content="noindex,follow">',
            raw,
            count=1,
            flags=re.I,
        )
    else:
        raw = re.sub(r"</head>", '<meta name="robots" content="noindex,follow"></head>', raw, count=1, flags=re.I)
    if "septicscope-quality-status" not in raw:
        raw = re.sub(r"</head>", marker_tag + "</head>", raw, count=1, flags=re.I)
    return raw


def strip_ads(raw: str) -> str:
    raw = re.sub(
        r'<script\b[^>]*src=["\'][^"\']*pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^"\']*["\'][^>]*>\s*</script>',
        "",
        raw,
        flags=re.I | re.S,
    )
    raw = re.sub(r'<ins\b[^>]*class=["\'][^"\']*adsbygoogle[^"\']*["\'][^>]*>.*?</ins>', "", raw, flags=re.I | re.S)
    raw = re.sub(r'<script\b[^>]*>\s*\(adsbygoogle\s*=\s*window\.adsbygoogle\s*\|\|\s*\[\]\)\.push\([^;]*;?\s*</script>', "", raw, flags=re.I | re.S)
    raw = re.sub(r'<script\b[^>]*>[^<]{0,500}adsbygoogle\.push\([^<]{0,500}</script>', "", raw, flags=re.I | re.S)
    return raw


def add_adsense(raw: str) -> str:
    if ADSENSE_CLIENT in raw:
        return raw
    tag = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>'
    return re.sub(r"</head>", tag + "</head>", raw, count=1, flags=re.I)


def canonical_url(path: Path) -> str:
    return DOMAIN + route(path)


def sitemap_urls() -> tuple[ET.ElementTree, ET.Element, str]:
    path = SITE / "sitemap.xml"
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    tree = ET.parse(path)
    return tree, tree.getroot(), ns


def set_sitemap(allowed: set[str]) -> None:
    tree, root, ns = sitemap_urls()
    existing: dict[str, ET.Element] = {}
    for node in list(root):
        loc = node.find(f"{{{ns}}}loc")
        value = clean(loc.text if loc is not None else "")
        if not value or value not in allowed:
            root.remove(node)
        else:
            if value in existing:
                root.remove(node)
            else:
                existing[value] = node
    for url in sorted(allowed):
        if url in existing:
            continue
        node = ET.SubElement(root, f"{{{ns}}}url")
        ET.SubElement(node, f"{{{ns}}}loc").text = url
        ET.SubElement(node, f"{{{ns}}}lastmod").text = TODAY
    tree.write(SITE / "sitemap.xml", encoding="utf-8", xml_declaration=True)


def rewrite_faq_hub() -> None:
    faq = SITE / "faq" / "index.html"
    faq.parent.mkdir(parents=True, exist_ok=True)
    answers = [
        ("How often should a septic tank be pumped?", "Many conventional household systems are pumped about every three to five years, but that is a planning range rather than a universal schedule. Tank size, household size, water use, garbage-disposal use, solids accumulation, system type, and local requirements can change the interval. Inspection and sludge/scum measurements provide better evidence than the calendar alone. Keep every pumping receipt so the next service provider can see the actual history.", "/guides/septic-maintenance-checklist/"),
        ("How can I tell whether the tank is full or the system is failing?", "Slow drains, gurgling, sewage backups, odors, wet or spongy soil, unusually green grass over the drainfield, or a high-water alarm can signal a problem, but they do not identify the cause by themselves. A tank can need routine pumping without the drainfield being failed, and a recently pumped tank does not prove the rest of the system is healthy. Reduce water use and arrange qualified evaluation when several fixtures are affected or sewage is present.", "/guides/septic-drainfield-repair-replacement/"),
        ("What should never be flushed into a septic system?", "The safest rule is to flush only human waste and toilet paper. Wipes, paper towels, diapers, hygiene products, floss, cat litter, grease, paint, solvents, pesticides, and other trash or hazardous chemicals can clog plumbing, disrupt treatment, or increase solids reaching the tank and drainfield. Products labeled flushable can still create problems because dispersibility and actual household plumbing conditions vary." , "/guides/septic-maintenance-checklist/"),
        ("What does a septic alarm mean?", "An alarm usually means liquid has reached a high-water level or a pump/control condition needs attention. Silence the audible alarm if the control panel instructions allow it, but do not turn off the system or keep using large amounts of water. Avoid laundry, dishwashing, long showers, and other heavy use until the cause is evaluated. Sewage backup, exposed wiring, or flooded electrical equipment requires immediate professional help and safe separation from the area.", "/guides/types-of-septic-systems/"),
        ("How do I find a septic permit or as-built drawing?", "Start with the legal county for the property, not only the mailing city or ZIP code. Ask the permitting authority for the original permit, site evaluation, approved design, as-built drawing, final inspection, repair permits, operating permits, and maintenance records that may be in the public file. Records can be held by a county, health district, municipality, state office, or delegated agency. Use the county lookup below to identify the correct starting point.", "/counties/"),
        ("Can I drive, park, build, or plant trees over a drainfield?", "Avoid vehicles, heavy equipment, buildings, patios, pools, and other loads over the tank and drainfield unless a qualified designer and permitting authority approve a specific protected design. Compaction can reduce soil treatment capacity and damage components. Deep-rooted trees and shrubs can also interfere with piping or the absorption area. Maintain shallow grass cover and route roof, driveway, and surface drainage away from the field.", "/guides/septic-drainfield-repair-replacement/"),
        ("How long does a septic system last?", "There is no universal expiration date. Public agencies and Extension programs often use roughly twenty to thirty years as a planning range for conventional systems, while noting that proper siting, design, installation, maintenance, loading, soil, groundwater, and component type can shorten or extend useful life. Tank age is not the same as the condition of pumps, distribution components, piping, or the soil treatment area.", "/guides/septic-system-lifespan/"),
        ("Can heavy rain affect a septic system?", "Yes. Saturated soil and high groundwater can reduce the drainfield's ability to accept and treat wastewater. Conserve water during very wet conditions, fix leaks, keep surface drainage away from the field, and do not pump a tank solely to create space while groundwater is high unless a qualified local professional advises it; an empty tank can be vulnerable to movement in some conditions. Persistent backup or surfacing sewage needs prompt evaluation.", "/guides/septic-system-winter-care/"),
        ("What should a septic inspection include?", "A useful inspection should start with permits, design records, maintenance history, system type, and property observations. Scope can include tank access, sludge and scum measurements, baffles, filters, pumps, alarms, controls, distribution components, and drainfield conditions when accessible and appropriate. Ask what is excluded, whether pumping is required, what local transfer rules apply, and whether the report clearly separates observed facts from recommendations.", "/guides/septic-inspection-checklist/"),
        ("Do septic additives replace pumping or maintenance?", "No additive should be treated as a substitute for inspection, pumping, repair, or required maintenance. EPA does not recommend routine additives for domestic wastewater treatment, and some products can move solids or interfere with treatment. A functioning system already contains microorganisms. Decisions should be based on the permit, system design, measured solids, observed condition, and qualified local advice rather than a universal additive claim.", "/guides/septic-maintenance-checklist/"),
    ]
    faq_entities = []
    sections = []
    for question, answer, link in answers:
        faq_entities.append({"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}})
        sections.append(f'<section class="faq-answer"><h2>{escape(question)}</h2><p>{escape(answer)}</p><p><a href="{escape(link)}">Read the related SepticScope guide →</a></p></section>')
    schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_entities}, ensure_ascii=False).replace("<", "\\u003c")
    style = ''':root{--ink:#17221f;--muted:#5d6965;--forest:#123d35;--line:#d9e2dc;--soft:#eef6f2;--cream:#faf6ec;--max:980px}*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}a{color:#176b5b;text-underline-offset:3px}header,footer{border-block:1px solid var(--line)}.nav,main,.foot{max-width:var(--max);margin:auto;padding:18px 24px}.brand{font-weight:900;color:var(--forest);text-decoration:none}main{padding-top:55px;padding-bottom:75px}h1{font-size:clamp(2.45rem,6vw,4.5rem);line-height:1.03;letter-spacing:-.04em;color:var(--forest)}h2{color:var(--forest);line-height:1.18}.lead{font-size:1.15rem;color:var(--muted);max-width:800px}.notice{background:var(--cream);border:1px solid #eadcbc;border-radius:15px;padding:17px;margin:26px 0}.faq-grid{display:grid;gap:14px}.faq-answer{border:1px solid var(--line);border-radius:16px;padding:20px;background:#fff}.faq-answer h2{margin-top:0;font-size:1.3rem}.sources{background:var(--soft);border-radius:18px;padding:22px;margin-top:35px}.foot{color:var(--muted)}'''
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Septic System FAQ: Pumping, Alarms, Drainfields, Records & Inspections</title><meta name="description" content="Clear, source-based answers to common septic system questions about pumping, failure signs, alarms, drainfields, records, inspections, lifespan, rain, additives, and safe use."><link rel="canonical" href="{DOMAIN}/faq/"><style>{style}</style><script async src="https://www.googletagmanager.com/gtag/js?id=G-F6RB8YERCM"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-F6RB8YERCM');</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script><script type="application/ld+json">{schema}</script></head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a> · <a href="/counties/">County lookup</a> · <a href="/guides/">Guides</a> · <a href="/about/">Research standards</a></div></header><main><p><a href="/">Home</a> / Septic system FAQ</p><h1>Septic system frequently asked questions</h1><p class="lead">These answers are designed to help homeowners choose a safe next step. They do not replace a permit, site evaluation, inspection, engineering opinion, or diagnosis for a specific property.</p><div class="notice"><strong>Urgent sewage warning:</strong> Keep people and pets away from sewage or wastewater surfacing in the home or yard. Reduce water use and contact a qualified local professional or public-health authority.</div><div class="faq-grid">{''.join(sections)}</div><section class="sources"><h2>Primary public sources used for this FAQ</h2><ul><li><a href="https://www.epa.gov/septic/how-care-your-septic-system" rel="nofollow">U.S. EPA — How to Care for Your Septic System</a></li><li><a href="https://www.epa.gov/septic/resolving-septic-system-malfunctions" rel="nofollow">U.S. EPA — Resolving Septic System Malfunctions</a></li><li><a href="https://www.epa.gov/septic/types-septic-systems" rel="nofollow">U.S. EPA — Types of Septic Systems</a></li><li><a href="https://www.epa.gov/septic/frequent-questions-septic-systems" rel="nofollow">U.S. EPA — Frequent Questions on Septic Systems</a></li></ul><p>Last editorial review: {TODAY}. Local requirements and the property-specific permit control when they differ from general guidance.</p></section></main><footer><div class="foot">© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a> · <a href="/contact/">Corrections & feedback</a></div></footer></body></html>'''
    faq.write_text(html, encoding="utf-8")


def rewrite_about() -> None:
    out = SITE / "about" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    style = ''':root{--ink:#17221f;--muted:#5d6965;--forest:#123d35;--line:#d9e2dc;--soft:#eef6f2;--cream:#faf6ec;--max:980px}*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);line-height:1.7}a{color:#176b5b;text-underline-offset:3px}header,footer{border-block:1px solid var(--line)}.nav,main,.foot{max-width:var(--max);margin:auto;padding:18px 24px}.brand{font-weight:900;color:var(--forest);text-decoration:none}main{padding-top:55px;padding-bottom:75px}h1{font-size:clamp(2.45rem,6vw,4.5rem);line-height:1.03;letter-spacing:-.04em;color:var(--forest)}h2{color:var(--forest);margin-top:1.6em}.lead{font-size:1.16rem;color:var(--muted)}.principles{display:grid;grid-template-columns:1fr 1fr;gap:14px}.card{border:1px solid var(--line);border-radius:16px;padding:20px;background:#fff}.card h3{margin-top:0;color:var(--forest)}.disclosure{background:var(--cream);border:1px solid #eadcbc;border-radius:16px;padding:20px}.foot{color:var(--muted)}@media(max-width:700px){.principles{grid-template-columns:1fr}}'''
    body = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>About SepticScope: Editorial Standards, Sources & Corrections</title><meta name="description" content="Learn how SepticScope researches septic permits and homeowner guidance, separates verified facts from unfinished work, handles automation, advertising, corrections, and source reviews."><link rel="canonical" href="{DOMAIN}/about/"><style>{style}</style><script async src="https://www.googletagmanager.com/gtag/js?id=G-F6RB8YERCM"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-F6RB8YERCM');</script></head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a> · <a href="/counties/">County lookup</a> · <a href="/guides/">Guides</a> · <a href="/faq/">FAQs</a></div></header><main><p><a href="/">Home</a> / About</p><h1>How SepticScope researches, publishes, and corrects septic information</h1><p class="lead">SepticScope is an independent informational website built to make public septic and onsite-wastewater information easier to use. It is not a government agency, permitting authority, engineering firm, inspection company, installer, pumper, or substitute for a qualified local professional.</p><div class="disclosure"><strong>Important limitation:</strong> Septic requirements can depend on the legal county, delegated health jurisdiction, municipality, parcel conditions, soil, groundwater, design flow, system type, project type, permit history, and current agency interpretation. The current permitting authority and property-specific documents always control.</div><h2>What we are trying to solve</h2><p>Homeowners often need to move between county websites, state rules, health-district pages, forms, fee schedules, property records, and contractor information before they can answer a basic question. SepticScope connects those steps without pretending that one national answer applies everywhere. County lookup, homeowner guides, checklists, and calculators are kept separate from property-specific regulatory decisions.</p><h2>Editorial standards</h2><div class="principles"><article class="card"><h3>Use primary public sources first</h3><p>Regulatory statements should come from government, public-health, environmental, code, university Extension, or another recognized public source. Contractor marketing is not used to establish a legal requirement.</p></article><article class="card"><h3>Keep local and statewide facts separate</h3><p>A statewide rule does not make every county page unique. A county page stays out of search when it only repeats statewide text and lacks enough locally useful process, contact, records, fee, inspection, or authority information.</p></article><article class="card"><h3>Show the source and review date</h3><p>Published local guides identify the authority, link to the sources used, and display a review date. We do not hide the source behind an unsupported summary.</p></article><article class="card"><h3>Do not manufacture certainty</h3><p>We avoid universal cost promises, permit-ready sizing claims, diagnosis from symptoms alone, copied ratings, and service-area assumptions. Uncertainty and local verification steps are stated plainly.</p></article></div><h2>How automation is used</h2><p>Automation may help build navigation, check links, detect missing metadata, compare page similarity, maintain a national county index, and flag material for review. Automation is not allowed to upgrade a county page merely because a template exists, add repetitive links on a schedule, or invent a regulation, business, credential, service area, fee, permit step, or property-specific conclusion.</p><p>Following a September 2026 quality review, SepticScope stopped automatic hourly content mutation and reduced the indexable county footprint. Pages that are unfinished, too similar to other location pages, or insufficiently local are withheld from search and advertising until the underlying research is stronger.</p><h2>Advertising and commercial separation</h2><p>Display advertising helps fund hosting and research, but ads do not determine conclusions, source selection, or county publication status. Navigation, privacy, contact, unfinished, and quality-withheld pages are kept ad-free. If sponsored or affiliate relationships are introduced, they must be labeled and use the appropriate link relationship. Ordinary provider records are not endorsements or rankings.</p><h2>Corrections and review</h2><p>Rules, contacts, forms, fees, and agency pages can change. Readers and public agencies can report a broken link, outdated requirement, incorrect authority, or other issue through the <a href="/contact/">Contact &amp; Feedback page</a>. A useful correction includes the affected URL and the current official source. Material regulatory corrections take priority over cosmetic changes.</p><h2>What publication status means</h2><ul><li><strong>Published local guide:</strong> the page has enough source-supported local detail and passes the current quality gate.</li><li><strong>Withheld county research:</strong> a page may exist in the build for internal coverage tracking but is not promoted, indexed, or monetized.</li><li><strong>General homeowner guide:</strong> national education that clearly tells readers when local rules or professional evaluation are required.</li></ul><h2>Contact</h2><p>Use <a href="/contact/">Contact &amp; Feedback</a> for corrections, accessibility issues, source suggestions, privacy questions, or business-listing concerns. Last editorial-policy review: {TODAY}.</p></main><footer><div class="foot">© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/contact/">Corrections & feedback</a></div></footer></body></html>'''
    out.write_text(body, encoding="utf-8")


def build_homepage(approved: list[dict[str, Any]], retained_guides: list[str]) -> None:
    featured = approved[:8]
    county_cards = "".join(
        f'<a class="county-card" href="{escape(item["route"])}"><strong>{escape(item["county_label"])}</strong><span>{escape(item["authority"] or "Local authority identified")} · sources reviewed</span></a>'
        for item in featured
    )
    guide_candidates = [
        ("/guides/septic-maintenance-checklist/", "Septic maintenance checklist", "Recurring care, pumping history, inspections, records, and property checks."),
        ("/guides/septic-inspection-checklist/", "Septic inspection checklist", "What to review before hiring, buying, selling, or making a repair decision."),
        ("/guides/septic-drainfield-repair-replacement/", "Drainfield repair or replacement", "Understand what should be evaluated before accepting a full replacement recommendation."),
        ("/guides/types-of-septic-systems/", "Types of septic systems", "Compare conventional, aerobic, mound, drip, chamber, and sand-filter approaches."),
        ("/guides/septic-system-lifespan/", "Septic system lifespan", "Plan around condition, records, site factors, and component differences—not a fake expiration date."),
        ("/guides/septic-tank-size-calculator/", "Septic tank-size planning tool", "Use documented state examples and finish with the local permitting rule."),
    ]
    guide_set = set(retained_guides)
    guide_cards = "".join(
        f'<a class="guide-card" href="{path}"><strong>{escape(title)}</strong><span>{escape(description)}</span></a>'
        for path, title, description in guide_candidates if path in guide_set
    )
    schema = json.dumps({
        "@context": "https://schema.org", "@graph": [
            {"@type": "Organization", "@id": f"{DOMAIN}/#organization", "name": "SepticScope", "url": f"{DOMAIN}/"},
            {"@type": "WebSite", "@id": f"{DOMAIN}/#website", "url": f"{DOMAIN}/", "name": "SepticScope", "publisher": {"@id": f"{DOMAIN}/#organization"},
             "potentialAction": {"@type": "SearchAction", "target": f"{DOMAIN}/counties/?q={{search_term_string}}", "query-input": "required name=search_term_string"}},
        ],
    }, ensure_ascii=False).replace("<", "\\u003c")
    style = f''':root{{--ink:#17221f;--muted:#5d6965;--forest:#123d35;--forest2:#1e6253;--line:#d9e2dc;--mint:#eaf4ef;--cream:#faf6ec;--paper:#fffdfa;--shadow:0 16px 48px rgba(18,61,53,.10);--max:1180px}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);line-height:1.66}}a{{color:var(--forest2);text-underline-offset:3px}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:16px;top:12px;background:#fff;padding:10px;z-index:99}}header{{border-bottom:1px solid var(--line);background:#fff}}.nav{{max-width:var(--max);margin:auto;padding:16px 22px;display:flex;justify-content:space-between;gap:20px;align-items:center}}.brand{{font-weight:950;color:var(--forest);text-decoration:none;font-size:1.1rem}}.navlinks{{display:flex;gap:18px;flex-wrap:wrap}}.navlinks a{{text-decoration:none;font-weight:800;color:var(--ink)}}.hero{{background:var(--cream);border-bottom:1px solid var(--line)}}.hero-inner{{max-width:var(--max);margin:auto;padding:70px 22px;display:grid;grid-template-columns:minmax(0,1.22fr) minmax(300px,.78fr);gap:46px;align-items:center}}.eyebrow{{font-size:.77rem;font-weight:950;letter-spacing:.13em;text-transform:uppercase;color:var(--forest2)}}h1{{font-size:clamp(2.75rem,6vw,5rem);line-height:1.01;letter-spacing:-.05em;color:var(--forest);margin:.18em 0}}.lead{{font-size:clamp(1.08rem,2vw,1.24rem);color:#46534f;max-width:780px}}.hero-note{{border-radius:24px;background:var(--forest);color:#fff;padding:28px;box-shadow:var(--shadow)}}.hero-note h2{{color:#fff;margin-top:0}}.hero-note p{{color:#d8e7e2}}.hero-note li{{margin:.65em 0}}{county_lookup.LOOKUP_CSS}.section{{max-width:var(--max);margin:auto;padding:68px 22px}}.section-head{{display:flex;justify-content:space-between;align-items:end;gap:26px;margin-bottom:25px}}.section-head h2{{font-size:clamp(2rem,4vw,3rem);line-height:1.08;color:var(--forest);margin:0}}.section-head p{{max-width:600px;color:var(--muted);margin:0}}.journey{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.journey article{{border:1px solid var(--line);border-radius:17px;padding:20px;background:#fff}}.journey h3{{color:var(--forest);margin-top:0}}.guide-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.guide-card,.county-card{{border:1px solid var(--line);border-radius:15px;padding:18px;background:#fff;text-decoration:none;color:var(--ink)}}.guide-card strong,.county-card strong{{display:block;color:var(--forest);font-size:1.06rem}}.guide-card span,.county-card span{{display:block;color:var(--muted);margin-top:7px;font-size:.9rem}}.county-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:11px}}.method{{background:var(--mint);border-block:1px solid var(--line)}}.method-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.method article{{background:#fff;border:1px solid var(--line);border-radius:15px;padding:19px}}.method h3{{color:var(--forest);margin-top:0}}.cta{{background:var(--forest);color:#fff;border-radius:24px;padding:32px}}.cta h2{{color:#fff;margin-top:0}}.cta p{{color:#d8e7e2}}.cta a{{display:inline-flex;background:#fff;color:var(--forest);padding:11px 15px;border-radius:10px;font-weight:900;text-decoration:none}}footer{{background:#102e29;color:#d9e6e1}}.foot{{max-width:var(--max);margin:auto;padding:35px 22px}}.foot a{{color:#fff;margin-right:16px}}@media(max-width:900px){{.hero-inner{{grid-template-columns:1fr}}.journey,.guide-grid{{grid-template-columns:1fr 1fr}}.county-grid{{grid-template-columns:1fr 1fr}}.method-grid{{grid-template-columns:1fr}}}}@media(max-width:650px){{.navlinks a:nth-child(n+4){{display:none}}.section-head{{display:block}}.section-head p{{margin-top:10px}}.journey,.guide-grid,.county-grid{{grid-template-columns:1fr}}}}'''
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SepticScope: Practical Septic Permits, Maintenance & Homeowner Guidance</title><meta name="description" content="Find the correct county septic authority, then use source-based guides for permits, records, inspections, maintenance, system types, drainfields, costs, and replacement planning."><link rel="canonical" href="{DOMAIN}/"><style>{style}</style><script async src="https://www.googletagmanager.com/gtag/js?id=G-F6RB8YERCM"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-F6RB8YERCM');</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script><script defer src="/assets/county-lookup.js"></script><script type="application/ld+json">{schema}</script></head><body><a class="skip" href="#main">Skip to content</a><header><nav class="nav"><a class="brand" href="/">SepticScope</a><div class="navlinks"><a href="/counties/">County lookup</a><a href="/guides/">Homeowner guides</a><a href="/faq/">Septic FAQ</a><a href="/about/">How we research</a></div></nav></header><main id="main"><section class="hero"><div class="hero-inner"><div><p class="eyebrow">Public sources translated into practical next steps</p><h1>Practical septic guidance for real property decisions.</h1><p class="lead">Start with the legal county, find the responsible authority, and then use focused guidance for permits, records, inspections, maintenance, system problems, and replacement planning.</p>{county_lookup.lookup_form()}</div><aside class="hero-note"><h2>What changed</h2><p>SepticScope now withholds unfinished and repetitive location pages instead of treating a statewide template as a finished county guide.</p><ul><li>County pages need meaningful local detail before search indexing.</li><li>Navigation and unfinished research remain ad-free.</li><li>Sources, review dates, and correction routes stay visible.</li><li>No copied ratings, invented rules, or permit-ready guesses.</li></ul></aside></div></section><section class="section"><div class="section-head"><div><p class="eyebrow">The homeowner journey</p><h2>Move from the property question to the right next step.</h2></div><p>Septic work is local, but the decision process is consistent: identify the authority, understand the system or symptom, then verify the permit and professional scope.</p></div><div class="journey"><article><h3>1. Locate records and authority</h3><p>Use the county lookup to find the legal jurisdiction, permitting authority, official sources, permit history, and as-built starting points.</p></article><article><h3>2. Understand the system or problem</h3><p>Use a focused guide or checklist to prepare for maintenance, inspection, troubleshooting, a property transfer, or design planning.</p></article><article><h3>3. Confirm the property-specific path</h3><p>Current agency instructions, site conditions, the approved design, and qualified local professionals control the final answer.</p></article></div></section><section class="method"><div class="section"><div class="section-head"><div><p class="eyebrow">Focused, substantive resources</p><h2>Homeowner guides worth keeping.</h2></div><p>These pages are retained because they answer a distinct task with meaningful explanation, sources, cautions, and next steps.</p></div><div class="guide-grid">{guide_cards}</div><p style="margin-top:24px"><a href="/guides/"><strong>Browse all quality-reviewed guides →</strong></a></p></div></section><section class="section"><div class="section-head"><div><p class="eyebrow">Locally differentiated research</p><h2>Featured county guides that passed the quality gate.</h2></div><p>A county guide must provide more than a changed place name. It needs locally useful authority, process, contact, records, inspection, fee, code, or source detail.</p></div><div class="county-grid">{county_cards or '<p>County pages are being re-reviewed under the stricter standard.</p>'}</div><p style="margin-top:24px"><a href="/counties/"><strong>Search by ZIP, city, county, or FIPS code →</strong></a></p></section><section class="section"><div class="section-head"><div><p class="eyebrow">Common questions</p><h2>One comprehensive septic FAQ instead of thin answer pages.</h2></div><p>Pumping, alarms, failure signs, records, inspections, rain, additives, drainfield protection, and lifespan are consolidated into one source-based resource.</p></div><div class="cta"><h2>Start with the septic system FAQ.</h2><p>Get a concise answer, understand the limitation, and continue to the right detailed guide or county lookup.</p><a href="/faq/">Read the septic FAQ</a></div></section><section class="method"><div class="section"><div class="section-head"><div><p class="eyebrow">Publication standard</p><h2>Fewer pages, stronger reasons to trust each one.</h2></div></div><div class="method-grid"><article><h3>Primary sources first</h3><p>Government, public-health, code, and recognized public institutions support regulatory statements.</p></article><article><h3>Local evidence required</h3><p>Statewide rules can provide context, but they do not make dozens of county pages independently valuable.</p></article><article><h3>Corrections are visible</h3><p>Review dates and a public correction route make it possible to maintain changing contacts, forms, and rules.</p></article></div><p style="margin-top:24px"><a href="/about/"><strong>Read the full editorial and automation policy →</strong></a></p></div></section></main><footer><div class="foot"><a href="/counties/">County lookup</a><a href="/guides/">Guides</a><a href="/faq/">FAQ</a><a href="/about/">About</a><a href="/privacy/">Privacy</a><a href="/contact/">Corrections</a><p>© 2026 SepticScope. Independent informational resource; not a government agency or substitute for property-specific professional advice.</p></div></footer></body></html>'''
    (SITE / "index.html").write_text(html, encoding="utf-8")


def process() -> dict[str, Any]:
    if not SITE.is_dir() or not MANIFEST.exists():
        raise RuntimeError("Build the site and first inventory before quality recovery")

    manifest_data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest_records = manifest_data.get("records", [])
    by_route = {urlparse(clean(row.get("page_url"))).path: row for row in manifest_records if isinstance(row, dict)}

    county_paths = sorted(SITE.glob("counties/*/*/index.html"))
    candidates: list[tuple[Path, ParsedPage]] = []
    block_frequency: Counter[str] = Counter()
    normalized_by_path: dict[Path, list[tuple[str, int]]] = {}
    for path in county_paths:
        page = parse(path)
        if "noindex" in page.robots or not page.text:
            continue
        candidates.append((path, page))
        terms = location_terms(path, page)
        normalized = []
        for block in page.blocks:
            key = normalize_block(block, terms)
            words = word_count(key)
            if words >= 8:
                normalized.append((key, words))
                block_frequency[key] += 1
        normalized_by_path[path] = normalized

    approved: list[dict[str, Any]] = []
    demoted: list[dict[str, Any]] = []
    approved_routes: set[str] = set()
    approved_fips: set[str] = set()
    max_shared_ratio = 0.48

    for path, page in candidates:
        page_route = route(path)
        row = by_route.get(page_route, {})
        main_words = word_count(page.text)
        external = [(href, label) for href, label in page.anchors if is_external(href)]
        local = [(href, label) for href, label in external if local_source(label, href, path)]
        details, detail_hits = local_detail_score(page.text, len(local))
        normalized = normalized_by_path.get(path, [])
        total_block_words = sum(words for _key, words in normalized) or 1
        shared_words = sum(words for key, words in normalized if block_frequency[key] >= 4)
        shared_ratio = round(shared_words / total_block_words, 3)
        bad = [phrase for phrase in BAD_COUNTY_PHRASES if phrase in page.text.lower()]
        reasons = []
        if main_words < 300:
            reasons.append(f"only_{main_words}_main_words")
        if len(external) < 3:
            reasons.append(f"only_{len(external)}_external_sources")
        if not local:
            reasons.append("no_local_or_regional_source")
        if details < 4:
            reasons.append(f"only_{details}_local_detail_signals")
        if shared_ratio > max_shared_ratio:
            reasons.append(f"shared_template_ratio_{shared_ratio}")
        if bad:
            reasons.append("unfinished_or_unverified_language")
        record = {
            "route": page_route,
            "url": DOMAIN + page_route,
            "fips": clean(row.get("fips")),
            "county_label": f'{clean(row.get("county_or_equivalent_name"))}, {clean(row.get("state"))}',
            "authority": clean(row.get("official_regulating_authority")),
            "main_words": main_words,
            "external_sources": len(external),
            "local_sources": len(local),
            "local_detail_score": details,
            "local_detail_signals": detail_hits,
            "shared_template_ratio": shared_ratio,
            "decision_reasons": reasons,
        }
        if reasons:
            raw = path.read_text(encoding="utf-8", errors="replace")
            path.write_text(strip_ads(ensure_noindex(raw, "withheld-local-quality")), encoding="utf-8")
            demoted.append(record)
        else:
            approved.append(record)
            approved_routes.add(page_route)
            if record["fips"]:
                approved_fips.add(record["fips"])
            raw = path.read_text(encoding="utf-8", errors="replace")
            path.write_text(add_adsense(raw), encoding="utf-8")

    # Existing noindex county pages are ad-free and not promoted as finished local work.
    for path in county_paths:
        if path in {item[0] for item in candidates}:
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        path.write_text(strip_ads(ensure_noindex(raw, "withheld-unfinished-county")), encoding="utf-8")

    # State hubs are navigation, not finished editorial pages. Keep them usable but ad-free/noindex.
    state_hubs = sorted(SITE.glob("counties/*/index.html"))
    for path in state_hubs:
        if path == SITE / "counties" / "index.html":
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        path.write_text(strip_ads(ensure_noindex(raw, "navigation-state-hub")), encoding="utf-8")

    # Consolidate thin FAQ leaves into the substantive hub and add temporary redirects.
    faq_leaves = sorted(SITE.glob("faq/*/index.html"))
    for path in faq_leaves:
        raw = path.read_text(encoding="utf-8", errors="replace")
        path.write_text(strip_ads(ensure_noindex(raw, "consolidated-faq-answer")), encoding="utf-8")

    # Guide pages must be substantial and source-based; navigation hubs remain ad-free.
    retained_guides: list[str] = []
    demoted_guides: list[dict[str, Any]] = []
    for path in sorted(SITE.glob("guides/*/index.html")):
        page = parse(path)
        words = word_count(page.text)
        external = [(href, label) for href, label in page.anchors if is_external(href)]
        raw = path.read_text(encoding="utf-8", errors="replace")
        interactive = "<form" in raw.lower() or "calculator" in page.h1.lower()
        minimum = 350 if interactive else 500
        if words < minimum or len(external) < 2:
            path.write_text(strip_ads(ensure_noindex(raw, "withheld-guide-quality")), encoding="utf-8")
            demoted_guides.append({"route": route(path), "main_words": words, "external_sources": len(external), "interactive": interactive})
        else:
            retained_guides.append(route(path))
            path.write_text(add_adsense(raw), encoding="utf-8")

    # Navigation/trust pages must not carry Auto ads.
    ad_free = [
        SITE / "counties" / "index.html", SITE / "guides" / "index.html",
        SITE / "providers" / "index.html", SITE / "septic-services-near-me" / "index.html",
        SITE / "privacy" / "index.html", SITE / "contact" / "index.html",
        SITE / "sources.html", SITE / "guides" / "sources.html",
    ]
    for path in ad_free:
        if path.exists():
            path.write_text(strip_ads(path.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")

    rewrite_faq_hub()
    rewrite_about()
    approved.sort(key=lambda item: (-item["local_detail_score"], item["shared_template_ratio"], -item["main_words"], item["route"]))
    build_homepage(approved, retained_guides)

    # County lookup retains all 3,144 FIPS records but only links directly to approved local pages.
    lookup_path = DATA / "county-lookup.json"
    lookup_data = json.loads(lookup_path.read_text(encoding="utf-8"))
    for row in lookup_data.get("counties", []):
        fips = clean(row.get("f"))
        if fips in approved_fips:
            row["v"] = True
            continue
        row["v"] = False
        state_slug = re.sub(r"[^a-z0-9]+", "-", clean(row.get("s")).lower()).strip("-")
        row["u"] = f"/counties/{state_slug}/"
        row["o"] = ""
        row["r"] = ""
    lookup_path.write_text(json.dumps(lookup_data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    # Withheld county and FAQ URLs redirect to useful hubs, so old indexed URLs do not expose thin pages.
    redirects_path = SITE / "_redirects"
    existing_redirects = redirects_path.read_text(encoding="utf-8", errors="replace") if redirects_path.exists() else ""
    existing_redirects = re.sub(r"(?s)\n?# BEGIN ADSENSE QUALITY RECOVERY.*?# END ADSENSE QUALITY RECOVERY\n?", "\n", existing_redirects)
    redirect_lines = ["# BEGIN ADSENSE QUALITY RECOVERY"]
    for path in county_paths:
        page_route = route(path)
        if page_route in approved_routes:
            continue
        parts = path.relative_to(SITE).parts
        redirect_lines.append(f"{page_route} /counties/{parts[1]}/ 302")
    for path in faq_leaves:
        redirect_lines.append(f"{route(path)} /faq/ 302")
    for item in demoted_guides:
        redirect_lines.append(f'{item["route"]} /guides/ 302')
    redirect_lines.append("# END ADSENSE QUALITY RECOVERY")
    redirects_path.write_text(existing_redirects.rstrip() + "\n\n" + "\n".join(redirect_lines) + "\n", encoding="utf-8")

    # Build a deliberately small sitemap: substantial editorial pages and approved local guides only.
    allowed = {
        f"{DOMAIN}/", f"{DOMAIN}/counties/", f"{DOMAIN}/guides/", f"{DOMAIN}/faq/",
        f"{DOMAIN}/about/", f"{DOMAIN}/privacy/", f"{DOMAIN}/contact/",
    }
    for page_route in retained_guides:
        allowed.add(DOMAIN + page_route)
    for page_route in approved_routes:
        allowed.add(DOMAIN + page_route)
    set_sitemap(allowed)

    repeated_approved = Counter()
    for item in approved:
        # Bucket the approved pages by rounded shared ratio and structural size only as a warning aid.
        repeated_approved[(round(item["shared_template_ratio"], 2), item["external_sources"], item["local_detail_score"])] += 1
    largest_bucket = max(repeated_approved.values(), default=0)
    report = {
        "schema_version": 1,
        "generated_at": TODAY,
        "recovery_mode": True,
        "policy": "Quality over page count: no hourly content mutation, no unfinished/templated county indexing, no ads on navigation or withheld pages.",
        "county_pages_scanned": len(county_paths),
        "previously_indexable_county_candidates": len(candidates),
        "quality_approved_counties": len(approved),
        "quality_withheld_counties": len(county_paths) - len(approved),
        "approved_county_fips": sorted(approved_fips),
        "approved_counties": approved,
        "demoted_counties": demoted,
        "state_hubs_noindex_ad_free": len(state_hubs),
        "faq_leaf_pages_consolidated": len(faq_leaves),
        "retained_long_form_guides": len(retained_guides),
        "retained_guide_routes": retained_guides,
        "demoted_guides": demoted_guides,
        "sitemap_urls": len(allowed),
        "largest_approved_structural_bucket": largest_bucket,
        "launch_notes": [
            "The national county/FIPS lookup remains available for all 3,144 county-equivalents.",
            "Unapproved county results route to an ad-free state hub instead of an unfinished county page.",
            "Old FAQ leaf URLs temporarily redirect to the comprehensive FAQ hub.",
            "The global provider search remains hidden until nationwide coverage is complete.",
        ],
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT_TEXT.write_text(
        "\n".join([
            "SepticScope AdSense/search quality recovery",
            f"Generated: {TODAY}",
            f"County pages scanned: {len(county_paths)}",
            f"Previously indexable county candidates: {len(candidates)}",
            f"Quality-approved county guides: {len(approved)}",
            f"Withheld county pages: {len(county_paths) - len(approved)}",
            f"State hubs made noindex/ad-free: {len(state_hubs)}",
            f"FAQ leaves consolidated: {len(faq_leaves)}",
            f"Retained long-form guides: {len(retained_guides)}",
            f"Final sitemap URLs: {len(allowed)}",
            "",
        ]),
        encoding="utf-8",
    )
    print(REPORT_TEXT.read_text(encoding="utf-8"), end="")
    return report


def check() -> int:
    if not REPORT.exists():
        raise SystemExit("Quality recovery report is missing")
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    errors: list[str] = []
    approved = int(report.get("quality_approved_counties", 0))
    retained_guides = int(report.get("retained_long_form_guides", 0))
    sitemap_count = int(report.get("sitemap_urls", 99999))
    if approved < 5:
        errors.append(f"Fewer than five locally differentiated county guides survived: {approved}")
    if approved > 175:
        errors.append(f"Too many county pages survived the recovery gate: {approved}")
    if retained_guides < 8:
        errors.append(f"Fewer than eight substantial national guides survived: {retained_guides}")
    if sitemap_count > 210:
        errors.append(f"Recovery sitemap is still too broad: {sitemap_count}")
    for path in SITE.rglob("*.html"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "noindex" in raw.lower() and (ADSENSE_CLIENT in raw or "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" in raw):
            errors.append(f"Noindex page still carries AdSense code: {route(path)}")
            if len(errors) >= 50:
                break
    home = (SITE / "index.html").read_text(encoding="utf-8", errors="replace")
    if "data-county-lookup-root" not in home or "Fewer pages, stronger reasons to trust each one" not in home:
        errors.append("Quality-first homepage is missing")
    if "3,144 county and county-equivalent pages" in home or "High-coverage state hubs" in home:
        errors.append("Homepage still markets page volume instead of value")
    faq = (SITE / "faq" / "index.html").read_text(encoding="utf-8", errors="replace")
    if word_count(parse(SITE / "faq" / "index.html").text) < 1000 or '"@type": "FAQPage"' not in faq:
        errors.append("Consolidated FAQ hub is not substantial or lacks FAQ schema")
    about = parse(SITE / "about" / "index.html")
    if word_count(about.text) < 700 or "How automation is used" not in about.text:
        errors.append("Editorial transparency page is incomplete")
    growth = json.loads((ROOT / "data" / "growth-links.json").read_text(encoding="utf-8"))
    if growth.get("links"):
        errors.append("Automated repetitive growth links are still active")
    workflow = (ROOT / ".github" / "workflows" / "hourly-growth-maintenance.yml").read_text(encoding="utf-8")
    if "cron:" in workflow or "--apply-one" in workflow:
        errors.append("Scheduled automatic content mutation is still enabled")
    if errors:
        print("QUALITY RECOVERY ERRORS:")
        for error in errors:
            print(" -", error)
        return 1
    print(f"PASS: quality recovery holds {approved} county guides, {retained_guides} guides, and {sitemap_count} sitemap URLs")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        return check()
    process()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
