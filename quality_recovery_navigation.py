#!/usr/bin/env python3
"""Rebuild navigation hubs so they do not promote quality-withheld pages."""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
REPORT = SITE / "data" / "adsense-quality-recovery.json"
DOMAIN = "https://septicscope.com"
GA = "G-F6RB8YERCM"

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

GUIDES = {
    "/guides/buying-a-house-with-septic/": (
        "Buying a house with a septic system",
        "A detailed due-diligence path for permits, as-built records, inspection scope, site review, transaction contingencies, repair questions, and post-closing care.",
        "Home buying",
    ),
    "/guides/septic-maintenance-checklist/": (
        "Septic maintenance checklist",
        "Organize routine use, annual property checks, inspection, pumping history, records, alarms, filters, and professional maintenance responsibilities.",
        "Ownership",
    ),
    "/guides/septic-inspection-checklist/": (
        "Septic inspection checklist",
        "Understand records review, tank access, sludge and scum measurements, components, drainfield observations, report limitations, and follow-up questions.",
        "Inspection",
    ),
    "/guides/septic-drainfield-repair-replacement/": (
        "Drainfield repair versus replacement",
        "Separate localized component problems from soil-treatment-area failure and understand what evidence should support a major replacement recommendation.",
        "Troubleshooting",
    ),
    "/guides/types-of-septic-systems/": (
        "Types of septic systems",
        "Compare conventional, chamber, drip, aerobic, mound, and sand-filter systems while keeping local design approval and maintenance requirements in view.",
        "System basics",
    ),
    "/guides/septic-system-lifespan/": (
        "Septic system lifespan and replacement planning",
        "Plan around records, materials, components, maintenance, loading, soil, groundwater, and condition instead of relying on a single expiration age.",
        "Planning",
    ),
    "/guides/septic-system-winter-care/": (
        "Frozen septic systems and winter care",
        "Recognize freeze risks, avoid unsafe thawing shortcuts, protect insulation, manage seasonal properties, and know when professional help is needed.",
        "Seasonal care",
    ),
    "/guides/septic-tank-size-calculator/": (
        "Septic tank-size planning tool",
        "Use documented state examples as a preliminary planning reference without presenting a universal formula as a permit-ready local answer.",
        "Planning tool",
    ),
}

STYLE = r''':root{--ink:#17221f;--muted:#5d6965;--forest:#123d35;--forest2:#1e6253;--line:#d9e2dc;--mint:#eaf4ef;--cream:#faf6ec;--paper:#fffdfa;--max:1080px}*{box-sizing:border-box}body{margin:0;background:var(--paper);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}a{color:var(--forest2);text-underline-offset:3px}header,footer{border-block:1px solid var(--line);background:#fff}.nav,.foot,main{max-width:var(--max);margin:auto;padding:18px 24px}.brand{font-weight:950;color:var(--forest);text-decoration:none}.nav{display:flex;justify-content:space-between;gap:18px;align-items:center}.nav-links{display:flex;flex-wrap:wrap;gap:16px}.nav-links a{text-decoration:none;font-weight:780;color:var(--ink)}main{padding-top:56px;padding-bottom:80px}h1{font-size:clamp(2.45rem,6vw,4.65rem);line-height:1.02;letter-spacing:-.045em;color:var(--forest);margin:.18em 0}h2{color:var(--forest);font-size:clamp(1.6rem,3vw,2.35rem);line-height:1.14}.lead{font-size:1.17rem;color:#46534f;max-width:830px}.eyebrow{font-size:.77rem;font-weight:950;letter-spacing:.13em;text-transform:uppercase;color:var(--forest2)}.notice{background:var(--cream);border:1px solid #eadcbc;border-radius:16px;padding:18px;margin:26px 0}.guide-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:25px}.guide-card{border:1px solid var(--line);border-radius:17px;padding:20px;background:#fff;text-decoration:none;color:var(--ink)}.guide-card strong{display:block;color:var(--forest);font-size:1.15rem}.guide-card span{display:block;color:var(--muted);margin-top:8px}.guide-card small{display:inline-block;background:var(--mint);color:var(--forest2);padding:4px 8px;border-radius:999px;font-weight:850;margin-bottom:10px}.path{display:grid;grid-template-columns:repeat(3,1fr);gap:13px;margin-top:20px}.path article{border:1px solid var(--line);border-radius:15px;padding:18px;background:var(--mint)}.path h3{color:var(--forest);margin-top:0}.sources{background:var(--cream);border-radius:18px;padding:22px;margin-top:36px}.foot{color:var(--muted)}@media(max-width:760px){.guide-grid,.path{grid-template-columns:1fr}.nav-links a:nth-child(n+3){display:none}}'''


