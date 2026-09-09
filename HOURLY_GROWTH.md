# SepticScope research and quality workflow

The former scheduled hourly growth process is retired.

It was technically successful at building pages, inserting links, checking metadata, and passing link audits, but it optimized the wrong metric. Repeated scheduled changes increased the generated footprint without proving that each page offered enough original, locally useful value. After AdSense classified the site as low-value content, automatic mutation became a direct quality risk.

## Current operating mode

`.github/workflows/hourly-growth-maintenance.yml` is now **manual only**. It does not contain a cron schedule, does not run `--apply-one`, does not commit source files, and does not push to `main`.

A manual run can:

1. Build the same quality-gated output used by Cloudflare Pages.
2. Inspect a selected county batch for free official provider evidence in dry-run mode.
3. Enforce the AdSense/search quality-recovery policy.
4. Review titles, H1s, descriptions, canonicals, and mapped search intent.
5. Audit internal links and generated-site integrity.
6. Audit robots, sitemap, redirects, indexability, and canonicals.
7. Check external government and public source links.
8. Run the AdSense and content-quality audit.
9. Save all diagnostics without changing the repository.

## What is no longer allowed

- Publishing a page because an hourly schedule elapsed
- Adding one internal link every hour merely to create activity
- Treating a statewide template as a complete county guide
- Keeping a page indexable to preserve a page-count target
- Adding meta-keyword tags or repeating phrases for search engines
- Publishing provider service areas inferred from office location or search snippets
- Committing automated provider or content changes without editorial review
- Serving ads on unfinished, noindex, navigation-only, privacy, contact, or editorial-policy pages

`data/growth-links.json` remains empty unless a human-reviewed editorial update identifies a genuinely useful relationship that is not already represented in the page.

## County publication workflow

A county page should be upgraded only when the research adds meaningful local evidence. Useful additions include:

- The actual permitting authority for the legal parcel
- Direct local or delegated-agency contact information
- Application and form links
- Site or soil evaluation process
- Inspection stages and final approval
- Permit or as-built records process
- Current fee source
- County ordinance or local code
- Operating-permit or maintenance requirements
- Repair, replacement, transfer, or bedroom-addition procedures
- Locally supported provider information where appropriate

The final build independently measures content depth, source count, local-source evidence, local-detail signals, unfinished-language flags, and repeated-template share. A county page that fails is noindex, ad-free, absent from the sitemap, and not promoted as a finished guide.

## National guide publication workflow

A national guide needs a distinct user task, substantive original organization and explanation, primary public sources, clear limitations, and useful next steps. It must not exist merely as a keyword variation of another article.

Preferred work now includes improving a small number of durable resources:

- Buying or selling a home with septic
- Inspection scope and report quality
- Maintenance and pumping records
- Drainfield diagnosis and repair decisions
- System types and component identification
- Lifespan and replacement planning
- Seasonal and weather-related operation
- Permit and as-built record retrieval
- Costs explained by scope rather than unsupported national price promises

## Provider research

Provider discovery can use ordinary public search to find a possible company, but publication requires a company-owned website or official public directory that supports:

- Business identity
- Public phone and website
- Services actually offered
- Explicit county, city, ZIP, or service-area relationship
- Review date and source URL
- Public address, email, hours, or credential notes only when supported

Search snippets, copied reviews, ratings, and nearby-city assumptions are not evidence.

The global service finder remains withheld until all 3,144 county-equivalents have at least one source-reviewed provider relationship. Local provider information may remain on a county page only when the relationship is explicit and useful.

## Manual command sequence

```bash
python build_site.py
python tools/provider_discovery.py \
  --county-limit 100 \
  --search-budget 0 \
  --dry-run \
  --report provider-research-report.json
python quality_recovery.py --check
python tools/seo_hourly_audit.py --site site --report seo-quality-report.json
python audit_site.py
python tools/indexing_hygiene.py --site site
python audit_site.py --external
python adsense_audit.py
```

## Success criteria

The next phase is not measured by hourly commits. It is measured by:

- Growth in Google and Bing impressions for retained pages
- Improved click-through rate on pages already receiving impressions
- More queries reaching the top 20 and top 10
- Useful engagement with the county lookup and long-form guides
- Fewer thin or duplicate pages discovered by crawlers
- Successful AdSense review
- Revenue per useful session after approval

No change is preferable to a low-value change.
