"""Canonical SepticScope production build orchestrator.

Cloudflare Pages and GitHub Actions must both run only this file. The historical
site generator is preserved as site_core_build.py; supplemental guides, trust
hardening, provider rendering, contextual growth links, SEO safeguards and
machine-readable inventories are executed in a deterministic order so CI and
production cannot drift.
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
    "drainfield_guide.py",
    "tank_size_calculator.py",
    "septic_maintenance_checklist.py",
    "system_types_guide.py",
    "septic_winter_guide.py",
    "septic_inspection_checklist.py",
    "septic_system_lifespan_guide.py",
    "site_quality_polish.py",
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

    # The legacy build chain registers final trust/AdSense passes with atexit.
    # Capture them so this orchestrator can run supplemental page generators first,
    # then apply those finalizers, and only then create the authoritative manifests.
    atexit.register = capture_register  # type: ignore[assignment]
    try:
        runpy.run_path(str(CORE_BUILD), run_name="__main__")
    finally:
        atexit.register = original_register  # type: ignore[assignment]

    env = os.environ.copy()
    env["SEPTICSCOPE_ORCHESTRATED_BUILD"] = "1"
    for script_name in POST_BUILD_SCRIPTS:
        _run_script(ROOT / script_name, env=env)

    # Match normal Python atexit ordering (last registered, first executed).
    for function, args, kwargs in reversed(captured_exit_handlers):
        function(*args, **kwargs)

    inventory = ROOT / "site_inventory.py"
    provider_experience = ROOT / "provider_experience.py"
    growth_experience = ROOT / "continuous_growth_experience.py"
    seo_review = ROOT / "tools" / "seo_hourly_audit.py"
    growth_planner = ROOT / "tools" / "continuous_growth.py"

    # The first inventory creates the national county manifest needed to map provider
    # FIPS records to final county URLs. Source-controlled provider and contextual-link
    # layers then enrich the finished pages.
    _run_script(inventory, env=env)
    _run_script(provider_experience, env=env)
    _run_script(growth_experience, env=env)

    # Safe SEO maintenance repairs only missing title/description/canonical essentials;
    # it does not add meta-keywords or repeat phrases for ranking manipulation.
    _run_script(
        seo_review,
        "--site",
        str(ROOT / "site"),
        "--report",
        str(ROOT / "site" / "data" / "hourly-seo-build-report.json"),
        "--apply-safe",
        env=env,
    )

    # Rebuild inventories from the final enriched output. site_inventory.py preserves
    # the detailed provider page when its marker is present.
    _run_script(inventory, env=env)
    _run_script(
        seo_review,
        "--site",
        str(ROOT / "site"),
        "--report",
        str(ROOT / "site" / "data" / "hourly-seo-build-report.json"),
        env=env,
    )

    # Publish a machine-readable, plan-only view of the next evidence-backed growth
    # opportunities. Production builds never mutate source-controlled growth state.
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
