#!/usr/bin/env python3
"""Build a national septic-information homepage centered on county lookup."""
from __future__ import annotations

from collections import defaultdict
from html import escape
import json
from pathlib import Path
import re

from county_lookup_experience import LOOKUP_CSS, lookup_form

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
MANIFEST = SITE / "data" / "national-coverage-manifest.json"
DOMAIN = "https://septicscope.com"
GA_MEASUREMENT_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"

STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
}

HOME_CSS = r'''
.home-hero-actions{display:flex;flex-wrap:wrap;gap:11px;margin-top:18px}.home-hero-actions a{display:inline-flex;padding:11px 15px;border-radius:11px;text-decoration:none;font-weight:850}.home-hero-actions a:first-child{background:var(--forest);color:#fff}.home-hero-actions a:last-child{border:1px solid var(--line);background:#fff}.home-topic-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.home-topic-card{border:1px solid var(--line);border-radius:18px;background:#fff;padding:21px;text-decoration:none;color:var(--ink);box-shadow:0 7px 24px rgba(18,61,53,.045)}.home-topic-card:hover{transform:translateY(-2px);box-shadow:var(--shadow)}.home-topic-icon{display:grid;place-items:center;width:42px;height:42px;border-radius:12px;background:var(--mint);font-size:1.2rem;font-weight:900;color:var(--forest)}.home-topic-card h3{margin:14px 0 7px;color:var(--forest)}.home-topic-card p{margin:0;color:var(--muted)}.home-state-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:11px}.home-state-card,.home-county-card{border:1px solid var(--line);border-radius:13px;background:#fff;padding:14px;text-decoration:none;color:var(--ink)}.home-state-card strong,.home-county-card strong{display:block;color:var(--forest)}.home-state-card span,.home-county-card span{display:block;color:var(--muted);font-size:.82rem;margin-top:3px}.home-county-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:11px}.home-guide-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.home-guide{border:1px solid var(--line);border-radius:17px;padding:19px;background:var(--cream);text-decoration:none;color:var(--ink)}.home-guide strong{display:block;color:var(--forest);font-size:1.08rem}.home-guide span{display:block;color:var(--muted);margin-top:7px}.home-method{background:var(--forest);color:#fff;border-radius:25px;padding:34px;display:grid;grid-template-columns:1fr 1fr;gap:30px}.home-method h2,.home-method h3{color:#fff}.home-method p{color:#d6e6e0}.home-method-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.home-method-card{border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.08);border-radius:13px;padding:14px}.home-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.home-step{border:1px solid var(--line);border-radius:17px;padding:20px;background:#fff}.home-step-number{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--forest);color:#fff;font-weight:900}.home-step h3{margin:14px 0 7px;color:var(--forest)}.home-step p{margin:0;color:var(--muted)}.home-final-cta{background:var(--cream);border:1px solid var(--line);border-radius:24px;padding:34px;display:flex;justify-content:space-between;align-items:center;gap:28px}.home-final-cta h2{margin:0 0 8px;color:var(--forest)}.home-final-cta p{margin:0;color:var(--muted)}.home-final-cta a{flex:none;background:var(--forest);color:#fff;padding:13px 18px;border-radius:12px;text-decoration:none;font-weight:900}@media(max-width:930px){.home-topic-grid,.home-guide-grid,.home-steps{grid-template-columns:1fr 1fr}.home-state-grid{grid-template-columns:1fr 1fr}.home-county-grid{grid-template-columns:1fr 1fr}.home-method{grid-template-columns:1fr}}@media(max-width:650px){.home-topic-grid,.home-guide-grid,.home-state-grid,.home-county-grid,.home-method-grid,.home-steps{grid-template-columns:1fr}.home-final-cta{display:block}.home-final-cta a{display:inline-flex;margin-top:18px}}
'''


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def load_records() -> list[dict]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = data.get("records", [])
    if len(records) != 3144:
        raise RuntimeError(f"Homepage requires 3,144 county records; found {len(records)}")
    return records


def county_rows(records: list[dict]) -> list[dict]:
    rows = []
    for record in records:
        state = clean(record.get("state"))
        url = clean(record.get("page_url"))
        if not url.startswith(DOMAIN + "/"):
            continue
        rows.append({
            "county": clean(record.get("county_or_equivalent_name")),
            "state": state,
            "abbr": clean(record.get("state_abbreviation")) or STATE_ABBR.get(state, ""),
            "url": url.removeprefix(DOMAIN),
            "verified": record.get("verification_status") == "verified",
            "authority": clean(record.get("official_regulating_authority")),
            "reviewed": clean(record.get("date_last_reviewed")),
            "fips": clean(record.get("fips")),
        })
    return rows


