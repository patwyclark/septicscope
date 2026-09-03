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
EXPANSION_GLOB = "provider-expansion-*.json"


def load_object(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected a JSON object in {path}")
    return data


def county_value(item: object) -> str:
    if isinstance(item, dict):
        return str(item.get("fips", "")).strip()
    return str(item).strip()


def apply_provider_layer(
    providers: list[dict],
    by_id: dict[str, dict],
    layer: dict,
    *,
    label: str,
) -> None:
    updates = layer.get("provider_updates", {})
    if updates and not isinstance(updates, dict):
        raise RuntimeError(f"{label}: provider_updates must be an object")
    for provider_id, raw_update in updates.items():
        if provider_id not in by_id:
            raise RuntimeError(f"{label}: provider update references unknown id: {provider_id}")
        if not isinstance(raw_update, dict):
            raise RuntimeError(f"{label}: provider update for {provider_id} must be an object")
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
            raise RuntimeError(f"{label}: set override for {provider_id} must be an object")
        provider.update(field_updates)

    additions = layer.get("providers", [])
    if additions and not isinstance(additions, list):
        raise RuntimeError(f"{label}: providers must be a list")
    for addition in additions:
        if not isinstance(addition, dict):
            raise RuntimeError(f"{label}: each provider addition must be an object")
        provider_id = str(addition.get("id", "")).strip()
        if not provider_id:
            raise RuntimeError(f"{label}: provider addition is missing id")
        replacement = deepcopy(addition)
        if provider_id in by_id:
            index = providers.index(by_id[provider_id])
            providers[index] = replacement
            by_id[provider_id] = replacement
        else:
            providers.append(replacement)
            by_id[provider_id] = replacement


def curated_provider_data() -> dict:
    data = deepcopy(load_object(BASE_PROVIDER_FILE))
    providers = data.get("providers", [])
    if not isinstance(providers, list):
        raise RuntimeError("data/providers.json providers must be a list")

    by_id = {
        str(provider.get("id", "")).strip(): provider
        for provider in providers
        if isinstance(provider, dict) and str(provider.get("id", "")).strip()
    }

    layers: list[tuple[Path, dict]] = []
    if OVERRIDE_FILE.exists():
        layers.append((OVERRIDE_FILE, load_object(OVERRIDE_FILE)))
    for path in sorted((ROOT / "data").glob(EXPANSION_GLOB)):
        layers.append((path, load_object(path)))

    latest = str(data.get("last_updated", ""))
    for path, layer in layers:
        apply_provider_layer(providers, by_id, layer, label=path.name)
        latest = max(latest, str(layer.get("last_updated", "")))

    data["providers"] = sorted(
        providers,
        key=lambda provider: (
            str(provider.get("business_name", "")).casefold(),
            str(provider.get("id", "")),
        ),
    )
    data["last_updated"] = latest
    data["catalog_layers"] = [path.name for path, _layer in layers]
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
        # Keep the correct AdSense loader ready for the future day when the national
        # directory reaches its 3,144-county launch gate. The current incomplete
        # directory remains noindex and ad-free.
        renderer.ADSENSE_TAG = f'''<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={renderer.ADSENSE_CLIENT}" crossorigin="anonymous"></script>'''
        renderer.main()


if __name__ == "__main__":
    main()
