# SepticScope structured data

## `providers.json`

This is the source-controlled provider directory. A provider record should use a stable ID and may contain:

- `business_name`
- `website`
- `public_phone`
- `city`, `state`, `zip_code`
- `counties_served` using county FIPS values when verified
- `zip_codes_served` only when publicly supported
- `service_categories`
- public license or registration information
- `source_urls`
- `date_added`, `date_last_verified`
- `status` (`active`, `closed`, `uncertain`, or `needs_review`)
- `sponsored` and `affiliate` booleans
- coverage notes

Never invent a service area, copy reviews, or use a business logo without permission. Ordinary listings must remain neutrally ordered. Paid placement must be labeled and linked appropriately.

## `quality-baseline.json`

This prevents national county coverage or verified-guide totals from silently regressing. The generated national coverage manifest remains the detailed current source of truth.
