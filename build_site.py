"""Canonical SepticScope production build orchestrator.

Cloudflare Pages and GitHub Actions must both run only this file. The historical
site generator is preserved as site_core_build.py; supplemental guides, trust
hardening, and machine-readable inventories are executed here in a deterministic
order so CI and production cannot drift.
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
)


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
        script = ROOT / script_name
        if not script.is_file():
            raise FileNotFoundError(f"Missing supplemental generator: {script}")
        subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            env=env,
            check=True,
        )

    # Match normal Python atexit ordering (last registered, first executed).
    for function, args, kwargs in reversed(captured_exit_handlers):
        function(*args, **kwargs)

    inventory = ROOT / "site_inventory.py"
    if not inventory.is_file():
        raise FileNotFoundError(f"Missing site inventory generator: {inventory}")
    subprocess.run(
        [sys.executable, str(inventory)],
        cwd=ROOT,
        env=env,
        check=True,
    )


if __name__ == "__main__":
    _run()
