#!/usr/bin/env python3
"""Synchronize reviewed provider overrides into the canonical provider catalog.

The site renderer can apply provider overrides without mutating source data. This tool is
used by GitHub Actions after reviewed changes so inventory manifests, county provider
counts, and build metadata read the same curated records that visitors see.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
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


def sync_catalog(*, check: bool = False) -> bool:
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
    args = parser.parse_args()
    sync_catalog(check=args.check)


if __name__ == "__main__":
    main()
