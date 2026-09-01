#!/usr/bin/env python3
"""Conservative hourly SEO/keyword review for generated SepticScope pages.

The tool enforces one mapped primary keyword per indexable page and checks titles,
H1s, descriptions, canonicals, link text and intent coverage. It does not add a
meta-keywords tag or repeat phrases merely to change pages; safe mode only repairs
missing essentials with deterministic, readable text.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE = ROOT / "site"
DOMAIN = "https://septicscope.com"
STOPWORDS = {
    "a", "an", "and", "are", "at", "by", "county", "for", "from", "guide", "help",
    "how", "in", "information", "local", "of", "on", "or", "septic", "system", "systems",
    "the", "to", "with", "your", "requirements", "permit", "permits",
}
GENERIC_ANCHORS = {"click here", "here", "learn more", "read more", "more", "view", "go", "details"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title: list[str] = []
        self.h1s: list[str] = []
        self.description = ""
        self.robots = ""
        self.canonical = ""
        self.links: list[tuple[str, str]] = []
        self._capture: str | None = None
        self._buffer: list[str] = []
        self._anchor_href: str | None = None
        self._anchor_text: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr = {str(k).lower(): str(v or "") for k, v in attrs}
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip += 1
            return
        if self._skip:
            return
        if tag in {"title", "h1"}:
            self._capture = tag
            self._buffer = []
        elif tag == "meta":
            name = attr.get("name", "").lower()
            if name == "description":
                self.description = attr.get("content", "").strip()
            elif name == "robots":
                self.robots = attr.get("content", "").strip().lower()
        elif tag == "link" and "canonical" in attr.get("rel", "").lower():
            self.canonical = attr.get("href", "").strip()
        elif tag == "a" and attr.get("href"):
            self._anchor_href = attr["href"].strip()
            self._anchor_text = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"} and self._skip:
            self._skip -= 1
            return
        if self._capture == tag:
            value = clean(" ".join(self._buffer))
            if tag == "title" and value:
                self.title.append(value)
            elif tag == "h1" and value:
                self.h1s.append(value)
            self._capture = None
            self._buffer = []
        if tag == "a" and self._anchor_href is not None:
            self.links.append((self._anchor_href, clean(" ".join(self._anchor_text))))
            self._anchor_href = None
            self._anchor_text = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buffer.append(data)
        if self._anchor_href is not None:
            self._anchor_text.append(data)


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", unescape(str(value or ""))).strip()


def page_url(site: Path, path: Path) -> str:
    rel = path.relative_to(site).as_posix()
    if rel == "index.html":
        return DOMAIN + "/"
    if rel.endswith("/index.html"):
        return DOMAIN + "/" + rel[:-10]
    return DOMAIN + "/" + rel


def expected_canonical(site: Path, path: Path) -> str:
    return page_url(site, path)


def keyword_tokens(keyword: str) -> set[str]:
    return {
        token for token in re.findall(r"[a-z0-9]+", keyword.lower())
        if len(token) >= 3 and token not in STOPWORDS
    }


def keyword_coverage(keyword: str, *fields: str) -> float:
    tokens = keyword_tokens(keyword)
    if not tokens:
        return 1.0
    haystack = " ".join(clean(field).lower() for field in fields)
    present = sum(1 for token in tokens if re.search(rf"\b{re.escape(token)}\b", haystack))
    return present / len(tokens)


def insert_before_head_close(raw: str, fragment: str) -> tuple[str, bool]:
    if "</head>" not in raw.lower():
        return raw, False
    updated, count = re.subn(r"</head>", fragment + "</head>", raw, count=1, flags=re.I)
    return updated, bool(count)


def safe_description(h1: str, keyword: str) -> str:
    subject = clean(h1 or keyword or "SepticScope local septic information")
    base = f"{subject}. Find practical guidance, local requirements, official sources and the next steps to verify for your property."
    return base[:157].rstrip(" ,.;:") + ("." if len(base) <= 158 else "…")


def safe_apply(site: Path, path: Path, parser: PageParser, keyword: str) -> list[str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    changes: list[str] = []
    if not parser.title and parser.h1s:
        title = clean(parser.h1s[0])
        if not title.lower().endswith("septicscope"):
            title = f"{title} | SepticScope"
        raw, count = re.subn(r"<head(\b[^>]*)>", lambda match: match.group(0) + f"<title>{title}</title>", raw, count=1, flags=re.I)
        if count:
            changes.append("added_title")
    if not parser.description:
        description = safe_description(parser.h1s[0] if parser.h1s else "", keyword)
        raw, changed = insert_before_head_close(raw, f'<meta name="description" content="{description}">')
        if changed:
            changes.append("added_meta_description")
    if not parser.canonical:
        canonical = expected_canonical(site, path)
        raw, changed = insert_before_head_close(raw, f'<link rel="canonical" href="{canonical}">')
        if changed:
            changes.append("added_canonical")
    if changes:
        path.write_text(raw, encoding="utf-8")
    return changes


def audit(site: Path, apply_safe: bool, report_path: Path) -> int:
    keyword_file = site / "data" / "keyword-map.json"
    if not keyword_file.exists():
        raise RuntimeError("site/data/keyword-map.json is missing; run the production build first")
    keyword_data = json.loads(keyword_file.read_text(encoding="utf-8"))
    keyword_records = {str(item.get("url", "")): item for item in keyword_data.get("records", []) if isinstance(item, dict)}

    findings: list[dict[str, Any]] = []
    applied: list[dict[str, Any]] = []
    generic_anchor_counts: Counter[str] = Counter()
    indexable = 0
    low_coverage = 0
    hard_errors = 0

    for path in sorted(site.rglob("*.html")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        parser = PageParser()
        parser.feed(raw)
        url = page_url(site, path)
        record = keyword_records.get(url, {})
        is_indexable = "noindex" not in parser.robots and path.name != "404.html"
        if not is_indexable:
            continue
        indexable += 1
        keyword = clean(record.get("primary_keyword", ""))
        page_findings: list[str] = []
        if not keyword:
            page_findings.append("missing_primary_keyword_assignment")
        if not parser.title:
            page_findings.append("missing_title")
        if len(parser.h1s) != 1:
            page_findings.append(f"h1_count_{len(parser.h1s)}")
        if not parser.description:
            page_findings.append("missing_meta_description")
        if not parser.canonical:
            page_findings.append("missing_canonical")
        elif parser.canonical != expected_canonical(site, path):
            page_findings.append("canonical_mismatch")
        coverage = keyword_coverage(keyword, parser.title[0] if parser.title else "", parser.h1s[0] if parser.h1s else "", parser.description)
        if keyword and coverage < 0.50:
            page_findings.append("weak_keyword_intent_match")
            low_coverage += 1
        for href, label in parser.links:
            if clean(label).lower() in GENERIC_ANCHORS and (href.startswith("/") or urlparse(href).hostname in {"septicscope.com", "www.septicscope.com"}):
                generic_anchor_counts[clean(label).lower()] += 1
        if apply_safe and any(item in page_findings for item in ("missing_title", "missing_meta_description", "missing_canonical")):
            changes = safe_apply(site, path, parser, keyword)
            if changes:
                applied.append({"url": url, "changes": changes})
                final_parser = PageParser()
                final_parser.feed(path.read_text(encoding="utf-8", errors="replace"))
                parser = final_parser
                page_findings = [item for item in page_findings if item not in {"missing_title", "missing_meta_description", "missing_canonical"}]
        if any(item in page_findings for item in ("missing_primary_keyword_assignment", "missing_title", "missing_meta_description", "missing_canonical", "canonical_mismatch")) or any(item.startswith("h1_count_") for item in page_findings):
            hard_errors += 1
        if page_findings:
            findings.append({
                "url": url,
                "primary_keyword": keyword,
                "coverage_ratio": round(coverage, 3),
                "findings": page_findings,
                "title": parser.title[0] if parser.title else "",
                "h1": parser.h1s[0] if parser.h1s else "",
            })

    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "site": DOMAIN,
        "indexable_pages_reviewed": indexable,
        "keyword_map_records": len(keyword_records),
        "pages_with_hard_errors": hard_errors,
        "pages_with_weak_intent_match": low_coverage,
        "safe_changes_applied": len(applied),
        "applied": applied,
        "generic_internal_anchor_counts": dict(generic_anchor_counts.most_common()),
        "findings": findings[:500],
        "policy": "No meta-keywords tag and no blind phrase repetition. Safe fixes are limited to missing titles, descriptions and canonicals; content changes require evidence and intent review.",
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"Hourly SEO review: {indexable:,} indexable pages; {hard_errors} hard errors; "
        f"{low_coverage} weak-intent warnings; {len(applied)} safe fixes"
    )
    return 1 if hard_errors else 0


def self_test() -> int:
    assert keyword_tokens("septic tank pumping cost in Denton County") == {"tank", "pumping", "cost", "denton"}
    assert keyword_coverage("septic tank pumping cost", "Septic tank pumping cost in 2026") >= 1.0
    assert keyword_coverage("septic tank pumping cost", "Drainfield repair guide") < 0.5
    description = safe_description("Septic Tank Pumping Cost", "septic tank pumping cost")
    assert 80 <= len(description) <= 160
    print("PASS: hourly SEO audit self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", default=str(DEFAULT_SITE))
    parser.add_argument("--report", default=str(ROOT / "hourly-seo-report.json"))
    parser.add_argument("--apply-safe", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    return audit(Path(args.site), args.apply_safe, Path(args.report))


if __name__ == "__main__":
    raise SystemExit(main())
