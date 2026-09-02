#!/usr/bin/env python3
"""Synchronize reviewed provider overrides into the canonical provider catalog.

The site renderer can apply provider overrides without mutating source data. This tool is
used by GitHub Actions after reviewed changes so inventory manifests, county provider
counts, and build metadata read the same curated records that visitors see. Its self-test
also protects provider IDs and county FIPS mappings before a production build begins.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from provider_curated_experience import BASE_PROVIDER_FILE, curated_provider_data  # noqa: E402


def serialized_catalog() -> str:
    return json.dumps(
        curated_provider_data(),
        indent=2,
        ensure_ascii=False,
    ) + "\n"


def validate_catalog() -> dict:
    data = curated_provider_data()
    providers = data.get("providers", [])
    if not isinstance(providers, list):
        raise SystemExit("Curated provider catalog does not contain a provider list")

    seen: set[str] = set()
    for provider in providers:
        if not isinstance(provider, dict):
            raise SystemExit("Curated provider catalog contains a non-object record")
        provider_id = str(provider.get("id", "")).strip()
        if not provider_id or provider_id in seen:
            raise SystemExit(f"Missing or duplicate provider id: {provider_id!r}")
        seen.add(provider_id)
        for county in provider.get("counties_served", []):
            fips = county.get("fips", "") if isinstance(county, dict) else county
            if not re.fullmatch(r"\d{5}", str(fips).strip()):
                raise SystemExit(
                    f"Provider {provider_id} contains an invalid county FIPS value: {fips!r}"
                )

    serialized = json.dumps(data, ensure_ascii=False)
    if json.loads(serialized) != data:
        raise SystemExit("Curated provider catalog failed JSON round-trip validation")
    print(f"PASS: {len(providers)} unique curated provider records are structurally valid")
    return data


def sync_catalog(*, check: bool = False) -> bool:
    validate_catalog()
    desired = serialized_catalog()
    current = (
        BASE_PROVIDER_FILE.read_text(encoding="utf-8")
        if BASE_PROVIDER_FILE.exists()
        else ""
    )
    changed = current != desired
    if check and changed:
        raise SystemExit(
            "Canonical provider catalog is not synchronized with reviewed overrides"
        )
    if changed:
        BASE_PROVIDER_FILE.write_text(desired, encoding="utf-8")
        print("Synchronized reviewed provider records into data/providers.json")
    else:
        print("Canonical provider catalog already matches reviewed overrides")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail instead of writing when the canonical provider catalog is stale.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Validate the curated provider schema without changing source data.",
    )
    args = parser.parse_args()
    if args.self_test:
        validate_catalog()
        return
    sync_catalog(check=args.check)


if __name__ == "__main__":
    main()
