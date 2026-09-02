#!/usr/bin/env python3
"""Apply reviewed provider corrections and additions before rendering county cards."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory

import provider_experience as renderer

ROOT = Path(__file__).resolve().parent
BASE_PROVIDER_FILE = ROOT / "data" / "providers.json"
OVERRIDE_FILE = ROOT / "data" / "provider-overrides.json"


def load_object(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected a JSON object in {path}")
    return data


def county_value(item: object) -> str:
    if isinstance(item, dict):
        return str(item.get("fips", "")).strip()
    return str(item).strip()


def curated_provider_data() -> dict:
    data = deepcopy(load_object(BASE_PROVIDER_FILE))
    overrides = load_object(OVERRIDE_FILE) if OVERRIDE_FILE.exists() else {}
    providers = data.get("providers", [])
    if not isinstance(providers, list):
        raise RuntimeError("data/providers.json providers must be a list")

    by_id = {
        str(provider.get("id", "")).strip(): provider
        for provider in providers
        if isinstance(provider, dict) and str(provider.get("id", "")).strip()
    }

    updates = overrides.get("provider_updates", {})
    if updates and not isinstance(updates, dict):
        raise RuntimeError("provider_updates must be an object")
    for provider_id, raw_update in updates.items():
        if provider_id not in by_id:
            raise RuntimeError(f"Provider override references unknown id: {provider_id}")
        if not isinstance(raw_update, dict):
            raise RuntimeError(f"Provider override for {provider_id} must be an object")
        provider = by_id[provider_id]
        removals = {
            str(value).strip()
            for value in raw_update.get("remove_counties_served", [])
            if re.fullmatch(r"\d{5}", str(value).strip())
        }
        if removals:
            provider["counties_served"] = [
                item for item in provider.get("counties_served", [])
                if county_value(item) not in removals
            ]
        field_updates = raw_update.get("set", {})
        if field_updates and not isinstance(field_updates, dict):
            raise RuntimeError(f"set override for {provider_id} must be an object")
        provider.update(field_updates)

    for addition in overrides.get("providers", []):
        if not isinstance(addition, dict):
            raise RuntimeError("Each provider override addition must be an object")
        provider_id = str(addition.get("id", "")).strip()
        if not provider_id:
            raise RuntimeError("Provider override addition is missing id")
        if provider_id in by_id:
            replacement = deepcopy(addition)
            index = providers.index(by_id[provider_id])
            providers[index] = replacement
            by_id[provider_id] = replacement
        else:
            addition_copy = deepcopy(addition)
            providers.append(addition_copy)
            by_id[provider_id] = addition_copy

    data["providers"] = providers
    data["last_updated"] = max(
        str(data.get("last_updated", "")),
        str(overrides.get("last_updated", "")),
    )
    return data


def main() -> None:
    data = curated_provider_data()
    with TemporaryDirectory(prefix="septicscope-provider-") as directory:
        curated_file = Path(directory) / "providers.json"
        curated_file.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        renderer.PROVIDER_FILE = curated_file
        renderer.main()


if __name__ == "__main__":
    main()
