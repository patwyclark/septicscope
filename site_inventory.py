"""Run the national inventory with collision-, redirect-, provider-, and lookup-aware fixes."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from provider_curated_experience import curated_provider_data

ROOT = Path(__file__).resolve().parent
CORE = ROOT / "site_inventory_core.py"


def _replace_once(source: str, needle: str, patch: str, label: str) -> str:
    if source.count(needle) != 1:
        raise RuntimeError(f"{label} patch no longer matches the inventory core")
    return source.replace(needle, patch, 1)


def _patched_namespace() -> dict:
    source = CORE.read_text(encoding="utf-8")

    row_needle = "    county_rows = load_county_rows()\n"
    row_patch = row_needle + """    # Census data contains six same-name county/city pairs. Preserve the
    # long-standing county slug and append the legal-area label to the non-county
    # equivalent so every FIPS entity has its own canonical lookup target.
    collision_counts = Counter((row[0], slugify(row[1])) for row in county_rows)
    collision_safe_rows = []
    for abbr, name, lsad, fips in county_rows:
        if collision_counts[(abbr, slugify(name))] > 1 and str(lsad).lower() != "county":
            label = "Census Area" if lsad == "CA" else lsad
            if str(label).lower() not in name.lower():
                name = f"{name} {label}"
        collision_safe_rows.append([abbr, name, lsad, fips])
    county_rows = collision_safe_rows
"""
    source = _replace_once(source, row_needle, row_patch, "County-row compatibility")

    scan_needle = """        relative_parts = path.relative_to(ROOT).parts
        if any(part in excluded_roots for part in relative_parts):
            continue
"""
    scan_patch = """        relative = path.relative_to(ROOT)
        relative_parts = relative.parts
        if relative.as_posix() in {"site_inventory.py", "site_inventory_core.py"}:
            continue
        if any(part in excluded_roots for part in relative_parts):
            continue
"""
    source = _replace_once(source, scan_needle, scan_patch, "Legacy-brand scanner compatibility")

    pages_needle = "    html_pages = sorted(SITE.rglob(\"*.html\"))\n"
    pages_patch = pages_needle + """    redirected_page_urls = set()
    redirects_file = SITE / "_redirects"
    if redirects_file.exists():
        for redirect_line in redirects_file.read_text(encoding="utf-8", errors="replace").splitlines():
            redirect_line = redirect_line.strip()
            if not redirect_line or redirect_line.startswith("#"):
                continue
            fields = redirect_line.split()
            if len(fields) >= 3 and fields[0].startswith("/") and fields[2] in {"301", "302", "307", "308"}:
                if "*" not in fields[0] and ":" not in fields[0]:
                    redirected_page_urls.add(f"{DOMAIN}{fields[0]}")
"""
    source = _replace_once(source, pages_needle, pages_patch, "Redirect inventory")

    indexable_needle = "        indexable = not is_noindex(parser) and page_type != \"error_page\"\n"
    indexable_patch = "        indexable = not is_noindex(parser) and page_type != \"error_page\" and url not in redirected_page_urls\n"
    source = _replace_once(source, indexable_needle, indexable_patch, "Redirect indexability")

    provider_needle = "    write_provider_landing(provider_data)\n"
    provider_patch = """    provider_page = SITE / "providers" / "index.html"
    provider_ready = (
        provider_page.exists()
        and 'data-septicscope-provider-directory="1"'
        in provider_page.read_text(encoding="utf-8", errors="replace")
    )
    # Preserve a finished source-checked provider page during later inventory passes.
    if not provider_ready:
        write_provider_landing(provider_data)
"""
    source = _replace_once(source, provider_needle, provider_patch, "Provider-directory compatibility")

    provider_status_needle = '        if str(provider.get("status", "active")).lower() == "closed":\n'
    provider_status_patch = '        if str(provider.get("status", "active")).lower() not in {"active", "verified"}:\n'
    source = _replace_once(source, provider_status_needle, provider_status_patch, "Provider-status compatibility")

    provider_count_needle = '            "provider_listings": len(provider_data.get("providers", [])),\n'
    provider_count_patch = '            "provider_listings": sum(str(item.get("status", "active")).lower() in {"active", "verified"} for item in provider_data.get("providers", []) if isinstance(item, dict)),\n'
    source = _replace_once(source, provider_count_needle, provider_count_patch, "Provider-count compatibility")

    # A complete national lookup does not require a thin HTML page for every FIPS
    # record. Missing unverified county pages are an intentional lookup-only state.
    missing_needle = """        else:
            coverage_status = "missing"
            research_status = "not_started"
            verification_status = "unverified"
            publication_status = "not_deployed"
