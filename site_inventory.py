"""Run the national inventory with collision- and redirect-aware compatibility fixes."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent
CORE = ROOT / "site_inventory_core.py"


def _route_for_path(path: Path, site: Path) -> str:
    relative = path.relative_to(site).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return "/" + relative[:-10]
    return "/" + relative


def _redirect_sources(site: Path) -> set[str]:
    redirects = site / "_redirects"
    result: set[str] = set()
    if not redirects.exists():
        return result
    for line in redirects.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) < 3 or fields[2] not in {"301", "302", "307", "308"}:
            continue
        source = fields[0]
        if source.startswith("/") and "*" not in source and ":" not in source:
            result.add(source)
    return result


def _load_namespace() -> dict:
    namespace = runpy.run_path(str(CORE), run_name="septicscope_inventory_core")
    original_load_rows = namespace["load_county_rows"]
    original_parse_page = namespace["parse_page"]
    original_legacy_scan = namespace["repository_legacy_scan"]
    site = namespace["SITE"]

    def load_collision_safe_rows():
        rows = original_load_rows()
        counts = Counter((abbr, namespace["slugify"](name)) for abbr, name, lsad, fips in rows)
        fixed = []
        for abbr, name, lsad, fips in rows:
            if counts[(abbr, namespace["slugify"](name))] > 1 and str(lsad).lower() != "county":
                label = "Census Area" if lsad == "CA" else lsad
                name = name if str(label).lower() in name.lower() else f"{name} {label}"
            fixed.append([abbr, name, lsad, fips])
        return fixed

    redirect_sources = _redirect_sources(site)

    def parse_redirect_aware_page(path):
        parser, raw = original_parse_page(path)
        if _route_for_path(path, site) in redirect_sources:
            parser.robots = (parser.robots + ",noindex").strip(",")
        return parser, raw

    def scan_without_scanner_self_matches():
        ignored = {"site_inventory.py", "site_inventory_core.py"}
        return [
            finding for finding in original_legacy_scan()
            if finding.get("path") not in ignored
        ]

    namespace["load_county_rows"] = load_collision_safe_rows
    namespace["parse_page"] = parse_redirect_aware_page
    namespace["repository_legacy_scan"] = scan_without_scanner_self_matches
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
    namespace = _load_namespace()
    if args.check:
        namespace["check"]()
    else:
        namespace["generate"]()
    _verify_unique_county_urls(namespace)


if __name__ == "__main__":
    main()
