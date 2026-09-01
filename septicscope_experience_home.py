"""National homepage and county-directory rendering for SepticScope."""
from septicscope_experience_common import *  # noqa: F401,F403

def verified_feature_cards(records: list[dict[str, Any]]) -> str:
    preferred = ["48121", "48085", "51059", "06065", "04013", "37119", "16001", "12011"]
    by_fips = {record["f"]: record for record in records if record["v"]}
    selected = [by_fips[fips] for fips in preferred if fips in by_fips][:6]
    if len(selected) < 6:
        used = {record["f"] for record in selected}
        for record in records:
            if record["v"] and record["f"] not in used:
                selected.append(record)
                used.add(record["f"])
            if len(selected) == 6:
                break
    return "".join(
        f'''<a class="ss-county-card" href="{record['u']}"><span class="ss-county-card__state">Verified · {html.escape(record['s'])}</span><h3>{html.escape(record['n'])}</h3><p>Permitting authority, local process, contacts and official sources.</p></a>'''
        for record in selected
    )


def write_homepage(records: list[dict[str, Any]], providers: list[dict[str, Any]]) -> None:
    provider_count = len(providers)
    county_cards = verified_feature_cards(records)
    website_schema = safe_json({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "SepticScope",
        "url": f"{DOMAIN}/",
        "description": "Local septic permitting, maintenance, troubleshooting and service-provider information.",
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{DOMAIN}/?q={{search_term_string}}",
            "query-input": "required name=search_term_string",
        },
    })
    page = f'''<!doctype html><html lang="en" data-septicscope-menu-ready="2"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SepticScope | Local Septic Rules, Services & Homeowner Guides</title><meta name="description" content="Search by ZIP, city or county for local septic permits, official contacts, homeowner guidance and source-checked service listings."><link rel="canonical" href="{DOMAIN}/">
<meta property="og:title" content="SepticScope | Local Septic Rules, Services & Homeowner Guides"><meta property="og:description" content="Find the septic information that applies to your property, then understand what to do next."><meta property="og:type" content="website"><meta property="og:url" content="{DOMAIN}/"><meta name="twitter:card" content="summary">
<link rel="stylesheet" href="/assets/septicscope-home.css"><link rel="stylesheet" href="/assets/septicscope-home-components.css"><script defer src="/assets/location-search.js"></script>{GA_TAG}{ADSENSE_TAG}<script type="application/ld+json">{website_schema}</script></head><body>{header()}
<main id="main-content">
<section class="ss-hero"><div class="ss-wrap ss-hero__grid"><div><span class="ss-eyebrow">Local answers for septic owners</span><h1>Find the septic rules and help that apply to your property.</h1><p class="ss-hero__lead">Search by ZIP code, city and state, or county. Get local permit contacts, practical homeowner guidance, and source-checked service options without digging through scattered websites.</p>{search_form('home-location')}
<ul class="ss-proof"><li>{ICONS['check']}All 3,144 U.S. counties</li><li>{ICONS['check']}Official sources shown</li><li>{ICONS['check']}No paid rankings</li></ul></div>
<aside class="ss-hero-panel" aria-label="Popular SepticScope starting points"><p class="ss-hero-panel__label">What do you need today?</p><div class="ss-task-list">
<a class="ss-task" href="/counties/"><span class="ss-task__icon">{ICONS['permit']}</span><span><strong>Permit or property records</strong><small>Find the local office and process</small></span><span class="ss-task__arrow">›</span></a>
<a class="ss-task" href="/providers/?service=pumping"><span class="ss-task__icon">{ICONS['pump']}</span><span><strong>Pumping or maintenance</strong><small>Browse source-checked local listings</small></span><span class="ss-task__arrow">›</span></a>
<a class="ss-task" href="/guides/septic-inspection-checklist/"><span class="ss-task__icon">{ICONS['inspect']}</span><span><strong>Buying or selling a home</strong><small>Know what an inspection should cover</small></span><span class="ss-task__arrow">›</span></a>
<a class="ss-task" href="/guides/septic-drainfield-repair-replacement/"><span class="ss-task__icon">{ICONS['repair']}</span><span><strong>Backup, odor or wet yard</strong><small>Understand warning signs and next steps</small></span><span class="ss-task__arrow">›</span></a></div><p class="ss-hero-panel__note">SepticScope does not replace your permitting authority, inspector, designer or contractor. We show the sources and the verification date so you know what to confirm.</p></aside></div></section>

<section class="ss-section"><div class="ss-wrap"><div class="ss-section-head"><div><span class="ss-eyebrow">Local service categories</span><h2>Start with the type of septic help you need.</h2></div><p>Service listings use public business information and the service areas stated by each provider. Listings are not endorsements or rankings.</p></div><div class="ss-service-grid">
<a class="ss-service-card" href="/providers/?service=pumping"><div><span class="ss-service-card__icon">{ICONS['pump']}</span><h3>Septic pumping</h3><p>Routine pump-outs, tank cleaning and emergency pumping.</p></div><span class="ss-service-card__link">Find pumping services →</span></a>
<a class="ss-service-card" href="/providers/?service=installation"><div><span class="ss-service-card__icon">{ICONS['install']}</span><h3>Installation</h3><p>Conventional, aerobic and replacement-system installation.</p></div><span class="ss-service-card__link">Find installers →</span></a>
<a class="ss-service-card" href="/providers/?service=inspection"><div><span class="ss-service-card__icon">{ICONS['inspect']}</span><h3>Inspections</h3><p>Real-estate, operational and accessible-component inspections.</p></div><span class="ss-service-card__link">Find inspectors →</span></a>
<a class="ss-service-card" href="/providers/?service=repairs"><div><span class="ss-service-card__icon">{ICONS['repair']}</span><h3>Repairs & maintenance</h3><p>Alarms, pumps, aerators, lines, controls and maintenance contracts.</p></div><span class="ss-service-card__link">Find repair help →</span></a></div></div></section>

<section class="ss-section ss-section--soft"><div class="ss-wrap"><div class="ss-section-head"><div><span class="ss-eyebrow">Three clear paths</span><h2>From local rules to the next practical step.</h2></div></div><div class="ss-path-grid">
<article class="ss-path-card"><h3>Locate your permitting authority</h3><p>Use the national county lookup to find verified local requirements or official government starting points.</p><a class="ss-text-link" href="/counties/">Search county guides</a></article>
<article class="ss-path-card"><h3>Understand the system or problem</h3><p>Use plain-language guides, checklists and calculators before deciding what service or paperwork you need.</p><a class="ss-text-link" href="/guides/">Explore homeowner guides</a></article>
<article class="ss-path-card"><h3>Compare local service options</h3><p>Review public service categories, stated coverage and contact information without copied ratings or paid ordering.</p><a class="ss-text-link" href="/providers/">Browse local services</a></article></div></div></section>

<section class="ss-section"><div class="ss-wrap"><div class="ss-section-head"><div><span class="ss-eyebrow">Popular homeowner tools</span><h2>Useful resources for ownership, maintenance and real estate.</h2></div><p>Built to answer the next question—not to stretch one answer across multiple thin pages.</p></div><div class="ss-guide-grid">
<a class="ss-guide-card" href="/guides/septic-tank-size-calculator/"><div class="ss-guide-card__top">{ICONS['calculator']}<span class="ss-guide-card__type">Calculator</span></div><div class="ss-guide-card__body"><h3>Septic tank size calculator</h3><p>Use documented state examples without pretending one national formula controls every permit.</p></div><span class="ss-guide-card__foot">Open calculator →</span></a>
<a class="ss-guide-card" href="/guides/septic-maintenance-checklist/"><div class="ss-guide-card__top">{ICONS['calendar']}<span class="ss-guide-card__type">Printable</span></div><div class="ss-guide-card__body"><h3>Maintenance checklist</h3><p>Track routine care, inspections, pumping history, records and annual property checks.</p></div><span class="ss-guide-card__foot">Use the checklist →</span></a>
<a class="ss-guide-card" href="/guides/septic-inspection-checklist/"><div class="ss-guide-card__top">{ICONS['inspect']}<span class="ss-guide-card__type">Home buying</span></div><div class="ss-guide-card__body"><h3>Inspection checklist</h3><p>Know what a useful septic inspection should review, document and explain.</p></div><span class="ss-guide-card__foot">Review inspection steps →</span></a>
<a class="ss-guide-card" href="/guides/types-of-septic-systems/"><div class="ss-guide-card__top">{ICONS['layers']}<span class="ss-guide-card__type">System guide</span></div><div class="ss-guide-card__body"><h3>Types of septic systems</h3><p>Compare conventional, aerobic, mound, drip and other common treatment approaches.</p></div><span class="ss-guide-card__foot">Compare systems →</span></a>
<a class="ss-guide-card" href="/guides/septic-system-lifespan/"><div class="ss-guide-card__top">{ICONS['home']}<span class="ss-guide-card__type">Planning</span></div><div class="ss-guide-card__body"><h3>System lifespan planning</h3><p>Separate tank age from whole-system condition and plan for inspection or replacement.</p></div><span class="ss-guide-card__foot">Plan ahead →</span></a>
<a class="ss-guide-card" href="/guides/septic-drainfield-repair-replacement/"><div class="ss-guide-card__top">{ICONS['repair']}<span class="ss-guide-card__type">Troubleshooting</span></div><div class="ss-guide-card__body"><h3>Drainfield repair vs. replacement</h3><p>Understand what should be evaluated before accepting a full replacement recommendation.</p></div><span class="ss-guide-card__foot">Understand the decision →</span></a></div></div></section>

<section class="ss-section"><div class="ss-wrap"><div class="ss-local-banner"><div><span class="ss-eyebrow">Local service directory pilot</span><h2>Practical county pages should help people do more than read rules.</h2><p>We have started adding source-checked septic pumping, installation, inspection, design and maintenance listings to local county pages. The first North Texas batch is live, and the same structured process can expand county by county.</p><div class="ss-local-banner__actions"><a class="ss-button" href="/providers/">Browse local services</a><a class="ss-button ss-button--ghost" href="/contact/">Report or suggest a listing</a></div></div><div class="ss-directory-preview"><div class="ss-directory-preview__number">{provider_count}</div><div class="ss-directory-preview__label">source-checked provider listings in the first live batch</div><ul><li><span>Denton County</span><span>Pumping · install · repair</span></li><li><span>Collin County</span><span>Design · inspect · maintain</span></li><li><span>Directory policy</span><span>Neutral, no ratings</span></li></ul></div></div></div></section>

<section class="ss-section ss-section--soft"><div class="ss-wrap"><div class="ss-section-head"><div><span class="ss-eyebrow">Featured local guides</span><h2>Source-checked county information, not generic location swaps.</h2></div><p>Every verified county page identifies the authority and displays the official sources used.</p></div><div class="ss-county-grid">{county_cards}</div><p style="margin:26px 0 0"><a class="ss-text-link" href="/counties/">Browse all 3,144 counties and county equivalents</a></p></div></section>

<section class="ss-section ss-section--dark"><div class="ss-wrap"><div class="ss-section-head"><div><span class="ss-eyebrow">Coverage at a glance</span><h2>A national structure with a strict verification line.</h2></div><p>Unfinished counties are withheld from search results until local requirements are supported by authoritative sources.</p></div><div class="ss-metrics"><div class="metric-card"><div class="metric">0</div><div class="metric-label">verified county guides</div></div><div class="metric-card"><div class="metric">0</div><div class="metric-label">FAQ articles</div></div><div class="metric-card"><div class="metric">0</div><div class="metric-label">septic guides</div></div><div class="metric-card"><div class="metric">{provider_count}</div><div class="metric-label">local provider listings</div></div></div></div></section>

<section class="ss-section"><div class="ss-wrap ss-method-grid"><div class="ss-method-copy"><span class="ss-eyebrow">How we publish</span><h2>Useful enough to trust. Structured enough to scale.</h2><p>Septic rules vary by state, county, city and delegated health district. SepticScope keeps regulatory facts tied to public sources while keeping business listings separate from permitting guidance.</p><p><a class="ss-text-link" href="/sources.html">Read the source standards</a></p></div><div class="ss-method-list"><article class="ss-method-item"><span class="ss-method-item__number">1</span><div><h3>Find the controlling source</h3><p>County, public-health, environmental, code or other recognized public authority.</p></div></article><article class="ss-method-item"><span class="ss-method-item__number">2</span><div><h3>Explain the process plainly</h3><p>Permits, site evaluation, inspections, maintenance and records before background filler.</p></div></article><article class="ss-method-item"><span class="ss-method-item__number">3</span><div><h3>Show what was checked</h3><p>Visible sources, review dates and a correction path on local guidance.</p></div></article><article class="ss-method-item"><span class="ss-method-item__number">4</span><div><h3>Keep directory claims narrow</h3><p>Only service areas and categories stated in public provider information are published.</p></div></article></div></div></section>

<section class="ss-final-cta"><div class="ss-wrap"><h2>Start with the property location. We’ll take you to the right local page.</h2><p>Search a ZIP code, city and state, or county—then move from local rules to homeowner guidance and service options.</p><a class="ss-button" href="#main-content" onclick="document.querySelector('[data-location-input]').focus();return false;">Search my location</a></div></section>
</main>{footer()}</body></html>'''
    (SITE / "index.html").write_text(page, encoding="utf-8")


