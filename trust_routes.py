"""Legacy trust-route compatibility and homepage trust signals for SepticScope."""
from __future__ import annotations

from pathlib import Path
import re

DOMAIN = "https://septicscope.com"


def _verified_count(site: Path) -> int:
    total = 0
    for path in site.glob("counties/*/*/index.html"):
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        if "noindex" not in text and "official sources" in text and "permitting authority" in text:
            total += 1
    return total


def _refresh_home_metric(site: Path, verified: int) -> None:
    home = site / "index.html"
    if not home.exists() or not verified:
        return
    text = home.read_text(encoding="utf-8", errors="replace")

    # The original landing-page template carried a launch-day count of five guides.
    # Replace only a number directly associated with the "verified county guides"
    # label so unrelated figures such as the five cornerstone guides are untouched.
    patterns = [
        re.compile(r'(?is)(>\s*)\d+(\s*</[^>]+>\s*<[^>]+>\s*verified county guides\b)'),
        re.compile(r'(?is)(>\s*)\d+(\s*<[^>]*>\s*verified county guides\b)'),
    ]
    changed = False
    for pattern in patterns:
        updated, count = pattern.subn(lambda m: f"{m.group(1)}{verified}{m.group(2)}", text, count=1)
        if count:
            text = updated
            changed = True
            break

    # If the template structure changes, still publish a current source-verified count
    # beside the nationwide-lookup copy rather than silently leaving a stale metric.
    if not changed and "current-verified-county-count" not in text:
        marker = "Search all 3,144 U.S. counties and county equivalents."
        badge = (
            f'<span id="current-verified-county-count" style="display:block;margin-top:8px">'
            f'<strong>{verified}</strong> county guides are currently source-verified.</span>'
        )
        if marker in text:
            text = text.replace(marker, marker + badge, 1)
            changed = True

    if changed:
        home.write_text(text, encoding="utf-8")


def _write_legacy_redirect(path: Path, destination: str, title: str) -> None:
    canonical = f"{DOMAIN}{destination}"
    path.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="noindex,follow">'
        f'<link rel="canonical" href="{canonical}">'
        f'<meta http-equiv="refresh" content="0;url={destination}">'
        f'<title>{title} | SepticScope</title></head><body>'
        f'<p>This page moved to <a href="{destination}">{title}</a>.</p>'
        '</body></html>',
        encoding="utf-8",
    )


def _ensure_redirects(site: Path) -> None:
    redirects = site / "_redirects"
    existing = redirects.read_text(encoding="utf-8", errors="replace") if redirects.exists() else ""
    wanted = [
        "/privacy.html /privacy/ 301",
        "/corrections.html /contact/ 301",
    ]
    lines = existing.rstrip("\n").splitlines() if existing.strip() else []
    for rule in wanted:
        source = rule.split()[0]
        if not any(line.strip().startswith(source + " ") for line in lines):
            lines.append(rule)
    redirects.write_text("\n".join(lines) + "\n", encoding="utf-8")


def finalize(root: Path | str | None = None) -> None:
    repo = Path(root) if root is not None else Path(__file__).resolve().parent
    site = repo / "site"
    if not site.is_dir():
        return

    verified = _verified_count(site)
    _refresh_home_metric(site, verified)

    # Preserve old public URLs while making /privacy/ and /contact/ the canonical
    # destinations. The files are also safe fallbacks for hosts that ignore _redirects.
    _write_legacy_redirect(site / "privacy.html", "/privacy/", "Privacy Policy")
    _write_legacy_redirect(site / "corrections.html", "/contact/", "Contact & Feedback")
    _ensure_redirects(site)

    print(f"Trust-route compatibility complete: homepage count={verified}; legacy privacy/corrections redirected")
