# SepticScope

SepticScope is a production static website for source-checked U.S. septic permitting information, county and county-equivalent lookup, homeowner education, and a growing local-service directory.

The product is organized around the full homeowner journey: locate the property, identify the permitting authority, understand the system or problem, and find a source-reviewed business for the needed work.

## Primary public experiences

- `/` — national publisher-style homepage connecting local rules, providers, costs, maintenance, inspections, troubleshooting, system types, state hubs, and county guides
- `/septic-services-near-me/` — direct ZIP, city/state, county, business-name, state, and service search for source-reviewed septic businesses
- `/providers/` — complete crawlable provider catalog with public contact and county-coverage information
- `/counties/` — all 3,144 U.S. counties and county-equivalents, with verified pages separated from noindex research/help pages
- `/guides/` — connected homeowner guides, checklists, calculators, comparisons, and troubleshooting resources

## Canonical production build

Run exactly:

```bash
python build_site.py
```

`build_site.py` is the single production orchestrator used by both Cloudflare Pages and GitHub Actions. It runs the preserved core generator, every registered county expansion, supplemental guides and tools, trust/privacy hardening, layered provider rendering, the service locator, the national homepage, source-controlled contextual growth links, conservative SEO safeguards, and the final national inventory. Do not add extra production-only build commands; that would allow CI and Cloudflare output to drift.

## Repository layout

- `build_site.py` — canonical production orchestrator
- `site_core_build.py` — preserved historical generator and county-expansion chain
- `*_expansion.py` — official-source county research batches
- `nationwide_county_lookup.py` — all 3,144 U.S. counties and county-equivalents, including useful noindex help pages for locations still under research
- `nationwide_data/` — compressed national county/county-equivalent source dataset
- `site_inventory.py` — national coverage manifest, keyword map, source catalog, provider inventory, quality summary and deployment fingerprint
- `homepage_experience.py` — final national homepage built from the current county, guide, and provider inventory
- `septic_services_near_me.py` — crawlable local-service locator and national county search payload
- `provider_experience.py` — builds the provider directory and source-checked local-service modules on county pages
- `provider_curated_experience.py` — combines canonical providers, reviewed corrections, and modular provider-expansion catalogs before rendering
- `continuous_growth_experience.py` — renders source-controlled contextual links selected by the growth planner
- `tools/sync_curated_providers.py` — validates and flattens layered provider records into the canonical catalog
- `tools/provider_discovery.py` — evidence-gated hourly business discovery for a rotating county batch
- `tools/continuous_growth.py` — ranks site-wide growth opportunities and may add one safe, compounding contextual link per run
- `tools/seo_hourly_audit.py` — reviews every indexable page against its mapped keyword and SEO essentials without keyword stuffing
- `tools/indexnow_submit.py` — notifies IndexNow participants about changed provider and county URLs
- `data/providers.json` — canonical source-controlled provider directory
- `data/provider-overrides.json` — reviewed provider corrections and replacements
- `data/provider-expansion-*.json` — modular, source-reviewed provider research batches
- `data/growth-links.json` — source-controlled contextual internal-link improvements selected from the real page graph
- `data/indexnow-key.txt` — public IndexNow key copied to the built site
- `data/quality-baseline.json` — regression guard for nationwide coverage and verified-guide count
- `audit_site.py` — internal, external-link and generated-site integrity checks
- `adsense_audit.py` — advertising, trust and county-source quality checks
- `HOURLY_GROWTH.md` — hourly workflow, evidence, operating and no-filler quality policy
- `site/` — generated output; created during builds and not committed

## Provider publication standard

A business record may be discovered through ordinary public web search, but search-result snippets are never publication evidence. Before a business is exposed, a company-owned website or official public directory must support the business identity, a public phone number, septic or onsite-wastewater services, and the geographic relationship shown.

Provider records can include:

- Business name and company-owned website
- Public phone, email, street or mailing address, city, state, and ZIP when published
- Pumping, inspection, installation, repair, maintenance, drainfield, aerobic, design, commercial, emergency, or other documented service categories
- Explicit county FIPS relationships and county-guide links
- Public credential or license notes, with a requirement to reconfirm current status
- Published availability or emergency-service notes
- Source URLs, verification dates, coverage notes, and correction routes
- Sponsorship and affiliate flags

Ordinary listings use neutral ordering and are not endorsements. The site does not copy consumer reviews, manufacture ratings, infer a county from a nearby city, or present a business as serving every property in a county when the source only supports partial coverage.

## Generated inventories

Every build publishes:

- `/build-info.json`
- `/data/national-coverage-manifest.json`
- `/data/keyword-map.json`
- `/data/source-catalog.json`
- `/data/provider-directory.json`
- `/data/septic-services-near-me.json`
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

Cloudflare Pages supplies `CF_PAGES_COMMIT_SHA`; the build records it in `/build-info.json`. A GitHub Actions production-smoke workflow waits for that SHA and confirms that the validated commit—including the homepage, service locator, provider JSON, assets, county directory, sitemap, and robots file—is actually live.

## Quality gates

On pushes and pull requests, GitHub Actions compiles Python sources, performs the complete production build, verifies national coverage and keyword manifests, validates provider records and the 3,144-location service index, checks JavaScript syntax, scans internal and external links, and enforces AdSense/source-quality safeguards.

A separate hourly workflow reviews a rotating 100-county batch for source-qualified local businesses, finds one additional safe compounding site improvement when one is available, audits every generated internal and external link, and checks every indexable page against its mapped search intent. Provider changes automatically regenerate the homepage, provider catalog, county modules, and `/septic-services-near-me/`, then submit changed public URLs through IndexNow after deployment. It commits source data only after all quality gates pass.

County rules must come from authoritative government, public-health, code, or other recognized public sources. Do not infer regulations or mark a county verified without supporting sources. Provider service areas must likewise be explicitly supported; a nearby city or search-result snippet is not enough. The hourly system may make no change when the only available options would reduce quality.
