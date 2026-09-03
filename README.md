# SepticScope

SepticScope is a production static website for source-checked U.S. septic permitting information, county and county-equivalent lookup, homeowner education, and a growing private provider dataset.

The public product is organized around the part of the homeowner journey that has complete national coverage today: locate the property, identify the likely legal county, find the county FIPS code and permitting authority, open official sources, and understand the next maintenance, inspection, repair, records, or design step.

## Primary public experiences

- `/` — national publisher-style homepage with a direct ZIP, city/state, county/state, and county-FIPS lookup
- `/counties/` — the full 3,144-location county information search, plus state browsing and verified/in-progress labels
- `/counties/{state}/{county}/` — source-checked county guidance when complete, or a useful noindex official-help page while research continues
- `/guides/` — connected homeowner guides, checklists, calculators, comparisons, and troubleshooting resources
- `/faq/` — plain-language answers connected to local permit and records research

## Service-directory launch gate

Provider research continues in the source data and on county pages where the geographic relationship is explicitly supported. The national `/septic-services-near-me/` and `/providers/` experiences are intentionally withheld from public navigation, marked `noindex,follow`, excluded from the sitemap, and stripped of searchable listing cards until **all 3,144 U.S. counties and county-equivalents have at least one source-reviewed provider relationship**.

This prevents a visitor from entering a ZIP code and receiving an empty national service result. Each build publishes `/data/service-directory-status.json` so the coverage total and remaining launch requirement are measurable. The global search is released automatically only after the 3,144-county gate is satisfied.

## County lookup behavior

The public location lookup accepts:

- Five-digit ZIP code
- City and state
- County and state
- County name alone when unambiguous enough to show choices
- Five-digit county FIPS code, including searches such as `FIPS 48121`
- Browser geolocation when the visitor grants permission

ZIP and city searches use public postal coordinates and public FCC/Census county geocoding. Because postal and municipal boundaries can cross county lines, results explicitly tell users to confirm the property’s legal county before relying on permit information.

Each result can show the county or county-equivalent name, state, five-digit FIPS code, source-verification status, date reviewed, identified permitting authority, and a link to the applicable county page.

## Canonical production build

Run exactly:

```bash
python build_site.py
```

`build_site.py` is the single production orchestrator used by both Cloudflare Pages and GitHub Actions. It runs the preserved core generator, every registered county expansion, supplemental guides and tools, trust/privacy hardening, layered provider rendering, the background service dataset, the national county lookup, the homepage, the service-directory launch gate, contextual growth links, conservative SEO safeguards, and the final national inventory.

## Repository layout

- `build_site.py` — canonical production orchestrator
- `site_core_build.py` — preserved historical generator and county-expansion chain
- `*_expansion.py` — official-source county research batches
- `nationwide_county_lookup.py` — all 3,144 U.S. counties and county-equivalents, including useful noindex help pages for locations still under research
- `nationwide_data/` — compressed national county/county-equivalent source dataset
- `site_inventory.py` — national coverage manifest, keyword map, source catalog, provider inventory, quality summary and deployment fingerprint
- `county_lookup_experience.py` — public ZIP, city/state, county/state, FIPS, and geolocation search
- `homepage_experience.py` — final national homepage centered on county information and homeowner tasks
- `septic_services_near_me.py` — builds the background provider and 3,144-county data needed for the future global service search
- `septic_service_quality.py` — enforces the 3,144-county service-directory publication gate and removes premature public links
- `provider_experience.py` — renders source-reviewed service modules on supported county pages and the gated global directory page
- `provider_curated_experience.py` — combines canonical providers, reviewed corrections, and modular provider-expansion catalogs before rendering
- `continuous_growth_experience.py` — renders source-controlled contextual links selected by the growth planner
- `tools/sync_curated_providers.py` — validates and flattens layered provider records into the canonical catalog
- `tools/provider_discovery.py` — evidence-gated hourly provider discovery for a rotating county batch
- `tools/continuous_growth.py` — ranks site-wide growth opportunities and may add one safe, compounding contextual link per run
- `tools/seo_hourly_audit.py` — reviews every indexable page against its mapped keyword and SEO essentials without keyword stuffing
- `tools/indexnow_submit.py` — notifies IndexNow participants only about changed public URLs
- `data/providers.json` — canonical source-controlled provider dataset
- `data/provider-overrides.json` — reviewed provider corrections and replacements
- `data/provider-expansion-*.json` — modular, source-reviewed provider research batches
- `data/growth-links.json` — source-controlled contextual internal-link improvements selected from the real page graph
- `audit_site.py` — internal, external-link and generated-site integrity checks
- `adsense_audit.py` — advertising, trust and county-source quality checks
- `HOURLY_GROWTH.md` — hourly workflow, evidence, operating and no-filler quality policy
- `site/` — generated output; created during builds and not committed

