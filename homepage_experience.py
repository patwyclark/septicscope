#!/usr/bin/env python3
'''Replace the sparse launch homepage with a useful national septic publisher hub.'''
from __future__ import annotations

from collections import Counter, defaultdict
from html import escape
import json
from pathlib import Path
import re

from provider_curated_experience import curated_provider_data
from septic_services_near_me import clean, county_fips, display_services

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


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def load_manifest() -> list[dict]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = data.get("records", [])
    if len(records) != 3144:
        raise RuntimeError(f"Homepage requires 3,144 county records, found {len(records)}")
    return records


def providers() -> list[dict]:
    rows = [
        row for row in curated_provider_data().get("providers", [])
        if isinstance(row, dict)
        and str(row.get("status", "active")).lower() in {"active", "verified"}
        and clean(row.get("business_name"))
    ]
    rows.sort(key=lambda row: (clean(row.get("business_name")).casefold(), clean(row.get("id"))))
    return rows


def county_summary(records: list[dict], provider_rows: list[dict]) -> tuple[dict[str, dict], list[dict]]:
    provider_counts: Counter[str] = Counter()
    for provider in provider_rows:
        for fips in county_fips(provider):
            provider_counts[fips] += 1

    by_fips: dict[str, dict] = {}
    states: dict[str, dict] = defaultdict(lambda: {"total": 0, "verified": 0, "providers": 0})
    for record in records:
        fips = clean(record.get("fips"))
        state = clean(record.get("state"))
        county = clean(record.get("county_or_equivalent_name"))
        url = clean(record.get("page_url"))
        verified = record.get("verification_status") == "verified" or record.get("indexability_status") == "indexable"
        item = {
            "fips": fips, "state": state, "abbr": STATE_ABBR.get(state, ""),
            "county": county, "url": url.removeprefix(DOMAIN), "verified": verified,
            "providers": provider_counts[fips],
        }
        by_fips[fips] = item
        states[state]["total"] += 1
        states[state]["verified"] += int(verified)
        states[state]["providers"] += provider_counts[fips]
    state_rows = [
        {"state": state, "abbr": STATE_ABBR.get(state, ""), "slug": slugify(state), **counts}
        for state, counts in states.items()
    ]
    return by_fips, state_rows


def provider_preview(provider_rows: list[dict], counties: dict[str, dict]) -> str:
    selected: list[dict] = []
    used_states: set[str] = set()
    for provider in sorted(provider_rows, key=lambda row: (-len(county_fips(row)), clean(row.get("business_name")).casefold())):
        state = clean(provider.get("state"))
        if state and state not in used_states:
            selected.append(provider)
            used_states.add(state)
        if len(selected) == 6:
            break
    if len(selected) < 6:
        for provider in provider_rows:
            if provider not in selected:
                selected.append(provider)
            if len(selected) == 6:
                break
    cards = []
    for provider in selected:
        name = clean(provider.get("business_name"))
        labels = display_services(provider)[:5]
        county_names = [
            f"{counties[fips]['county']}, {counties[fips]['abbr'] or counties[fips]['state']}"
            for fips in county_fips(provider) if fips in counties
        ]
        coverage = ", ".join(county_names[:3])
        if len(county_names) > 3:
            coverage += f" + {len(county_names) - 3} more"
        service_text = " · ".join(labels)
        query = name.replace("&", "%26")
        cards.append(
            f'<article class="home-provider-card"><p class="home-card-kicker">{escape(clean(provider.get("state")) or "Local service")}</p>'
            f'<h3>{escape(name)}</h3><p>{escape(service_text)}</p><p class="home-small">{escape(coverage)}</p>'
            f'<a href="/septic-services-near-me/?q={escape(query)}">View contact and source details →</a></article>'
        )
    return "".join(cards)


def featured_counties(records: list[dict], provider_rows: list[dict], counties: dict[str, dict]) -> str:
    provider_counts: Counter[str] = Counter()
    for provider in provider_rows:
        for fips in county_fips(provider):
            provider_counts[fips] += 1
    candidates = [
        counties[clean(record.get("fips"))] for record in records
        if clean(record.get("fips")) in counties and counties[clean(record.get("fips"))]["verified"]
    ]
    candidates.sort(key=lambda row: (-provider_counts[row["fips"]], row["state"], row["county"]))
    selected: list[dict] = []
    used_states: set[str] = set()
    for row in candidates:
        if row["state"] not in used_states:
            selected.append(row)
            used_states.add(row["state"])
        if len(selected) == 8:
            break
    return "".join(
        f'<a class="home-county-card" href="{escape(row["url"])}"><strong>{escape(row["county"])}, {escape(row["abbr"] or row["state"])}</strong><span>Verified county guide'
        + (f' · {row["providers"]} local provider record{"s" if row["providers"] != 1 else ""}' if row["providers"] else '')
        + '</span></a>'
        for row in selected
    )


