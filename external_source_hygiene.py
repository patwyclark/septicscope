"""Normalize confirmed-broken official-source links after the core county build.

This is intentionally narrow: only URLs that have been independently confirmed as
broken by CI are replaced, and only with authoritative government sources that support
the same page claim. The pass runs before final inventory/SEO generation so the source
catalog and external-link audit see the corrected destination.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"


def replace_confirmed_broken_source() -> None:
    page = SITE / "counties" / "arizona" / "navajo" / "index.html"
    if not page.is_file():
        raise FileNotFoundError(f"Expected Navajo County page is missing: {page}")

    text = page.read_text(encoding="utf-8")
    old_url = "https://www.navajocountyaz.gov/m/FAQ"
    new_url = "https://www.navajocountyaz.gov/DocumentCenter/View/2431/Construction-Permit-Application"
    old_label = "Navajo County — building and septic permit FAQs"
    new_label = "Navajo County — construction permit application and septic requirements"

    if old_url in text:
        text = text.replace(old_url, new_url)
        text = text.replace(old_label, new_label)
        page.write_text(text, encoding="utf-8")
        print(f"Replaced confirmed-broken Navajo County source: {old_url} -> {new_url}")
    elif new_url not in text:
        raise RuntimeError("Navajo County page contains neither the retired nor replacement official source")


if __name__ == "__main__":
    replace_confirmed_broken_source()
