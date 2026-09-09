"""Canonical SepticScope production build orchestrator.

Cloudflare Pages and GitHub Actions must both run only this file. The historical
site generator is preserved as site_core_build.py; supplemental guides, trust
hardening, provider rendering, county lookup, gated service search, quality-first
publication, SEO safeguards and machine-readable inventories are executed in a
deterministic order so CI and production cannot drift.
"""
from __future__ import annotations

import atexit
import os
from pathlib import Path
import runpy
import subprocess
import sys
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent
CORE_BUILD = ROOT / "site_core_build.py"
POST_BUILD_SCRIPTS = (
    "kentucky_barren_river_quality.py",
    "kentucky_nky_quality.py",
    "kentucky_green_river_quality.py",
    "drainfield_guide.py",
    "tank_size_calculator.py",
    "septic_maintenance_checklist.py",
    "system_types_guide.py",
    "septic_winter_guide.py",
    "septic_inspection_checklist.py",
    "septic_system_lifespan_guide.py",
    "septic_records_guide.py",
    "site_quality_polish.py",
    "external_source_hygiene.py",
)


def _run_script(path: Path, *args: str, env: dict[str, str]) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Missing production build component: {path}")
    subprocess.run([sys.executable, str(path), *args], cwd=ROOT, env=env, check=True)


def _run() -> None:
    if not CORE_BUILD.is_file():
        raise FileNotFoundError(f"Missing canonical core build: {CORE_BUILD}")

    captured_exit_handlers: list[
        tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]
    ] = []
    original_register = atexit.register

    def capture_register(
        function: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Callable[..., Any]:
        captured_exit_handlers.append((function, args, kwargs))
        return function

    atexit.register = capture_register  # type: ignore[assignment]
    try:
        runpy.run_path(str(CORE_BUILD), run_name="__main__")
    finally:
        atexit.register = original_register  # type: ignore[assignment]

    env = os.environ.copy()
    env["SEPTICSCOPE_ORCHESTRATED_BUILD"] = "1"
    for script_name in POST_BUILD_SCRIPTS:
        _run_script(ROOT / script_name, env=env)

    for function, args, kwargs in reversed(captured_exit_handlers):
        function(*args, **kwargs)

    inventory = ROOT / "site_inventory.py"
    provider_experience = ROOT / "provider_curated_experience.py"
    growth_experience = ROOT / "continuous_growth_experience.py"
    service_locator = ROOT / "septic_services_near_me.py"
    county_lookup = ROOT / "county_lookup_experience.py"
    homepage_experience = ROOT / "homepage_experience.py"
    service_quality = ROOT / "septic_service_quality.py"
    adsense_recovery = ROOT / "adsense_recovery.py"
    seo_review = ROOT / "tools" / "seo_hourly_audit.py"
    growth_planner = ROOT / "tools" / "continuous_growth.py"

    # First create the national county manifest from the historical build, render all
    # evidence-backed experiences, then remove every unverified county placeholder.
    # The lookup keeps all 3,144 FIPS records without publishing 2,000+ construction pages.
    _run_script(inventory, env=env)
    _run_script(provider_experience, env=env)
    _run_script(growth_experience, env=env)
    _run_script(service_locator, env=env)
    _run_script(county_lookup, env=env)
    _run_script(homepage_experience, env=env)
    _run_script(service_quality, env=env)
    _run_script(adsense_recovery, env=env)

    # Re-inventory the quality-filtered output, then regenerate the two public entry
    # points from the final verified/lookup-only statuses. A second recovery pass keeps
    # those regenerated pages consistent with the AdSense placement allowlist.
    _run_script(inventory, env=env)
    _run_script(county_lookup, env=env)
    _run_script(homepage_experience, env=env)
    _run_script(service_quality, env=env)
    _run_script(adsense_recovery, env=env)
    _run_script(inventory, env=env)

    # Conservative SEO repairs may add only missing metadata essentials. The final
    # recovery pass reasserts publication, advertising, trust and sitemap safeguards.
    _run_script(
        seo_review,
        "--site",
        str(ROOT / "site"),
        "--report",
        str(ROOT / "site" / "data" / "hourly-seo-build-report.json"),
        "--apply-safe",
        env=env,
    )
    _run_script(adsense_recovery, env=env)
    _run_script(inventory, env=env)
    _run_script(
        seo_review,
        "--site",
        str(ROOT / "site"),
        "--report",
        str(ROOT / "site" / "data" / "hourly-seo-build-report.json"),
        env=env,
    )

    _run_script(
        growth_planner,
        "--site",
        str(ROOT / "site"),
        "--state",
        str(ROOT / "data" / "growth-links.json"),
        "--report",
        str(ROOT / "site" / "data" / "continuous-growth-report.json"),
        env=env,
    )


if __name__ == "__main__":
    _run()