def state_cards(states: list[dict]) -> str:
    selected = sorted(states, key=lambda row: (-row["verified"], -row["providers"], row["state"]))[:12]
    return "".join(
        f'<a class="home-state-card" href="/counties/{escape(row["slug"])}/"><strong>{escape(row["state"])}</strong>'
        f'<span>{row["verified"]} verified guides · {row["total"]} locations'
        + (f' · {row["providers"]} provider connections' if row["providers"] else '')
        + '</span></a>'
        for row in selected
    )


EXTRA_CSS = r'''
.home-hero-actions{display:flex;flex-wrap:wrap;gap:11px;margin-top:18px}.home-hero-actions a{display:inline-flex;padding:11px 15px;border-radius:11px;text-decoration:none;font-weight:850}.home-hero-actions a:first-child{background:var(--forest);color:#fff}.home-hero-actions a:last-child{border:1px solid var(--line);background:#fff}.home-service-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.home-service-card{border:1px solid var(--line);border-radius:18px;background:#fff;padding:21px;text-decoration:none;color:var(--ink);box-shadow:0 7px 24px rgba(18,61,53,.045)}.home-service-card:hover{transform:translateY(-2px);box-shadow:var(--shadow)}.home-service-card span{display:grid;place-items:center;width:42px;height:42px;border-radius:12px;background:var(--mint);font-size:1.2rem}.home-service-card h3{margin:14px 0 7px;color:var(--forest)}.home-service-card p{margin:0;color:var(--muted)}.home-provider-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.home-provider-card{border:1px solid var(--line);border-radius:17px;background:#fff;padding:19px}.home-provider-card h3{margin:4px 0 8px;color:var(--forest)}.home-provider-card p{color:var(--muted);margin:7px 0}.home-provider-card a{font-weight:850}.home-card-kicker{font-size:.74rem!important;text-transform:uppercase;letter-spacing:.1em;font-weight:900;color:var(--forest2)!important}.home-small{font-size:.87rem}.home-state-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:11px}.home-state-card,.home-county-card{border:1px solid var(--line);border-radius:13px;background:#fff;padding:14px;text-decoration:none;color:var(--ink)}.home-state-card strong,.home-county-card strong{display:block;color:var(--forest)}.home-state-card span,.home-county-card span{display:block;color:var(--muted);font-size:.82rem;margin-top:3px}.home-county-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:11px}.home-guide-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.home-guide{border:1px solid var(--line);border-radius:17px;padding:19px;background:var(--cream);text-decoration:none;color:var(--ink)}.home-guide strong{display:block;color:var(--forest);font-size:1.08rem}.home-guide span{display:block;color:var(--muted);margin-top:7px}.home-method{background:var(--forest);color:#fff;border-radius:25px;padding:34px;display:grid;grid-template-columns:1fr 1fr;gap:30px}.home-method h2,.home-method h3{color:#fff}.home-method p{color:#d6e6e0}.home-method-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.home-method-card{border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.08);border-radius:13px;padding:14px}.home-final-cta{background:var(--cream);border:1px solid var(--line);border-radius:24px;padding:34px;display:flex;justify-content:space-between;align-items:center;gap:28px}.home-final-cta h2{margin:0 0 8px;color:var(--forest)}.home-final-cta p{margin:0;color:var(--muted)}.home-final-cta a{flex:none;background:var(--forest);color:#fff;padding:13px 18px;border-radius:12px;text-decoration:none;font-weight:900}@media(max-width:930px){.home-service-grid,.home-provider-grid,.home-guide-grid{grid-template-columns:1fr 1fr}.home-state-grid{grid-template-columns:1fr 1fr}.home-county-grid{grid-template-columns:1fr 1fr}.home-method{grid-template-columns:1fr}}@media(max-width:650px){.home-service-grid,.home-provider-grid,.home-guide-grid,.home-state-grid,.home-county-grid,.home-method-grid{grid-template-columns:1fr}.home-final-cta{display:block}.home-final-cta a{display:inline-flex;margin-top:18px}}
'''


