"""Apply deterministic final content polish before trust hardening and inventory."""
from __future__ import annotations

from html import unescape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"


def _metric_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf'(<div\s+class=["\']metric["\']>\s*)[0-9][0-9,]*(\s*</div>\s*'
        rf'<div\s+class=["\']metric-label["\']>\s*){re.escape(label)}(\s*</div>)',
        flags=re.IGNORECASE,
    )


def _replace_home_stat(
    text: str,
    accepted_labels: tuple[str, ...],
    output_label: str,
    value: int,
) -> str:
    for label in accepted_labels:
        pattern = _metric_pattern(label)
        updated, count = pattern.subn(
            lambda match: (
                f"{match.group(1)}{value:,}{match.group(2)}"
                f"{output_label}{match.group(3)}"
            ),
            text,
            count=1,
        )
        if count:
            return updated
    raise RuntimeError(
        "Homepage metric card not found for any accepted label: "
        + ", ".join(accepted_labels)
    )


def _visible_text(text: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", unescape(without_tags)).strip()


def _assert_visible_metric(text: str, label: str, expected: int) -> None:
    visible = _visible_text(text)
    if not re.search(
        rf"\b{expected:,}\s+{re.escape(label)}\b",
        visible,
        flags=re.IGNORECASE,
    ):
        raise RuntimeError(
            f"Homepage does not show the expected metric: {expected:,} {label}"
        )


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
    text = _replace_home_stat(
        text,
        ("verified county guides",),
        "verified county guides",
        verified,
    )
    text = _replace_home_stat(
        text,
        ("FAQ articles",),
        "FAQ articles",
        faq_count,
    )
    text = _replace_home_stat(
        text,
        ("cornerstone guides", "septic guides"),
        "septic guides",
        guide_count,
    )
    home.write_text(text, encoding="utf-8")

    final = home.read_text(encoding="utf-8", errors="replace")
    _assert_visible_metric(final, "verified county guides", verified)
    _assert_visible_metric(final, "FAQ articles", faq_count)
    _assert_visible_metric(final, "septic guides", guide_count)
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


def _polish_faq_hub() -> None:
    page = SITE / "faq" / "index.html"
    if not page.exists():
        raise RuntimeError("Generated FAQ hub is missing")
    text = page.read_text(encoding="utf-8", errors="replace")
    old = "<h1>Septic Questions, Answered</h1>"
    new = "<h1>Septic System Frequently Asked Questions</h1>"
    if old in text:
        text = text.replace(old, new, 1)
    elif new not in text:
        raise RuntimeError("FAQ hub H1 no longer matches the expected source")
    page.write_text(text, encoding="utf-8")


def main() -> None:
    if not SITE.is_dir():
        raise RuntimeError("site/ does not exist; run the core build first")
    _polish_lifespan_guide()
    _polish_faq_hub()
    verified, faq_count, guide_count = _polish_homepage()
    print(
        "Site quality polish complete: "
        f"homepage={verified} verified counties/{faq_count} FAQs/{guide_count} guides; "
        "lifespan and FAQ hub H1s aligned to distinct search intent"
    )


if __name__ == "__main__":
    main()
