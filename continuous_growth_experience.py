#!/usr/bin/env python3
"""Render source-controlled continuous-growth links into generated pages."""
from __future__ import annotations

from collections import defaultdict
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
STATE_FILE = ROOT / "data" / "growth-links.json"
DOMAIN = "https://septicscope.com"
SECTION_MARKER = 'data-septicscope-growth-links="1"'
STYLE_MARKER = 'data-septicscope-growth-link-style="1"'
STYLE = r'''.ss-growth-links{margin:34px 0 10px;padding:22px;border:1px solid #dce3e8;border-radius:16px;background:#f7fafb}.ss-growth-links h2{margin-top:0}.ss-growth-links ul{display:grid;gap:12px;padding-left:1.2rem}.ss-growth-links li{padding-left:.2rem}.ss-growth-links a{font-weight:750}.ss-growth-links p{margin:.35rem 0 0;color:#5b6672}'''


def load_state() -> list[dict]:
    if not STATE_FILE.exists():
        return []
    data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("links"), list):
        raise RuntimeError("data/growth-links.json must be an object with a links array")
    return [item for item in data["links"] if isinstance(item, dict)]


def url_to_path(url: str) -> Path | None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.netloc not in {"septicscope.com", "www.septicscope.com"}:
        return None
    relative = parsed.path.strip("/")
    if not relative:
        return SITE / "index.html"
    if relative.endswith(".html"):
        return SITE / relative
    return SITE / relative / "index.html"


def remove_existing(text: str) -> str:
    return re.sub(
        r'<section\s+data-septicscope-growth-links="1"\b.*?</section>',
        "",
        text,
        flags=re.I | re.S,
    )


def ensure_style(text: str) -> str:
    if STYLE_MARKER in text:
        return text
    fragment = f'<style {STYLE_MARKER}>{STYLE}</style>'
    if re.search(r"</head>", text, flags=re.I):
        return re.sub(r"</head>", fragment + "</head>", text, count=1, flags=re.I)
    return text


def is_noindex(text: str) -> bool:
    for match in re.finditer(r'<meta\b[^>]*name=["\']robots["\'][^>]*>', text, flags=re.I):
        if "noindex" in match.group(0).lower():
            return True
    return False


def section_for(items: list[dict]) -> str:
    rows = []
    seen_targets: set[str] = set()
    for item in items:
        target = str(item.get("target_url", "")).strip()
        anchor = str(item.get("anchor_text", "")).strip()
        summary = str(item.get("summary", "")).strip()
        if not target.startswith(DOMAIN + "/") or not anchor or target in seen_targets:
            continue
        target_path = url_to_path(target)
        if not target_path or not target_path.exists():
            continue
        seen_targets.add(target)
        local_href = urlparse(target).path or "/"
        rows.append(
            f'<li><a href="{escape(local_href)}">{escape(anchor)}</a>'
            + (f'<p>{escape(summary)}</p>' if summary else "")
            + "</li>"
        )
    if not rows:
        return ""
    return (
        f'<section {SECTION_MARKER} class="ss-growth-links">'
        "<h2>Related SepticScope resources</h2>"
        "<p>Continue with the most relevant next step for planning, maintenance, inspection, or local requirements.</p>"
        f'<ul>{"".join(rows)}</ul>'
        "</section>"
    )


def inject(text: str, section: str) -> str:
    if not section:
        return text
    text = ensure_style(text)
    official_sources = re.search(r"<h2[^>]*>\s*Official sources\s*</h2>", text, flags=re.I)
    if official_sources:
        return text[: official_sources.start()] + section + text[official_sources.start() :]
    if re.search(r"</main>", text, flags=re.I):
        return re.sub(r"</main>", section + "</main>", text, count=1, flags=re.I)
    return text


def main() -> None:
    if not SITE.is_dir():
        raise SystemExit("site/ is missing; run python build_site.py first")
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in load_state():
        source = str(item.get("source_url", "")).strip()
        if source.startswith(DOMAIN + "/"):
            grouped[source].append(item)

    touched = 0
    rendered = 0
    for source, items in sorted(grouped.items()):
        path = url_to_path(source)
        if not path or not path.exists():
            continue
        original = path.read_text(encoding="utf-8", errors="replace")
        text = remove_existing(original)
        if is_noindex(text):
            if text != original:
                path.write_text(text, encoding="utf-8")
                touched += 1
            continue
        section = section_for(items)
        if section:
            text = inject(text, section)
            rendered += len(re.findall(r"<li>", section))
        if text != original:
            path.write_text(text, encoding="utf-8")
            touched += 1
    print(f"Continuous growth experience complete: {rendered} contextual links across {touched} pages")


if __name__ == "__main__":
    main()