## Provider publication standard

A business may be discovered through ordinary public web search, but a search-result snippet is never publication evidence. Before a provider can be tied to a county, a company-owned website or official public directory must support the business identity, a public phone number, septic or onsite-wastewater services, and the geographic relationship shown.

Provider records can include:

- Business name and company-owned website
- Public phone, email, street or mailing address, city, state, and ZIP when published
- Pumping, inspection, installation, repair, maintenance, drainfield, aerobic, design, commercial, emergency, or other documented services
- Explicit county FIPS relationships
- Public credential or license notes, with a requirement to reconfirm current status
- Published availability or emergency-service notes
- Source URLs, verification dates, coverage notes, and correction routes
- Sponsorship and affiliate flags

Ordinary records are neutrally ordered and are not endorsements. SepticScope does not copy consumer reviews, manufacture ratings, infer countywide coverage from a nearby office address, or present partial coverage as a guarantee for every property.

## Generated inventories

Every build publishes:

- `/build-info.json`
- `/data/national-coverage-manifest.json`
- `/data/county-lookup.json`
- `/data/keyword-map.json`
- `/data/source-catalog.json`
- `/data/provider-directory.json`
- `/data/septic-services-near-me.json`
- `/data/service-directory-status.json`
- `/data/project-audit-summary.json`
- `/data/project-audit-summary.txt`
- `/data/hourly-seo-build-report.json`
- `/data/continuous-growth-report.json`

A county is counted as verified only when its final page is indexable and contains both a permitting-authority section and visible official sources. Page existence alone is not verification.

## Cloudflare Pages

- Repository: `patwyclark/septicscope`
- Production branch: `main`
- Framework preset: None
- Build command: `python build_site.py`
- Build output directory: `site`
- Root directory: repository root
- Production domain: `https://septicscope.com`

Cloudflare Pages supplies `CF_PAGES_COMMIT_SHA`; the build records it in `/build-info.json`. The production-smoke workflow waits for that exact SHA and confirms that the county lookup, 3,144-location payload, homepage, noindex service gate, sitemap, robots file, county pages, guides, and reported metrics are actually live.

## Quality gates

On pushes and pull requests, GitHub Actions compiles Python sources, performs the complete production build, verifies all 3,144 county records and FIPS identifiers, checks JavaScript syntax, validates the provider coverage gate, scans internal and external links, reviews keyword and canonical behavior, and enforces AdSense/source-quality safeguards.

The hourly workflow reviews a rotating 100-county batch for source-qualified provider evidence, finds one additional safe compounding site improvement when one is available, audits every generated internal and external link, and checks every indexable page against its mapped search intent. It continues expanding the private provider dataset and county-local modules, but excludes `/providers/` and `/septic-services-near-me/` from public search-engine notifications until the national launch gate is complete.

County rules must come from authoritative government, public-health, code, or other recognized public sources. Provider service areas must likewise be explicitly supported. The hourly system may make no change when the only available options would reduce quality.
