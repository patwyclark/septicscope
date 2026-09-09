#!/usr/bin/env python3
"""Remove incomplete local-service modules from the public recovery footprint.

Provider research stays in source data. During AdSense/search recovery, county pages
focus on permits and homeowner information instead of presenting uneven business
coverage as a finished directory product.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
SECTION = re.compile(
    r'<section\s+data-septicscope-provider-section=["\']1["\'][^>]*>.*?</section>',
    flags=re.I | re.S,
)
STYLE = re.compile(
    r'<style\s+data-septicscope-provider-style=["\']1["\'][^>]*>.*?</style>',
    flags=re.I | re.S,
)


def main() -> None:
    pages_changed = 0
    modules_removed = 0
    for path in SITE.rglob("*.html"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        updated, count = SECTION.subn("", raw)
        updated = STYLE.sub("", updated)
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            pages_changed += 1
            modules_removed += count
    leftovers = []
    for path in SITE.rglob("*.html"):
        if path in {SITE / "providers" / "index.html", SITE / "septic-services-near-me" / "index.html"}:
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "data-septicscope-provider-section" in raw:
            leftovers.append(path.relative_to(SITE).as_posix())
    if leftovers:
        raise RuntimeError("Provider modules remain on public pages: " + ", ".join(leftovers[:10]))
    print(
        f"Recovery provider visibility: removed {modules_removed} incomplete local-service modules "
        f"from {pages_changed} pages; source data retained privately"
    )


if __name__ == "__main__":
    main()
