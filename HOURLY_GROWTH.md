# SepticScope hourly continuous growth

The `Hourly continuous SepticScope growth` GitHub Actions workflow runs at minute 23 of every hour and can also be started manually.

## Public-product rule

The homepage and `/counties/` always prioritize the nationally complete county-information lookup. Visitors can search by ZIP code, city and state, county and state, five-digit county FIPS code, or browser location.

The national `/septic-services-near-me/` and `/providers/` experiences remain `noindex,follow`, absent from the sitemap, and unlinked from public pages until **all 3,144 U.S. counties and county-equivalents have at least one source-reviewed provider relationship**. Provider research and supported county-local cards continue in the background; incomplete national search is not promoted.

## What each hourly run does

1. Builds the same production output used by Cloudflare Pages.
2. Regenerates the 3,144-location county search and verifies the homepage lookup.
3. Reviews a rotating batch of 100 county or county-equivalent records for free official installer, pumper, hauler, maintenance-provider, and licensed-professional sources.
4. Adds only evidence-qualified provider records and county relationships.
5. Regenerates supported county-local provider cards and the private background service dataset.
6. Recalculates the national provider launch status in `/data/service-directory-status.json`.
7. Keeps the global service search hidden unless all 3,144 county-equivalents have coverage.
8. Reads the generated internal-link graph, county coverage, provider coverage, keyword map, and source-review dates.
9. Applies one additional safe, compounding improvement when a useful opportunity exists.
10. Reviews every indexable page against its mapped primary keyword, title, H1, description, canonical, and internal anchor text.
11. Audits every generated page and internal link, checks external government/source/provider links, and enforces AdSense and source-quality gates.
12. Commits source-controlled changes only after every quality gate passes.
13. Waits for the exact commit to reach Cloudflare and submits only changed **public** URLs to IndexNow. Hidden service-directory routes are excluded.

The workflow is designed to keep making useful progress without forcing low-quality changes. When no defensible improvement is available, it records the next opportunities and makes no filler change.

## County lookup safeguards

The generated public lookup includes:

- All 3,144 counties and county-equivalents
- Unique five-digit county FIPS identifiers
- Verified versus in-progress source status
- Identified permitting authority when available
- Review date when available
- Direct county-page URLs
- ZIP and city/state resolution through public postal coordinates and FCC/Census county geocoding
- A warning that postal and city boundaries may cross county lines

CI and production smoke tests fail if the homepage search disappears, if the county dataset is incomplete or duplicated, if the county directory becomes noindex, or if a sample FIPS lookup such as Denton County `48121` is wrong.

## Provider discovery and publication policy

Reviewing 100 counties is a throughput target, not a promise to publish 100 businesses. A provider relationship is added only when source evidence passes the quality threshold. Ambiguous candidates remain private workflow diagnostics.

Google Search or another ordinary public search interface may be used manually to discover a possible business. The search result itself is never publication evidence. Before a record is accepted, the researcher opens a company-owned website or official public-agency directory and confirms:

- Business name and company-owned website
- Public phone number
- Public email and street or mailing address when published
- Septic or onsite-wastewater services
- Explicit county, city, ZIP, or service-area evidence
- Source URL and review date
- Public license, certification, or registration information when supportable
- Published hours or emergency availability when stated

Reviewed batches may be stored in `data/provider-expansion-*.json`. `provider_curated_experience.py` merges those batches with canonical providers and reviewed corrections. `tools/sync_curated_providers.py` validates unique IDs and county FIPS values, then flattens the layered catalog into `data/providers.json`.

The project does not scrape Google results from GitHub Actions and does not require a paid search API. Hourly automation uses free official public sources. Ordinary provider records are neutrally ordered and are not endorsements. The system does not copy reviews, publish star ratings, infer a county from a nearby office, or convert partial coverage into a countywide guarantee.

## Service launch gate

The launch status file reports:

```text
/data/service-directory-status.json
```

It includes:

- `public`
- `provider_records`
- `covered_counties`
- `required_counties` — always 3,144
- `remaining_counties`
- the exact launch requirement

When `public` is false:

- The homepage contains no service-finder or provider-directory link
- Public pages contain no links to those global routes
- `/septic-services-near-me/` is a noindex, non-searchable holding page
- `/providers/` is a noindex progress page without business cards
- Neither route appears in the sitemap
- AdSense is suppressed on the hidden global directory pages
- County-local provider cards may remain where source evidence supports them

When `public` becomes true, the complete service locator and provider directory can be published automatically and added to the sitemap.

## Continuous-growth link policy

`data/growth-links.json` records contextual internal links selected from the real generated page graph. A page may receive no more than three automated growth links.

The planner considers current incoming and outgoing links, page type, search intent, shared septic topic groups, state-to-county relationships, existing links, indexability, and target availability. It never inserts links into noindex pages, legal pages, or missing targets.

## Keyword policy

The hourly SEO process does not create `meta keywords`, repeat phrases blindly, or insert keywords merely to make a page different. Every indexable page must have a primary keyword in the generated keyword map, and the audit checks title, H1, description, canonical, and intent alignment.

The public county lookup targets county septic information, permits, records, authority, and FIPS-code intent. The unfinished global service routes remain noindex and do not compete for search visibility.

## Growth reports

Each production build publishes:

```text
/data/county-lookup.json
/data/service-directory-status.json
/data/continuous-growth-report.json
/data/septic-services-near-me.json
```

Each hourly run retains private diagnostics containing provider research results, rejected candidates, provider coverage gaps, the selected continuous-growth improvement, internal-link opportunities, source-review backlogs, national content gaps, keyword output, link audits, AdSense audits, and representative generated pages.

## Manual dry run

```bash
python build_site.py
python tools/provider_discovery.py \
  --county-limit 100 \
  --search-budget 0 \
  --dry-run \
  --report hourly-provider-report.json
python tools/continuous_growth.py \
  --site site \
  --state data/growth-links.json \
  --report hourly-continuous-growth-report.json
python tools/seo_hourly_audit.py --site site --report hourly-seo-report.json
node --check site/assets/county-lookup.js
node --check site/assets/septic-services-near-me.js
python audit_site.py
python audit_site.py --external
python adsense_audit.py
```
