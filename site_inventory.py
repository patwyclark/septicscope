"""Run the national inventory with collision-, redirect-, and provider-aware fixes."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORE = ROOT / "site_inventory_core.py"


def _patched_namespace() -> dict:
    source = CORE.read_text(encoding="utf-8")

    row_needle = "    county_rows = load_county_rows()\n"
    row_patch = row_needle + """    # Census data contains six same-name county/city pairs. Preserve the
    # long-standing county slug and append the legal-area label to the non-county
    # equivalent so every FIPS entity has its own canonical page.
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
    if source.count(row_needle) != 1:
        raise RuntimeError("County-row compatibility patch no longer matches the inventory core")
    source = source.replace(row_needle, row_patch, 1)

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
    if source.count(scan_needle) != 1:
        raise RuntimeError("Legacy-brand scanner compatibility patch no longer matches the inventory core")
    source = source.replace(scan_needle, scan_patch, 1)

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
    if source.count(pages_needle) != 1:
        raise RuntimeError("Redirect inventory patch no longer matches the inventory core")
    source = source.replace(pages_needle, pages_patch, 1)

    indexable_needle = "        indexable = not is_noindex(parser) and page_type != \"error_page\"\n"
    indexable_patch = "        indexable = not is_noindex(parser) and page_type != \"error_page\" and url not in redirected_page_urls\n"
    if source.count(indexable_needle) != 1:
        raise RuntimeError("Redirect indexability patch no longer matches the inventory core")
    source = source.replace(indexable_needle, indexable_patch, 1)

    provider_needle = "    write_provider_landing(provider_data)\n"
    provider_patch = """    provider_page = SITE / "providers" / "index.html"
    provider_ready = (
        provider_page.exists()
        and 'data-septicscope-provider-directory="1"'
        in provider_page.read_text(encoding="utf-8", errors="replace")
    )
    # The first inventory pass creates the county manifest. A later provider rendering
    # pass replaces the placeholder with a source-checked directory. Preserve that
    # finished page when the inventory is regenerated from final production output.
    if not provider_ready:
        write_provider_landing(provider_data)
"""
    if source.count(provider_needle) != 1:
        raise RuntimeError("Provider-directory compatibility patch no longer matches the inventory core")
    source = source.replace(provider_needle, provider_patch, 1)

    provider_status_needle = '        if str(provider.get("status", "active")).lower() == "closed":\n'
    provider_status_patch = '        if str(provider.get("status", "active")).lower() not in {"active", "verified"}:\n'
    if source.count(provider_status_needle) != 1:
        raise RuntimeError("Provider-status compatibility patch no longer matches the inventory core")
    source = source.replace(provider_status_needle, provider_status_patch, 1)

    provider_count_needle = '            "provider_listings": len(provider_data.get("providers", [])),\n'
    provider_count_patch = '            "provider_listings": sum(str(item.get("status", "active")).lower() in {"active", "verified"} for item in provider_data.get("providers", []) if isinstance(item, dict)),\n'
    if source.count(provider_count_needle) != 1:
        raise RuntimeError("Provider-count compatibility patch no longer matches the inventory core")
    source = source.replace(provider_count_needle, provider_count_patch, 1)

    namespace = {
        "__name__": "septicscope_inventory_core",
        "__file__": str(CORE),
    }
    exec(compile(source, str(CORE), "exec"), namespace)
    return namespace


def _verify_unique_county_urls(namespace: dict) -> None:
    manifest = namespace["OUTPUT_DATA_DIR"] / "national-coverage-manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    urls = [record["page_url"] for record in data["records"]]
    duplicates = [url for url, count in Counter(urls).items() if count > 1]
    if duplicates:
        raise SystemExit(
            "National manifest contains duplicate county/county-equivalent URLs: "
            + ", ".join(sorted(duplicates))
        )
    if len(urls) != 3144 or len(set(urls)) != 3144:
        raise SystemExit(
            f"National manifest URL integrity failure: {len(urls)} records, "
            f"{len(set(urls))} unique URLs"
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
        raise SystemExit("Missing collision-safe county-equivalent routes: " + ", ".join(sorted(missing)))
    print("PASS: 3,144 unique county and county-equivalent canonical URLs")


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