def featured_counties(rows: list[dict]) -> str:
    preferred = ["48121", "48085", "04013", "06065", "37119", "16001", "12011", "53033"]
    by_fips = {row["fips"]: row for row in rows if row["verified"]}
    selected = [by_fips[fips] for fips in preferred if fips in by_fips]
    used = {row["fips"] for row in selected}
    if len(selected) < 8:
        for row in sorted((item for item in rows if item["verified"]), key=lambda item: (item["state"], item["county"])):
            if row["fips"] in used:
                continue
            selected.append(row)
            used.add(row["fips"])
            if len(selected) == 8:
                break
    cards = []
    for row in selected[:8]:
        detail = f'County FIPS {row["fips"]}'
        if row["authority"]:
            detail += " · authority identified"
        cards.append(
            f'<a class="home-county-card" href="{escape(row["url"])}"><strong>{escape(row["county"])}, {escape(row["abbr"] or row["state"])}</strong><span>Verified county guide · {escape(detail)}</span></a>'
        )
    return "".join(cards)


def state_cards(records: list[dict]) -> tuple[str, int]:
    states: dict[str, dict] = defaultdict(lambda: {"total": 0, "verified": 0})
    for record in records:
        state = clean(record.get("state"))
        states[state]["total"] += 1
        states[state]["verified"] += int(record.get("verification_status") == "verified")
    complete = sum(values["total"] == values["verified"] for values in states.values())
    selected = sorted(states.items(), key=lambda pair: (-pair[1]["verified"], pair[0]))[:12]
    cards = "".join(
        f'<a class="home-state-card" href="/counties/{escape(slugify(state))}/"><strong>{escape(state)}</strong><span>{values["verified"]} verified guides · {values["total"]} counties/equivalents</span></a>'
        for state, values in selected
    )
    return cards, complete


def build() -> None:
    if not SITE.is_dir() or not MANIFEST.exists():
        raise RuntimeError("Run the first inventory before the homepage experience")
    records = load_records()
    rows = county_rows(records)
    verified_count = sum(row["verified"] for row in rows)
    guide_count = len(list((SITE / "guides").glob("*/index.html")))
    faq_count = len(list((SITE / "faq").glob("*/index.html")))
    state_html, completed_states = state_cards(records)

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": f"{DOMAIN}/#organization", "name": "SepticScope", "url": f"{DOMAIN}/"},
            {
                "@type": "WebSite",
                "@id": f"{DOMAIN}/#website",
                "url": f"{DOMAIN}/",
                "name": "SepticScope",
                "publisher": {"@id": f"{DOMAIN}/#organization"},
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": f"{DOMAIN}/counties/?q={{search_term_string}}",
                    "query-input": "required name=search_term_string",
                },
            },
        ],
    }
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": "Can I find county septic information by ZIP code?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. The county lookup can resolve a ZIP code or city and state to one or more possible counties, then link to the appropriate SepticScope county information page."}},
            {"@type": "Question", "name": "What is a county FIPS code?", "acceptedAnswer": {"@type": "Answer", "text": "A county FIPS code is a five-digit federal geographic identifier made from the two-digit state code and three-digit county or county-equivalent code."}},
            {"@type": "Question", "name": "Why can a ZIP code return more than one county?", "acceptedAnswer": {"@type": "Answer", "text": "ZIP and city boundaries do not always match county boundaries. Confirm the legal county in the property record before relying on permit information."}},
            {"@type": "Question", "name": "Does SepticScope issue septic permits?", "acceptedAnswer": {"@type": "Answer", "text": "No. SepticScope is an independent information resource. The current permitting authority and its current instructions control."}},
        ],
    }

    topics = [
        ("P", "Septic permits and applications", "Find the authority, local starting point, official sources, and process notes for the property county.", "/counties/"),
        ("R", "Septic records and as-builts", "Use county guidance to locate permit histories, site plans, inspection records, and records-request contacts.", "/faq/how-do-i-find-my-septic-system-records/"),
        ("I", "Buying, selling, or inspecting", "Prepare for records review, tank access, inspection scope, reports, and local transfer requirements.", "/guides/septic-inspection-checklist/"),
        ("M", "Maintenance and pumping planning", "Build a practical care schedule around household use, system type, inspections, and pumping history.", "/guides/septic-maintenance-checklist/"),
        ("!", "Backups, odors, alarms, or wet yards", "Recognize failure warnings, reduce wastewater use, protect people from sewage exposure, and choose the next step.", "/faq/what-causes-a-drainfield-to-fail/"),
        ("S", "System types, sizing, and replacement", "Compare conventional and advanced systems and understand why site conditions and permits control design.", "/guides/types-of-septic-systems/"),
    ]
    topic_html = "".join(
        f'<a class="home-topic-card" href="{href}"><span class="home-topic-icon">{escape(icon)}</span><h3>{escape(title)}</h3><p>{escape(description)}</p></a>'
        for icon, title, description, href in topics
    )
    guide_html = "".join([
        '<a class="home-guide" href="/guides/septic-maintenance-checklist/"><strong>Septic maintenance checklist</strong><span>Monthly, annual, inspection, pumping, and recordkeeping tasks in one plan.</span></a>',
        '<a class="home-guide" href="/guides/septic-inspection-checklist/"><strong>Septic inspection checklist</strong><span>Understand records, access, components, drainfield observations, and written reports.</span></a>',
        '<a class="home-guide" href="/guides/septic-tank-size-calculator/"><strong>Septic tank-size planning tool</strong><span>Use documented examples without pretending one national rule controls every permit.</span></a>',
        '<a class="home-guide" href="/guides/septic-drainfield-repair-replacement/"><strong>Drainfield repair or replacement</strong><span>Separate localized problems from broader soil-treatment-area failure.</span></a>',
        '<a class="home-guide" href="/guides/types-of-septic-systems/"><strong>Types of septic systems</strong><span>Compare conventional, aerobic, mound, drip, chamber, and sand-filter approaches.</span></a>',
        '<a class="home-guide" href="/guides/septic-system-lifespan/"><strong>Septic system lifespan</strong><span>Separate tank age from the condition of pumps, controls, piping, and the drainfield.</span></a>',
    ])

    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SepticScope: County Septic Permits, Records, Codes & Homeowner Guides</title><meta name="description" content="Search by ZIP, city, county, state, or county FIPS code for septic permit guidance, official contacts, records starting points, inspections, maintenance, troubleshooting, and system guides."><link rel="canonical" href="{DOMAIN}/"><meta property="og:type" content="website"><meta property="og:title" content="SepticScope: Find the Septic Information for Your Property"><meta property="og:description" content="Search all U.S. counties and county-equivalents for septic permits, records, official contacts, FIPS codes, and practical homeowner guidance."><meta property="og:url" content="{DOMAIN}/"><link rel="stylesheet" href="/assets/septic-services-near-me.css"><style>{LOOKUP_CSS}{HOME_CSS}</style><script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}');</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script><script defer src="/assets/county-lookup.js"></script><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c")}</script><script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False).replace("<", "\\u003c")}</script></head><body>
