"""Apply deterministic final content polish before trust hardening and inventory."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"


def _replace_home_stat(text: str, label: str, value: int) -> str:
    label_index = text.lower().find(label.lower())
    if label_index < 0:
        raise RuntimeError(f"Homepage metric label not found: {label}")
    window_start = max(0, label_index - 1200)
    window = text[window_start:label_index]
    matches = list(re.finditer(r">\s*([0-9][0-9,]*)\s*<", window))
    if not matches:
        raise RuntimeError(f"Homepage metric value not found before: {label}")
    match = matches[-1]
    start = window_start + match.start(1)
    end = window_start + match.end(1)
    return text[:start] + f"{value:,}" + text[end:]


def _visible_number_before(text: str, label: str) -> int:
    label_index = text.lower().find(label.lower())
    if label_index < 0:
        raise RuntimeError(f"Homepage metric label not found after polish: {label}")
    window = text[max(0, label_index - 1200):label_index]
    matches = list(re.finditer(r">\s*([0-9][0-9,]*)\s*<", window))
    if not matches:
        raise RuntimeError(f"Homepage metric value not found after polish: {label}")
    return int(matches[-1].group(1).replace(",", ""))


def _count_verified_counties() -> int:
    total = 0
    counties = SITE / "counties"
    for page in counties.glob("*/*/index.html"):
        raw = page.read_text(encoding="utf-8", errors="replace")
        lower = raw.lower()
        if "local guide in progress" in lower:
            continue
        if "official sources" in lower and "permitting authority" in lower:
            total += 1
    return total


def _polish_homepage() -> tuple[int, int, int]:
    home = SITE / "index.html"
    if not home.exists():
        raise RuntimeError("Generated homepage is missing")
    verified = _count_verified_counties()
    faq_count = len(list((SITE / "faq").glob("*/index.html")))
    guide_count = len(list((SITE / "guides").glob("*/index.html")))

    text = home.read_text(encoding="utf-8", errors="replace")
    text = _replace_home_stat(text, "verified county guides", verified)
    text = _replace_home_stat(text, "FAQ articles", faq_count)
    guide_label = "cornerstone guides" if "cornerstone guides" in text.lower() else "septic guides"
    text = _replace_home_stat(text, guide_label, guide_count)
    text = re.sub(r"cornerstone guides", "septic guides", text, flags=re.IGNORECASE)
    home.write_text(text, encoding="utf-8")

    final = home.read_text(encoding="utf-8", errors="replace")
    checks = {
        "verified county guides": verified,
        "FAQ articles": faq_count,
        "septic guides": guide_count,
    }
    for label, expected in checks.items():
        actual = _visible_number_before(final, label)
        if actual != expected:
            raise RuntimeError(f"Homepage metric mismatch for {label}: {actual} != {expected}")
    return verified, faq_count, guide_count


def _polish_lifespan_guide() -> None:
    page = SITE / "guides" / "septic-system-lifespan" / "index.html"
    if not page.exists():
        raise RuntimeError("Generated septic-system-lifespan guide is missing")
    text = page.read_text(encoding="utf-8", errors="replace")
    old = "<h1>How long does a septic system last?</h1>"
    new = "<h1>Septic system lifespan: what lasts, what fails, and when</h1>"
    if old in text:
        text = text.replace(old, new, 1)
    elif new not in text:
        raise RuntimeError("Lifespan guide H1 no longer matches the expected source")
    page.write_text(text, encoding="utf-8")


def main() -> None:
    if not SITE.is_dir():
        raise RuntimeError("site/ does not exist; run the core build first")
    _polish_lifespan_guide()
    verified, faq_count, guide_count = _polish_homepage()
    print(
        "Site quality polish complete: "
        f"homepage={verified} verified counties/{faq_count} FAQs/{guide_count} guides; "
        "lifespan guide H1 de-duplicated"
    )


if __name__ == "__main__":
    main()