def build() -> None:
    if not SITE.is_dir() or not MANIFEST.exists():
        raise RuntimeError("Run the first inventory before the homepage experience")
    records = load_manifest()
    provider_rows = providers()
    counties, states = county_summary(records, provider_rows)
    verified_count = sum(1 for row in counties.values() if row["verified"])
    provider_count = len(provider_rows)
    provider_counties = len({fips for provider in provider_rows for fips in county_fips(provider)})
    guide_count = len(list((SITE / "guides").glob("*/index.html")))
    faq_count = len(list((SITE / "faq").glob("*/index.html")))
    completed_states = sum(1 for row in states if row["verified"] == row["total"])

    schema = {
        "@context": "https://schema.org", "@graph": [
            {"@type": "Organization", "@id": f"{DOMAIN}/#organization", "name": "SepticScope", "url": f"{DOMAIN}/"},
            {"@type": "WebSite", "@id": f"{DOMAIN}/#website", "url": f"{DOMAIN}/", "name": "SepticScope",
             "publisher": {"@id": f"{DOMAIN}/#organization"},
             "potentialAction": {"@type": "SearchAction", "target": f"{DOMAIN}/septic-services-near-me/?q={{search_term_string}}", "query-input": "required name=search_term_string"}},
        ],
    }
    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": "Can I find septic services by ZIP code?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. The Septic Services Near Me locator resolves a ZIP, city and state, or county to possible county coverage and filters source-reviewed provider records."}},
            {"@type": "Question", "name": "Does SepticScope issue septic permits?", "acceptedAnswer": {"@type": "Answer", "text": "No. SepticScope is an independent information resource. The applicable local or state agency controls permits, approvals, and records."}},
            {"@type": "Question", "name": "Are providers ranked?", "acceptedAnswer": {"@type": "Answer", "text": "No. Ordinary listings are neutrally ordered and are not endorsements. Users should verify current service area, credentials, insurance, availability, job scope, and price."}},
        ],
    }

    service_cards = [
        ("↧", "Septic pumping near me", "Find tank pumping, cleaning, holding-tank, filter, and access services.", "pumping"),
        ("✓", "Septic inspectors near me", "Find inspection, property-transfer, camera, certification, and evaluation services.", "inspection"),
        ("＋", "Septic installers near me", "Find system design, site evaluation, soil testing, installation, and permit support.", "installation"),
        ("!", "Septic repair near me", "Find troubleshooting, drainfield, replacement, locating, excavation, and emergency help.", "repair"),
        ("↻", "Septic maintenance near me", "Find aerobic, pump, control, filter, riser, and maintenance-contract service.", "maintenance"),
        ("▦", "Commercial septic service", "Find grease-trap, lift-station, septage, sewer-pump, and specialty providers.", "commercial"),
    ]
    service_html = "".join(
        f'<a class="home-service-card" href="/septic-services-near-me/?service={key}"><span>{icon}</span><h3>{title}</h3><p>{description}</p></a>'
        for icon, title, description, key in service_cards
    )
    guide_html = "".join([
        '<a class="home-guide" href="/guides/septic-maintenance-checklist/"><strong>Septic maintenance checklist</strong><span>Monthly, yearly, inspection, and pumping tasks in one practical plan.</span></a>',
        '<a class="home-guide" href="/guides/septic-inspection-checklist/"><strong>Septic inspection checklist</strong><span>Understand records, tank access, components, drainfield checks, and reports.</span></a>',
        '<a class="home-guide" href="/guides/septic-system-failure-signs/"><strong>Signs of septic failure</strong><span>Recognize backups, slow drains, odors, wet areas, alarms, and urgent next steps.</span></a>',
        '<a class="home-guide" href="/guides/septic-tank-pumping-cost/"><strong>Septic pumping cost factors</strong><span>Compare access, tank size, disposal, inspection, and emergency-service variables.</span></a>',
        '<a class="home-guide" href="/guides/septic-drainfield-repair-replacement/"><strong>Drainfield repair or replacement</strong><span>Separate localized repair possibilities from larger soil-treatment-area failures.</span></a>',
        '<a class="home-guide" href="/guides/types-of-septic-systems/"><strong>Types of septic systems</strong><span>Compare conventional, aerobic, mound, drip, chamber, and sand-filter systems.</span></a>',
    ])

    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SepticScope: Local Septic Rules, Services, Costs & Homeowner Guides</title><meta name="description" content="Find septic services near you, county permit guidance, official records, maintenance checklists, inspection help, troubleshooting, costs, and system guides in one source-checked resource."><link rel="canonical" href="{DOMAIN}/"><meta property="og:type" content="website"><meta property="og:title" content="SepticScope: Local Septic Help From Permit to Pumping"><meta property="og:description" content="Search septic services by ZIP, city, county, state, or service and find source-checked permit and homeowner guidance."><meta property="og:url" content="{DOMAIN}/"><link rel="stylesheet" href="/assets/septic-services-near-me.css"><style>{EXTRA_CSS}</style><script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}');</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c")}</script><script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False).replace("<", "\\u003c")}</script></head><body>