def load_report() -> dict:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    if not data.get("recovery_mode"):
        raise RuntimeError("Quality recovery report is not active")
    return data


def write_guides(report: dict) -> None:
    retained = [route for route in report.get("retained_guide_routes", []) if route in GUIDES]
    if len(retained) < 8:
        raise RuntimeError(f"Guide hub expected eight quality-reviewed guides; found {len(retained)}")
    cards = "".join(
        f'<a class="guide-card" href="{escape(route)}"><small>{escape(GUIDES[route][2])}</small><strong>{escape(GUIDES[route][0])}</strong><span>{escape(GUIDES[route][1])}</span></a>'
        for route in retained
    )
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Septic System Guides: Maintenance, Inspection, Buying & Repair</title><meta name="description" content="Use quality-reviewed septic system guides for home buying, maintenance, inspections, drainfields, system types, lifespan, winter care, and tank-size planning."><link rel="canonical" href="{DOMAIN}/guides/"><style>{STYLE}</style><script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA}');</script></head><body><header><nav class="nav"><a class="brand" href="/">SepticScope</a><div class="nav-links"><a href="/counties/">County lookup</a><a href="/faq/">Septic FAQ</a><a href="/about/">Research standards</a></div></nav></header><main><p><a href="/">Home</a> / Septic system guides</p><p class="eyebrow">Focused homeowner resources</p><h1>Septic system guides for real ownership decisions</h1><p class="lead">These guides survived SepticScope’s quality review because each addresses a distinct homeowner task with substantive explanation, public sources, practical cautions, and a clear next step. Shorter or overlapping pages have been withheld or consolidated instead of remaining in the public guide library.</p><div class="notice"><strong>Start with the property location when a rule or permit is involved.</strong> System design, setbacks, inspection requirements, operating permits, transfer rules, and professional credentials vary by jurisdiction. Use the <a href="/counties/">county lookup</a> before treating general guidance as a property-specific answer.</div><div class="guide-grid">{cards}</div><section><h2>Choose the guide that matches the decision</h2><div class="path"><article><h3>Before buying or selling</h3><p>Use the homebuyer and inspection guides together. One organizes the transaction and records search; the other helps define inspection scope and report quality.</p></article><article><h3>For routine ownership</h3><p>Use the maintenance checklist, system-type guide, and winter guidance to build a record-based care plan rather than relying on a single universal pumping interval.</p></article><article><h3>When a problem or major expense appears</h3><p>Use the drainfield and lifespan guides to separate observations, component failures, maintenance needs, current malfunction, and long-term replacement planning.</p></article></div></section><section class="sources"><h2>How these guides are maintained</h2><p>Regulatory statements are tied to government, public-health, code, university Extension, or other recognized public sources. Cost, design, and diagnosis claims are qualified when local conditions or professional evaluation control. Broken links, outdated agency instructions, and material factual issues can be reported through <a href="/contact/">Contact &amp; Feedback</a>.</p><p><a href="/about/">Read the editorial, automation, advertising, and correction standards →</a></p></section></main><footer><div class="foot">© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/contact/">Corrections & feedback</a></div></footer></body></html>'''
    (SITE / "guides" / "index.html").write_text(html, encoding="utf-8")


