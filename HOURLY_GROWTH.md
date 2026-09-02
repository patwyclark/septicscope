# SepticScope hourly continuous growth

The `Hourly continuous SepticScope growth` GitHub Actions workflow runs at minute 23 of every hour and can also be started manually.

## What each run does

1. Builds the same production output used by Cloudflare Pages.
2. Reviews a rotating batch of 100 county or county-equivalent records for free official installer, pumper, hauler, maintenance-provider, and licensed-professional sources.
3. Publishes only evidence-qualified provider records, then rebuilds the affected provider directory and county modules.
4. Reads the live generated internal-link graph, county coverage, provider coverage, keyword map, and source-review dates.
5. Applies one additional safe, compounding improvement when a useful opportunity exists. The first automatic improvement class is a contextual link between genuinely related SepticScope pages.
6. Produces a ranked growth report covering underlinked pages, verified counties without providers, source-review backlogs, and missing high-value national content clusters.
7. Reviews every indexable page against its mapped primary keyword, title, H1, description, canonical, and internal anchor text.
8. Audits every generated page and internal link, checks external government/source/provider links, and enforces AdSense and source-quality gates.
9. Commits `data/providers.json` and/or `data/growth-links.json` only after all quality gates pass.
10. Waits for the exact source commit to reach Cloudflare, then submits changed public URLs to IndexNow.

The workflow is designed to keep making useful progress without forcing low-quality changes. When no defensible automatic improvement is available, it records the next best opportunities in the diagnostic artifact and makes no filler change.

## Continuous-growth link policy

`data/growth-links.json` is the source-controlled record of contextual internal links selected from the real generated page graph. A page may receive no more than three automated growth links.

The planner considers:

- Current outgoing and incoming internal-link counts
- Page type and search intent
- Shared topic groups such as inspection/real estate, maintenance/pumping, failure/repair, system design, winter care, and permits/records
- State-to-county relationships
- Whether the source already links to the target
- Whether both pages are indexable and present in the current production build

The renderer groups approved links into one small “Related SepticScope resources” section. It never inserts links into noindex pages, legal pages, or missing targets.

## Provider discovery policy

Reviewing 100 counties is a throughput target, not a promise to publish 100 businesses. A business is published only when the source evidence passes the quality threshold. Ambiguous results are retained in the workflow artifact for later review and are not exposed publicly.

Google Search may be used manually during SepticScope research sessions to discover local septic companies. The search result itself is never treated as sufficient evidence. Before publication, the researcher opens the company-owned website or an official public-agency directory and confirms:

- Business name
- Public phone number
- Septic or onsite-wastewater services
- The stated county, city, or service area
- A source URL and review date
- Any public license or registration information that can be supported

The project does not scrape Google Search results from GitHub Actions. Hourly automation uses free official public sources, while Google-discovered company records are added in reviewed batches through `data/providers.json`.

Ordinary provider records are neutrally ordered and are not endorsements. The system does not copy reviews, publish star ratings, infer a county from a nearby city, or treat a search-result snippet as evidence.

## Keyword policy

The hourly SEO process does not create `meta keywords`, repeat phrases blindly, or insert keywords merely to make a page different. Every indexable page must have a primary keyword in the generated keyword map, and the audit checks whether the title, H1, and description match that search intent.

Automatic metadata edits are limited to missing essentials that can be repaired deterministically: title, meta description, and canonical URL. Weak intent matches are reported for evidence-based editorial work instead of being padded with repetitive text.

## Growth reports

Each production build publishes:

```text
/data/continuous-growth-report.json
```

Each hourly run also retains a private diagnostic artifact containing:

- Provider research results and rejected candidates
- The selected and applied continuous-growth improvement
- Top contextual internal-link opportunities
- Verified counties without provider coverage
- Verified guides due for source review
- High-value national content gaps not yet represented by a live page
- Keyword, internal-link, external-link, and AdSense audit output

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
python audit_site.py
python audit_site.py --external
python adsense_audit.py
```

To test one source-controlled improvement locally, add `--apply-one` to `tools/continuous_growth.py`, rebuild, and run the complete audit suite before committing.
