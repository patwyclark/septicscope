# SepticScope hourly growth maintenance

The `Hourly provider growth, link and SEO audit` GitHub Actions workflow runs at minute 23 of every hour and can also be started manually.

## What each run does

1. Builds the same production output used by Cloudflare Pages.
2. Reviews a rotating batch of 100 county or county-equivalent records.
3. Checks county-linked official installer, pumper, hauler, maintenance-provider, and licensed-professional directories that can be accessed without a paid search API.
4. Publishes at most one new evidence-qualified provider per reviewed county per run, then rebuilds the affected directory and county modules.
5. Reviews every indexable page against its mapped primary keyword, title, H1, description, canonical, and internal anchor text.
6. Audits every generated page and internal link, checks external government/source/provider links, and enforces AdSense and source-quality gates.
7. Commits `data/providers.json` only when new evidence-qualified records were added or existing records gained new supported county coverage.
8. Submits changed public URLs to IndexNow after a successful source-data commit.

Reviewing 100 counties is a throughput target, not a promise to publish 100 businesses. A business is published only when the source evidence passes the quality threshold. Ambiguous results are retained in the workflow artifact for later review and are not exposed publicly.

## Google Search research process

Google Search may be used manually during SepticScope research sessions to discover local septic companies. The search result itself is never treated as sufficient evidence. Before publication, the researcher opens the company-owned website or an official public-agency directory and confirms:

- Business name
- Public phone number
- Septic or onsite-wastewater services
- The stated county, city, or service area
- A source URL and review date
- Any public license or registration information that can be supported

The project does not scrape Google Search results from GitHub Actions. Google does not provide a free, unrestricted server-side search feed for this use, and automated scraping would be unreliable and prone to blocking. Hourly automation therefore uses free official public sources, while Google-discovered company records are added in reviewed batches through `data/providers.json`.

## Publication evidence rules

Ordinary provider records are neutrally ordered and are not endorsements. The system does not copy reviews, publish star ratings, infer a county from a nearby city, or treat a search-result snippet as evidence.

A company-site record requires all of the following:

- A company-owned website, not a marketplace or review aggregator
- Visible septic or onsite-wastewater service evidence
- An explicit relationship between the service and the county being reviewed
- A public business phone number
- A credible business name
- A stored verification URL and date
- Permission under the site's `robots.txt`

An official-directory record requires a county-specific government or public-agency list that identifies the business and a public phone number.

## Keyword policy

The hourly SEO process does not create `meta keywords`, repeat phrases blindly, or insert keywords merely to make a page different. Every indexable page must have a primary keyword in the generated keyword map, and the audit checks whether the title, H1, and description match that search intent.

Automatic edits are limited to missing essentials that can be repaired deterministically: title, meta description, and canonical URL. Weak intent matches are reported for evidence-based editorial work instead of being padded with repetitive text.

## Manual dry run

```bash
python build_site.py
python tools/provider_discovery.py \
  --county-limit 100 \
  --search-budget 0 \
  --dry-run \
  --report hourly-provider-report.json
python tools/seo_hourly_audit.py --site site --report hourly-seo-report.json
python audit_site.py
python audit_site.py --external
python adsense_audit.py
```

The provider, SEO, internal-link, external-link, and AdSense reports are retained as GitHub Actions artifacts for 14 days.