def write_state_hubs(report: dict) -> None:
    approved_by_state: dict[str, list[dict]] = {}
    for item in report.get("approved_counties", []):
        parsed = urlparse(str(item.get("url", "")))
        parts = parsed.path.strip("/").split("/")
        if len(parts) != 3 or parts[0] != "counties":
            continue
        approved_by_state.setdefault(parts[1], []).append(item)
    for path in sorted(SITE.glob("counties/*/index.html")):
        state_slug = path.parent.name
        state = STATE_NAMES.get(state_slug, state_slug.replace("-", " ").title())
        approved = sorted(approved_by_state.get(state_slug, []), key=lambda item: str(item.get("county_label", "")))
        cards = "".join(
            f'<a class="guide-card" href="{escape(urlparse(str(item["url"])).path)}"><small>Published local guide</small><strong>{escape(str(item["county_label"]))}</strong><span>{escape(str(item.get("authority") or "Local authority and sources identified"))}</span></a>'
            for item in approved
        )
        if not cards:
            cards = '<div class="notice"><strong>No county-specific guide in this state currently passes the stricter publication standard.</strong> Use the official state and local government directories below while the local research is rebuilt.</div>'
        state_source = f"https://www.usa.gov/states/{state_slug}"
        html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(state)} Septic Research and Official Starting Points | SepticScope</title><meta name="description" content="Find quality-reviewed county septic guides and official state or local government starting points for {escape(state)} while additional local research is completed."><meta name="robots" content="noindex,follow"><link rel="canonical" href="{DOMAIN}/counties/{escape(state_slug)}/"><meta name="septicscope-quality-status" content="navigation-state-hub"><style>{STYLE}</style><script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA}');</script></head><body><header><nav class="nav"><a class="brand" href="/">SepticScope</a><div class="nav-links"><a href="/counties/">County lookup</a><a href="/guides/">Guides</a><a href="/faq/">FAQ</a></div></nav></header><main><p><a href="/counties/">All states</a> / {escape(state)}</p><p class="eyebrow">Navigation and official starting points</p><h1>{escape(state)} septic information</h1><p class="lead">SepticScope is re-reviewing county pages under a stricter local-value standard. The published guides below contain enough local authority, process, contact, record, fee, inspection, rule, or source detail to remain public. Other county pages are withheld rather than presented as finished local research.</p><div class="guide-grid">{cards}</div><section class="sources"><h2>Get official help while local research is in progress</h2><ul><li><a href="{escape(state_source)}" rel="nofollow">USA.gov — official {escape(state)} government directory</a></li><li><a href="https://www.usa.gov/state-local-governments" rel="nofollow">USA.gov — state and local government directory</a></li><li><a href="https://www.epa.gov/septic/state-septic-system-program-contacts" rel="nofollow">U.S. EPA — state septic program contacts</a></li></ul><p>Ask which agency has onsite-wastewater authority for the legal parcel, then confirm permits, site or soil evaluation, approved design, inspections, setbacks, fees, operating requirements, maintenance obligations, records, and current professional credentials.</p></section></main><footer><div class="foot">© 2026 SepticScope · <a href="/about/">Research standards</a> · <a href="/contact/">Corrections & feedback</a></div></footer></body></html>'''
        path.write_text(html, encoding="utf-8")


def main() -> None:
    report = load_report()
    write_guides(report)
    write_state_hubs(report)
    guides = (SITE / "guides" / "index.html").read_text(encoding="utf-8")
    for route in report.get("demoted_guides", []):
        value = route.get("route") if isinstance(route, dict) else None
        if value and value in guides:
            raise RuntimeError(f"Guide hub still promotes a quality-withheld page: {value}")
    print(f"Recovery navigation rebuilt: 8 guide cards; {len(list(SITE.glob('counties/*/index.html')))} ad-free state hubs")


if __name__ == "__main__":
    main()