<a class="ssn-skip" href="#main">Skip to content</a><header class="ssn-header"><nav class="ssn-nav" aria-label="Primary"><a class="ssn-brand" href="/"><span class="ssn-mark">SS</span><span>SepticScope</span></a><div class="ssn-links"><a class="ssn-nav-cta" href="/counties/">Find my county</a><a href="/guides/">Homeowner guides</a><a href="/faq/">FAQs</a><a href="/about/">Research standards</a></div></nav></header>
<main id="main"><section class="ssn-hero"><div class="ssn-hero-inner"><div><p class="ssn-eyebrow">County permits, official contacts, records, codes, and homeowner help</p><h1>Find the septic information that applies to your property.</h1><p class="ssn-lede">Search by ZIP code, city and state, county and state, or county FIPS code. Open the correct local page for permit guidance, official sources, records starting points, inspections, maintenance, troubleshooting, and system planning.</p><div id="county-lookup">{lookup_form()}</div><div class="home-hero-actions"><a href="/counties/">Browse every county</a><a href="/guides/">Explore homeowner guides</a></div></div><aside class="ssn-hero-card"><p class="ssn-eyebrow" style="color:#cfe3dc">Start with the legal county</p><h2>Why location comes first</h2><div class="ssn-checks"><div class="ssn-check"><strong>ZIPs can cross county lines</strong>The lookup may return more than one possible county. Confirm the property record.</div><div class="ssn-check"><strong>Authority varies by location</strong>A county, health district, city, state, or delegated office may control the septic process.</div><div class="ssn-check"><strong>Verified and in-progress pages are labeled</strong>Source-checked local guides are separated from official-help pages still under research.</div></div></aside></div></section>
<div class="ssn-metrics"><div class="ssn-metric-grid"><div class="ssn-metric"><strong>{verified_count:,}</strong><span>verified county guides</span></div><div class="ssn-metric"><strong>{faq_count:,}</strong><span>FAQ articles</span></div><div class="ssn-metric"><strong>{guide_count:,}</strong><span>septic guides</span></div><div class="ssn-metric"><strong>3,144</strong><span>county and county-equivalent pages</span></div></div></div>
<section class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">One site for the full homeowner journey</p><h2>Start with what you need to do</h2></div><p>County information stays connected to practical guides so you can move from authority and records to inspection, maintenance, troubleshooting, or replacement planning.</p></div><div class="home-topic-grid">{topic_html}</div></section>
<section class="ssn-how"><div class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Three checks before acting</p><h2>Use local information without guessing</h2></div><p>Septic rules can change by location, project type, property conditions, and system type.</p></div><div class="home-steps"><article class="home-step"><span class="home-step-number">1</span><h3>Confirm the county</h3><p>Use the property record when a ZIP, city, subdivision, or mailing address overlaps county boundaries.</p></article><article class="home-step"><span class="home-step-number">2</span><h3>Identify the authority</h3><p>Open the county page and verify which local, regional, municipal, or state office controls the work.</p></article><article class="home-step"><span class="home-step-number">3</span><h3>Confirm the exact project path</h3><p>New systems, repairs, replacements, alterations, home sales, records requests, and maintenance may follow different processes.</p></article></div></div></section>
<section class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Local rules and official sources</p><h2>Featured county septic guides</h2></div><p>Verified guides identify the permitting authority, official sources, review date, local process, and county-specific cautions where public evidence supports them.</p></div><div class="home-county-grid">{featured_counties(rows)}</div><div class="home-hero-actions"><a href="/counties/">Search all 3,144 county pages</a></div></section>
<section class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Own, buy, sell, maintain, or repair</p><h2>Most useful homeowner guides</h2></div><p>Use connected checklists, explainers, calculators, comparisons, and troubleshooting resources instead of isolated thin articles.</p></div><div class="home-guide-grid">{guide_html}</div><div class="home-hero-actions"><a href="/guides/">See all homeowner guides</a><a href="/faq/">Browse septic FAQs</a></div></section>
<section class="ssn-how"><div class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Browse by state</p><h2>High-coverage state hubs</h2></div><p>{completed_states} states or districts currently have complete verified county coverage. Every state hub distinguishes source-checked guides from in-progress official-help pages.</p></div><div class="home-state-grid">{state_html}</div><div class="home-hero-actions"><a href="/counties/">Browse all states and counties</a></div></div></section>
<section class="ssn-section"><div class="home-method"><div><p class="ssn-eyebrow" style="color:#cfe3dc">Why SepticScope is different</p><h2>Built around useful evidence, not location-name swaps.</h2><p>Regulatory statements come from government, public-health, code, and other recognized public sources. Review dates and sources stay visible, and unfinished county research remains clearly labeled.</p><p><a style="color:#fff;font-weight:850" href="/about/">Read the research and correction standards →</a></p></div><div class="home-method-grid"><div class="home-method-card"><h3>Regulatory accuracy</h3><p>State and local responsibilities are separated, and current agency instructions control.</p></div><div class="home-method-card"><h3>Transparent source status</h3><p>Verified guides and in-progress official-help pages are not presented as equivalent.</p></div><div class="home-method-card"><h3>Protected index quality</h3><p>Unfinished county pages remain noindex until local authority, process, and sources are supportable.</p></div><div class="home-method-card"><h3>Continuous quality checks</h3><p>Internal links, external sources, metadata, canonicals, sitemap behavior, and AdSense safeguards are audited.</p></div></div></div></section>
<section class="ssn-section"><div class="home-final-cta"><div><h2>Start with the property location.</h2><p>Search a ZIP, city and state, county and state, or county FIPS code to open the correct septic information page.</p></div><a href="#county-lookup">Find my county information</a></div></section></main>
<footer class="ssn-footer"><div class="ssn-footer-inner"><div class="ssn-footer-links"><a href="/counties/">County lookup</a><a href="/guides/">Homeowner guides</a><a href="/faq/">FAQs</a><a href="/about/">About our research</a><a href="/privacy/">Privacy</a><a href="/contact/">Corrections & feedback</a></div><small>© 2026 SepticScope. Independent informational resource; not a government agency. Current local agency instructions control.</small></div></footer></body></html>'''

    home = SITE / "index.html"
    home.write_text(html, encoding="utf-8")
    lower = html.lower()
    if lower.count("<h1") != 1:
        raise RuntimeError("Homepage must contain exactly one H1")
    if "data-county-lookup-root" not in html or "/assets/county-lookup.js" not in html:
        raise RuntimeError("Homepage county lookup was not generated")
    if "/septic-services-near-me/" in lower or 'href="/providers/' in lower:
        raise RuntimeError("Incomplete global service-directory links remain on the homepage")
    if re.search(r"Browse\s+Indiana\s+septic", html, flags=re.I):
        raise RuntimeError("Obsolete Indiana-only homepage link remains")
    visible = re.sub(r"<[^>]+>", " ", html)
    for label, value in (("verified county guides", verified_count), ("FAQ articles", faq_count), ("septic guides", guide_count)):
        if not re.search(rf"\b{value:,}\s+{re.escape(label)}\b", visible, flags=re.I):
            raise RuntimeError(f"Homepage metric missing: {value:,} {label}")
    print(f"Homepage experience complete: county lookup restored; {verified_count:,} verified counties; service search hidden")


if __name__ == "__main__":
    build()
