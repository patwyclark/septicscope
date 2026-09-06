"""Legacy trust-route compatibility and homepage trust signals for SepticScope."""
from __future__ import annotations

from pathlib import Path
import re


# These historic .html URLs remain valid aliases for users and old backlinks, but
# the public platform redirects them to their clean canonical routes. They must
# therefore never be advertised in the sitemap or treated as indexable source files.
LEGACY_REDIRECTS = {
    "/privacy.html": "/privacy/",
    "/corrections.html": "/contact/",
    "/sources.html": "/sources",
    "/disclaimer.html": "/disclaimer",
}


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


def _ensure_redirects(site: Path) -> None:
    redirects = site / "_redirects"
    existing = redirects.read_text(encoding="utf-8", errors="replace") if redirects.exists() else ""
    wanted = [f"{source} {target} 301" for source, target in LEGACY_REDIRECTS.items()]
    lines = existing.rstrip("\n").splitlines() if existing.strip() else []
    for rule in wanted:
        source = rule.split()[0]
        if not any(line.strip().startswith(source + " ") for line in lines):
            lines.append(rule)
    redirects.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _remove_redirect_sources_from_sitemap(site: Path) -> None:
    """Keep legacy aliases available without advertising redirects to search engines."""
    sitemap = site / "sitemap.xml"
    if not sitemap.exists():
        return
    text = sitemap.read_text(encoding="utf-8", errors="replace")
    original = text
    for source in LEGACY_REDIRECTS:
        url = f"https://septicscope.com{source}"
        pattern = re.compile(
            rf"<url>\s*<loc>{re.escape(url)}</loc>.*?</url>",
            flags=re.I | re.S,
        )
        text = pattern.sub("", text)
    if text != original:
        sitemap.write_text(text, encoding="utf-8")


def _mark_redirect_source_files_noindex(site: Path) -> None:
    """Make static alias files match their public redirect/non-indexable intent.

    Cloudflare serves the redirect before these files are exposed, but the marker keeps
    local audits from misclassifying the implementation file as a canonical landing page.
    """
    for source in LEGACY_REDIRECTS:
        rel = source.lstrip("/")
        path = site / rel
        if not path.is_file() or path.suffix.lower() != ".html":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r'<meta\s+[^>]*name=["\']robots["\'][^>]*>', text, flags=re.I):
            text = re.sub(
                r'<meta\s+[^>]*name=["\']robots["\'][^>]*>',
                '<meta name="robots" content="noindex,follow">',
                text,
                count=1,
                flags=re.I,
            )
        elif "</head>" in text:
            text = text.replace(
                "</head>",
                '<meta name="robots" content="noindex,follow"></head>',
                1,
            )
        path.write_text(text, encoding="utf-8")


def finalize(root: Path | str | None = None) -> None:
    repo = Path(root) if root is not None else Path(__file__).resolve().parent
    site = repo / "site"
    if not site.is_dir():
        return

    verified = _verified_count(site)
    _refresh_home_metric(site, verified)

    # Preserve old URLs for users/backlinks while giving crawlers only direct,
    # canonical destinations in the sitemap.
    _ensure_redirects(site)
    _remove_redirect_sources_from_sitemap(site)
    _mark_redirect_source_files_noindex(site)

    print(
        f"Trust-route compatibility complete: homepage count={verified}; "
        "legacy trust aliases redirect and are excluded from indexing/sitemap"
    )
