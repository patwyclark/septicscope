#!/usr/bin/env python3
"""Final deterministic checks and link repairs for the homepage/service locator."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"

REPLACEMENTS = {
    '<a href="/guides/septic-tank-pumping-cost/">Understand pumping quotes →</a>':
        '<a href="/faq/how-often-should-you-pump-a-septic-tank/">Plan routine pumping intervals →</a>',
    '<a href="/guides/septic-system-failure-signs/">Warning signs and urgent next steps →</a>':
        '<a href="/faq/what-causes-a-drainfield-to-fail/">What causes drainfield failure? →</a>',
    '<a class="home-guide" href="/guides/septic-tank-pumping-cost/"><strong>Septic pumping cost factors</strong><span>Compare access, tank size, disposal, inspection, and emergency-service variables.</span></a>':
        '<a class="home-guide" href="/faq/how-often-should-you-pump-a-septic-tank/"><strong>How often to pump a septic tank</strong><span>Understand typical intervals and the household, tank, and use factors that change the schedule.</span></a>',
    '<a class="home-guide" href="/guides/septic-system-failure-signs/"><strong>Signs of septic failure</strong><span>Recognize backups, slow drains, odors, wet areas, alarms, and urgent next steps.</span></a>':
        '<a class="home-guide" href="/faq/what-causes-a-drainfield-to-fail/"><strong>What causes a drainfield to fail?</strong><span>Understand solids, excess water, compaction, roots, age, and site conditions that can damage the treatment area.</span></a>',
}

FORBIDDEN_PATHS = (
    "/guides/septic-tank-pumping-cost/",
    "/guides/septic-system-failure-signs/",
)

REQUIRED_LIVE_PATHS = (
    "/faq/how-often-should-you-pump-a-septic-tank/",
    "/faq/what-causes-a-drainfield-to-fail/",
    "/guides/septic-maintenance-checklist/",
    "/guides/septic-inspection-checklist/",
    "/guides/septic-drainfield-repair-replacement/",
)


def apply(path: Path) -> None:
    if not path.exists():
        raise RuntimeError(f"Required generated page is missing: {path}")
    text = path.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    for forbidden in FORBIDDEN_PATHS:
        if forbidden in text:
            raise RuntimeError(f"Generated page still links to an unavailable route: {forbidden}")
    path.write_text(text, encoding="utf-8")


def assert_live_targets() -> None:
    for url_path in REQUIRED_LIVE_PATHS:
        target = SITE / url_path.strip("/") / "index.html"
        if not target.exists():
            raise RuntimeError(f"Service experience target is missing: {url_path}")


def main() -> None:
    assert_live_targets()
    apply(SITE / "index.html")
    apply(SITE / "septic-services-near-me" / "index.html")
    print("Septic service quality pass complete: homepage and locator link only to live support resources")


if __name__ == "__main__":
    main()