<a class="ssn-skip" href="#main">Skip to content</a><header class="ssn-header"><nav class="ssn-nav" aria-label="Primary"><a class="ssn-brand" href="/"><span class="ssn-mark">SS</span><span>SepticScope</span></a><div class="ssn-links"><a href="/counties/">County guides</a><a href="/guides/">Homeowner guides</a><a href="/faq/">FAQs</a><a class="ssn-nav-cta" href="/septic-services-near-me/">Septic Services Near Me</a></div></nav></header>
<main id="main"><section class="ssn-hero"><div class="ssn-hero-inner"><div><p class="ssn-eyebrow">Permits, providers, maintenance, costs, and troubleshooting</p><h1>The practical home base for everything septic.</h1><p class="ssn-lede">Find source-checked local septic services, county permit contacts, official records, inspection guidance, maintenance plans, cost explanations, system types, and urgent troubleshooting without bouncing between incomplete directories.</p><form class="ssn-search" action="/septic-services-near-me/" method="get"><div class="ssn-search-row"><label><span class="ssn-skip">Location</span><input type="search" name="q" placeholder="ZIP, City + State, County, or business name" autocomplete="postal-code"></label><label><span class="ssn-skip">Service</span><select name="service"><option value="">All septic services</option><option value="pumping">Pumping & cleaning</option><option value="inspection">Inspections & home sales</option><option value="installation">Design & installation</option><option value="repair">Repair & drainfield work</option><option value="maintenance">Aerobic & maintenance</option><option value="commercial">Commercial & specialty</option></select></label><button type="submit">Find local septic help</button></div><div class="ssn-search-tools"><span>Search all 3,144 U.S. counties and county-equivalents</span><a href="/counties/">Browse permit guides</a></div></form><div class="home-hero-actions"><a href="/septic-services-near-me/">Septic Services Near Me</a><a href="/guides/">Explore homeowner guides</a></div></div>
<aside class="ssn-hero-card"><p class="ssn-eyebrow" style="color:#cfe3dc">A better local-information model</p><h2>Start with the property and the job.</h2><div class="ssn-checks"><div class="ssn-check"><strong>1. Find the county</strong>ZIP and city searches resolve to likely county coverage; boundary warnings stay visible.</div><div class="ssn-check"><strong>2. Check the permit authority</strong>Verified county guides link to current official sources and local process details.</div><div class="ssn-check"><strong>3. Contact the right service</strong>Provider records separate pumping, inspections, design, installation, repair, and maintenance.</div></div></aside></div></section>
<div class="ssn-metrics"><div class="ssn-metric-grid"><div class="ssn-metric"><strong>{verified_count:,}</strong><span>verified county guides</span></div><div class="ssn-metric"><strong>{faq_count:,}</strong><span>FAQ articles</span></div><div class="ssn-metric"><strong>{guide_count:,}</strong><span>septic guides</span></div><div class="ssn-metric"><strong>{provider_count:,}</strong><span>source-reviewed service businesses</span></div></div></div>
<section class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Hire the right kind of help</p><h2>Septic services by job type</h2></div><p>Go directly to the local service you need. Listings show public contact details, published service coverage, documented services, credential notes, source links, and review dates.</p></div><div class="home-service-grid">{service_html}</div></section>
<section class="ssn-how"><div class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Growing local coverage</p><h2>Recently source-reviewed businesses</h2></div><p>{provider_count:,} active provider records currently connect to {provider_counties:,} counties. Coverage is expanded only when a company-owned or official source supports the location and services.</p></div><div class="home-provider-grid">{provider_preview(provider_rows, counties)}</div><div class="home-hero-actions"><a href="/septic-services-near-me/">Search all septic services near me</a><a href="/contact/">Suggest a business for review</a></div></div></section>
<section class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Local rules and records</p><h2>Featured county septic guides</h2></div><p>Verified guides identify the permitting authority, local starting points, official sources, records paths, and county-specific cautions where publicly documented.</p></div><div class="home-county-grid">{featured_counties(records, provider_rows, counties)}</div><div class="home-hero-actions"><a href="/counties/">Browse every county and county-equivalent</a><a href="/septic-services-near-me/">Search by ZIP or city</a></div></section>
<section class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Own, buy, sell, or repair with confidence</p><h2>Most useful homeowner guides</h2></div><p>Use connected checklists, explainers, calculators, system comparisons, and troubleshooting guides instead of isolated articles.</p></div><div class="home-guide-grid">{guide_html}</div><div class="home-hero-actions"><a href="/guides/">See all homeowner guides</a><a href="/faq/">Browse septic FAQs</a></div></section>
<section class="ssn-how"><div class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Browse by state</p><h2>High-coverage state hubs</h2></div><p>{completed_states} states or districts currently have complete verified county coverage. Every state hub distinguishes verified guides from in-progress help pages.</p></div><div class="home-state-grid">{state_cards(states)}</div><div class="home-hero-actions"><a href="/counties/">Browse all states</a></div></div></section>
<section class="ssn-section"><div class="home-method"><div><p class="ssn-eyebrow" style="color:#cfe3dc">Why SepticScope is different</p><h2>Built around useful evidence, not manufactured rankings.</h2><p>Regulations come from government, public-health, code, and recognized public sources. Provider details come from company-owned websites or official directories. Search snippets, copied reviews, and unsupported county claims are not publication evidence.</p><p><a style="color:#fff;font-weight:850" href="/about/">Read the research and correction standards →</a></p></div><div class="home-method-grid"><div class="home-method-card"><h3>Regulatory accuracy</h3><p>Local and state sources are separated, review dates are visible, and current agency instructions control.</p></div><div class="home-method-card"><h3>Transparent directory</h3><p>Ordinary businesses are neutrally ordered; sponsorship and affiliate relationships must be disclosed.</p></div><div class="home-method-card"><h3>Protected index quality</h3><p>Unfinished county pages remain noindex until the authority, process, and sources are supportable.</p></div><div class="home-method-card"><h3>Continuous quality checks</h3><p>Internal links, external sources, metadata, canonicals, sitemap behavior, and AdSense safeguards are audited.</p></div></div></div></section>
<section class="ssn-section"><div class="home-final-cta"><div><h2>Start with your location.</h2><p>Search by ZIP, city and state, county, business name, or septic service—and keep the permit guide one click away.</p></div><a href="/septic-services-near-me/">Find Septic Services Near Me</a></div></section></main>
<footer class="ssn-footer"><div class="ssn-footer-inner"><div class="ssn-footer-links"><a href="/septic-services-near-me/">Septic Services Near Me</a><a href="/counties/">County septic guides</a><a href="/providers/">Provider directory</a><a href="/guides/">Homeowner guides</a><a href="/faq/">FAQs</a><a href="/about/">About our research</a><a href="/privacy/">Privacy</a><a href="/contact/">Corrections & feedback</a></div><small>© 2026 SepticScope. Independent informational resource; not a government agency. Current local agency instructions and current contractor credentials control.</small></div></footer></body></html>'''

    home = SITE / "index.html"
    home.write_text(html, encoding="utf-8")
    if html.lower().count("<h1") != 1:
        raise RuntimeError("Homepage must contain exactly one H1")
    if html.count('href="/septic-services-near-me/"') < 4 or ">Septic Services Near Me<" not in html:
        raise RuntimeError("Homepage does not prominently expose Septic Services Near Me")
    if re.search(r"Browse\s+Indiana\s+septic", html, flags=re.I):
        raise RuntimeError("Obsolete Indiana-only homepage link remains")
    for label, value in (("verified county guides", verified_count), ("FAQ articles", faq_count), ("septic guides", guide_count)):
        visible = re.sub(r"<[^>]+>", " ", html)
        if not re.search(rf"\b{value:,}\s+{re.escape(label)}\b", visible, flags=re.I):
            raise RuntimeError(f"Homepage metric missing: {value:,} {label}")
    print(f"Homepage experience complete: {verified_count:,} verified counties; {provider_count:,} providers; {provider_counties:,} provider-covered counties")


if __name__ == "__main__":
    build()