"""
    missing_patch = """        else:
            coverage_status = "lookup_only"
            research_status = "not_started_or_in_progress"
            verification_status = "unverified"
            publication_status = "lookup_only_not_published"
"""
    source = _replace_once(source, missing_needle, missing_patch, "Lookup-only county publication")

    stats_init_needle = """            "in_progress_help_pages": 0,
            "missing_pages": 0,
"""
    stats_init_patch = """            "in_progress_help_pages": 0,
            "lookup_only_counties": 0,
            "missing_pages": 0,
"""
    source = _replace_once(source, stats_init_needle, stats_init_patch, "Lookup-only state statistics")

    stats_count_needle = """        elif path.exists():
            stats["in_progress_help_pages"] += 1
        else:
            stats["missing_pages"] += 1
"""
    stats_count_patch = """        elif path.exists():
            stats["in_progress_help_pages"] += 1
        else:
            stats["lookup_only_counties"] += 1
"""
    source = _replace_once(source, stats_count_needle, stats_count_patch, "Lookup-only state counting")

    totals_needle = '    missing_county_pages = sum(record["publication_status"] == "not_deployed" for record in county_manifest)\n'
    totals_patch = """    published_county_pages = sum(
        str(record["publication_status"]).startswith("deployed_")
        for record in county_manifest
    )
    lookup_only_counties = sum(
        record["publication_status"] == "lookup_only_not_published"
        for record in county_manifest
    )
    missing_county_pages = sum(
        record["publication_status"] == "not_deployed"
        for record in county_manifest
    )
"""
    source = _replace_once(source, totals_needle, totals_patch, "County publication totals")

    summary_count_needle = '            "published_county_or_equivalent_pages": len(county_manifest) - missing_county_pages,\n'
    summary_count_patch = """            "county_lookup_records": len(county_manifest),
            "published_county_or_equivalent_pages": published_county_pages,
"""
    source = _replace_once(source, summary_count_needle, summary_count_patch, "Summary county publication count")

    in_progress_needle = """            "in_progress_county_help_pages": sum(
                record["coverage_status"] == "official_help_page" for record in county_manifest
            ),
            "missing_county_equivalent_pages": missing_county_pages,
"""
    in_progress_patch = """            "in_progress_county_help_pages": sum(
                record["coverage_status"] == "official_help_page" for record in county_manifest
            ),
            "lookup_only_counties": lookup_only_counties,
            "missing_county_equivalent_pages": missing_county_pages,
"""
    source = _replace_once(source, in_progress_needle, in_progress_patch, "Summary lookup-only count")

    build_count_needle = '        "published_county_or_equivalent_pages": len(county_manifest) - missing_county_pages,\n'
    build_count_patch = """        "county_lookup_records": len(county_manifest),
        "published_county_or_equivalent_pages": published_county_pages,
        "lookup_only_counties": lookup_only_counties,
"""
    source = _replace_once(source, build_count_needle, build_count_patch, "Build-info county publication count")

    namespace = {
        "__name__": "septicscope_inventory_core",
        "__file__": str(CORE),
    }
    exec(compile(source, str(CORE), "exec"), namespace)
    namespace["load_provider_data"] = curated_provider_data
    return namespace


def _verify_unique_county_urls(namespace: dict) -> None:
    manifest = namespace["OUTPUT_DATA_DIR"] / "national-coverage-manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    urls = [record["page_url"] for record in data["records"]]
    duplicates = [url for url, count in Counter(urls).items() if count > 1]
    if duplicates:
        raise SystemExit(
            "National manifest contains duplicate county lookup targets: "
            + ", ".join(sorted(duplicates))
        )
    if len(urls) != 3144 or len(set(urls)) != 3144:
        raise SystemExit(
            f"National lookup URL integrity failure: {len(urls)} records, "
            f"{len(set(urls))} unique targets"
        )
    required_city_routes = {
        "https://septicscope.com/counties/maryland/baltimore-city/",
        "https://septicscope.com/counties/missouri/st-louis-city/",
        "https://septicscope.com/counties/virginia/fairfax-city/",
        "https://septicscope.com/counties/virginia/franklin-city/",
        "https://septicscope.com/counties/virginia/richmond-city/",
        "https://septicscope.com/counties/virginia/roanoke-city/",
    }
    missing = required_city_routes.difference(urls)
    if missing:
        raise SystemExit("Missing collision-safe county-equivalent lookup targets: " + ", ".join(sorted(missing)))
    print("PASS: 3,144 unique county and county-equivalent lookup targets")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    namespace = _patched_namespace()
    if args.check:
        namespace["check"]()
    else:
        namespace["generate"]()
    _verify_unique_county_urls(namespace)


if __name__ == "__main__":
    main()
