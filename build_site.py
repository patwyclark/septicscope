"""Canonical SepticScope production build orchestrator.

Cloudflare Pages and GitHub Actions must both run only this file. The build now
prioritizes a small, locally differentiated search footprint over page count. The
quality-recovery pass runs before the final inventory so unfinished, repetitive,
navigation-only, and consolidated pages are noindex/ad-free and excluded from the
sitemap before validation.
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
    "homebuyer_guide_quality.py",
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
    service_locator = ROOT / "septic_services_near_me.py"
    county_lookup = ROOT / "county_lookup_experience.py"
    homepage_experience = ROOT / "homepage_experience.py"
    service_quality = ROOT / "septic_service_quality.py"
    quality_recovery = ROOT / "quality_recovery.py"
    quality_finalize = ROOT / "quality_recovery_finalize.py"
    seo_review = ROOT / "tools" / "seo_hourly_audit.py"

    # The first inventory creates the national county manifest used by the lookup and
    # provider layers. Provider information can still enrich supported county pages,
    # while the global provider search remains gated until national coverage exists.
    _run_script(inventory, env=env)
    _run_script(provider_experience, env=env)
    _run_script(service_locator, env=env)
    _run_script(county_lookup, env=env)
    _run_script(homepage_experience, env=env)
    _run_script(service_quality, env=env)

    # This is the decisive quality gate. It consolidates FAQ pages, rebuilds the
    # homepage and About page, demotes repetitive or insufficiently local county pages,
    # removes ads from navigation/noindex pages, and creates a focused sitemap.
    _run_script(quality_recovery, env=env)
    _run_script(quality_finalize, env=env)

    # Final inventories and SEO checks must inspect the post-recovery output rather
    # than the larger pre-recovery generator footprint.
    _run_script(inventory, env=env)
    _run_script(
        seo_review,
        "--site",
        str(ROOT / "site"),
        "--report",
        str(ROOT / "site" / "data" / "hourly-seo-build-report.json"),
        "--apply-safe",
        env=env,
    )
    _run_script(inventory, env=env)
    _run_script(
        seo_review,
        "--site",
        str(ROOT / "site"),
        "--report",
        str(ROOT / "site" / "data" / "hourly-seo-build-report.json"),
        env=env,
    )
    _run_script(quality_recovery, "--check", env=env)


if __name__ == "__main__":
    _run()