def write_county_directory(records: list[dict[str, Any]]) -> None:
    states: dict[str, dict[str, Any]] = defaultdict(lambda: {"total": 0, "verified": 0, "slug": ""})
    for record in records:
        item = states[record["s"]]
        item["total"] += 1
        item["verified"] += int(record["v"])
        item["slug"] = record["state_slug"]
    state_cards = "".join(
        f'<a class="ss-state-card" href="/counties/{data["slug"]}/"><strong>{html.escape(state)}</strong><span>{data["verified"]} verified guide{("" if data["verified"] == 1 else "s")} · {data["total"]} locations</span></a>'
        for state, data in sorted(states.items())
    )
    page = f'''<!doctype html><html lang="en" data-septicscope-menu-ready="2"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>U.S. County Septic Lookup by ZIP, City or County | SepticScope</title><meta name="description" content="Search all 3,144 U.S. counties and county equivalents by ZIP code, city and state, or county name for local septic permits and official contacts."><link rel="canonical" href="{DOMAIN}/counties/"><link rel="stylesheet" href="/assets/septicscope-home.css"><link rel="stylesheet" href="/assets/septicscope-home-components.css"><script defer src="/assets/location-search.js"></script>{GA_TAG}{ADSENSE_TAG}</head><body>{header('counties')}<main id="main-content"><section class="ss-directory-hero"><div class="ss-wrap"><span class="ss-eyebrow">Nationwide septic lookup</span><h1>Find septic information for your location.</h1><p>Search by ZIP code, city and state, or county. Verified guides use official local sources; in-progress pages stay out of search results while connecting you to government starting points.</p>{search_form('directory-location')}</div></section><section class="ss-section"><div class="ss-wrap"><div class="ss-section-head"><div><span class="ss-eyebrow">Browse all states</span><h2>Every U.S. county and county equivalent.</h2></div><p>A verified count reflects source-checked local guidance—not merely whether a URL exists.</p></div><div class="ss-state-grid">{state_cards}</div></div></section></main>{footer()}</body></html>'''
    target = SITE / "counties" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")
