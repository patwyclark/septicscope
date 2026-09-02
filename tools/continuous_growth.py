#!/usr/bin/env python3
"""Find and apply one conservative, compounding SepticScope improvement per run.

The planner reads the built site's real internal-link graph, county coverage,
provider coverage, keyword map, and review dates. It may add one contextual
internal-link relationship to source-controlled data when a useful opportunity
exists. It never generates filler text, changes regulations, removes noindex,
or creates pages merely to satisfy an hourly quota.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import tempfile
from typing import Any
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://septicscope.com"
DEFAULT_SITE = ROOT / "site"
DEFAULT_STATE = ROOT / "data" / "growth-links.json"
DEFAULT_REPORT = ROOT / "hourly-continuous-growth-report.json"

STOPWORDS = {
    "a", "about", "an", "and", "are", "at", "by", "county", "for", "from",
    "guide", "guides", "help", "how", "in", "information", "local", "of", "on",
    "or", "septic", "system", "systems", "the", "to", "with", "your",
}
LEGAL_PATHS = {"/about/", "/contact/", "/corrections/", "/privacy/", "/sources/"}
MAX_LINKS_PER_SOURCE = 3

TOPIC_GROUPS: dict[str, set[str]] = {
    "inspection_real_estate": {"inspection", "inspect", "buyer", "buying", "selling", "sale", "real", "estate", "homebuyer", "transfer"},
    "maintenance_pumping": {"maintenance", "maintain", "pumping", "pump", "flush", "wipes", "cleaning", "care"},
    "failure_repair": {"failure", "failed", "repair", "replacement", "drainfield", "backup", "odor", "alarm", "wet", "yard", "lifespan"},
    "design_system_type": {"design", "size", "tank", "bedroom", "aerobic", "mound", "chamber", "types", "installation"},
    "winter_seasonal": {"winter", "frozen", "freeze", "seasonal", "cold"},
    "permit_records": {"permit", "requirements", "regulations", "records", "authority", "application", "county"},
}

CONTENT_GAP_CATALOG = [
    {
        "slug": "septic-permit-process",
        "title": "Septic permit process explained",
        "intent": "Homeowner wants the steps, documents, inspections, and approval sequence before installation or repair.",
    },
    {
        "slug": "failed-septic-inspection-home-sale",
        "title": "What happens after a failed septic inspection during a home sale",
        "intent": "Buyer or seller needs negotiation, repair, permit, and closing guidance without unsupported legal claims.",
    },
    {
        "slug": "septic-vs-sewer",
        "title": "Septic vs. public sewer comparison",
        "intent": "Homebuyer compares ownership duties, recurring costs, failure risk, utility bills, and property constraints.",
    },
    {
        "slug": "septic-alarm-troubleshooting",
        "title": "Septic alarm troubleshooting and immediate actions",
        "intent": "Homeowner sees a high-water or pump alarm and needs safe steps before a technician arrives.",
    },
    {
        "slug": "septic-odor-troubleshooting",
        "title": "Septic odor troubleshooting by location",
        "intent": "Homeowner needs to distinguish indoor plumbing odors, tank odors, vent issues, and drainfield symptoms.",
    },
    {
        "slug": "septic-records-request-checklist",
        "title": "Septic permit and as-built records request checklist",
        "intent": "Owner or buyer needs a reusable checklist for locating permits, plans, inspection history, and maintenance records.",
    },
    {
        "slug": "septic-glossary",
        "title": "Septic and onsite wastewater glossary",
        "intent": "Reader needs plain-language definitions that connect technical terms to deeper guides and county requirements.",
    },
]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.h1_parts: list[str] = []
        self.description = ""
        self.robots = ""
        self.canonical = ""
        self.links: list[tuple[str, str]] = []
        self._capture: str | None = None
        self._buffer: list[str] = []
        self._anchor_href: str | None = None
        self._anchor_text: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr = {str(key).lower(): str(value or "") for key, value in attrs}
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if tag in {"title", "h1"}:
            self._capture = tag
            self._buffer = []
        elif tag == "meta":
            name = attr.get("name", "").lower()
            if name == "description":
                self.description = clean(attr.get("content", ""))
            elif name == "robots":
                self.robots = clean(attr.get("content", "")).lower()
        elif tag == "link" and "canonical" in attr.get("rel", "").lower():
            self.canonical = clean(attr.get("href", ""))
        elif tag == "a" and attr.get("href"):
            self._anchor_href = attr["href"].strip()
            self._anchor_text = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1
            return
        if self._capture == tag:
            value = clean(" ".join(self._buffer))
            if tag == "title" and value:
                self.title_parts.append(value)
            elif tag == "h1" and value:
                self.h1_parts.append(value)
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


def site_url(site: Path, path: Path) -> str:
    relative = path.relative_to(site).as_posix()
    if relative == "index.html":
        return DOMAIN + "/"
    if relative.endswith("/index.html"):
        return DOMAIN + "/" + relative[:-10]
    return DOMAIN + "/" + relative


def normalize_internal(base_url: str, href: str) -> str | None:
    href = clean(href)
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    resolved = urljoin(base_url, href)
    parsed = urlparse(resolved)
    if parsed.hostname not in {"septicscope.com", "www.septicscope.com"}:
        return None
    path = parsed.path or "/"
    if path.endswith("/index.html"):
        path = path[:-10]
    elif path.endswith(".html"):
        return DOMAIN + path
    elif not path.endswith("/"):
        path += "/"
    return DOMAIN + path


def classify(url: str) -> str:
    path = urlparse(url).path
    parts = [part for part in path.split("/") if part]
    if path == "/":
        return "homepage"
    if path in LEGAL_PATHS:
        return "legal"
    if parts == ["counties"]:
        return "county_directory"
    if len(parts) == 2 and parts[0] == "counties":
        return "state_hub"
    if len(parts) == 3 and parts[0] == "counties":
        return "county_page"
    if parts == ["guides"]:
        return "guide_hub"
    if len(parts) == 2 and parts[0] == "guides":
        return "guide"
    if parts == ["faq"]:
        return "faq_hub"
    if len(parts) == 2 and parts[0] == "faq":
        return "faq_article"
    if parts == ["providers"]:
        return "provider_directory"
    return "other"


def url_slug(url: str) -> str:
    parts = [part for part in urlparse(url).path.split("/") if part]
    return parts[-1] if parts else "home"


def tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", clean(value).lower())
        if len(token) >= 3 and token not in STOPWORDS
    }


def topic_labels(value: str) -> set[str]:
    words = tokens(value)
    return {
        label for label, vocabulary in TOPIC_GROUPS.items()
        if words.intersection(vocabulary)
    }


@dataclass
class Page:
    url: str
    path: Path
    title: str
    h1: str
    description: str
    page_type: str
    indexable: bool
    outgoing: set[str] = field(default_factory=set)
    anchor_labels: dict[str, str] = field(default_factory=dict)
    inbound: int = 0

    @property
    def text(self) -> str:
        return " ".join((self.title, self.h1, self.description))



def scan_site(site: Path) -> dict[str, Page]:
    pages: dict[str, Page] = {}
    raw_links: dict[str, list[tuple[str, str]]] = {}
    for path in sorted(site.rglob("*.html")):
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        derived = site_url(site, path)
        canonical = parser.canonical if parser.canonical.startswith(DOMAIN) else derived
        page = Page(
            url=canonical,
            path=path,
            title=parser.title_parts[0] if parser.title_parts else "",
            h1=parser.h1_parts[0] if parser.h1_parts else "",
            description=parser.description,
            page_type=classify(canonical),
            indexable="noindex" not in parser.robots and path.name != "404.html",
        )
        pages[canonical] = page
        raw_links[canonical] = parser.links

    for url, link_rows in raw_links.items():
        page = pages[url]
        for href, label in link_rows:
            target = normalize_internal(url, href)
            if not target or target == url:
                continue
            page.outgoing.add(target)
            if label:
                page.anchor_labels[target] = label
    inbound = Counter(target for page in pages.values() for target in page.outgoing if target in pages)
    for url, page in pages.items():
        page.inbound = inbound[url]
    return pages


def load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected a JSON object in {path}")
    return data


def state_links(state: dict[str, Any]) -> list[dict[str, Any]]:
    links = state.get("links", [])
    if not isinstance(links, list):
        raise RuntimeError("data/growth-links.json must contain a links array")
    return [item for item in links if isinstance(item, dict)]


def semantic_score(source: Page, target: Page) -> float:
    source_tokens = tokens(source.text)
    target_tokens = tokens(target.text)
    overlap = len(source_tokens.intersection(target_tokens))
    source_topics = topic_labels(source.text)
    target_topics = topic_labels(target.text)
    topic_overlap = len(source_topics.intersection(target_topics))
    score = overlap * 2.0 + topic_overlap * 7.0

    if source.page_type == "guide" and target.page_type == "guide":
        score += 8.0
    elif source.page_type == "faq_article" and target.page_type == "guide":
        score += 9.0
    elif source.page_type == "county_page" and target.page_type == "guide":
        score += 6.0
    elif source.page_type == "state_hub" and target.page_type == "county_page":
        source_parts = urlparse(source.url).path.strip("/").split("/")
        target_parts = urlparse(target.url).path.strip("/").split("/")
        if len(source_parts) >= 2 and len(target_parts) >= 3 and source_parts[1] == target_parts[1]:
            score += 20.0
        else:
            score -= 20.0
    else:
        score -= 3.0

    score += max(0.0, 5.0 - min(target.inbound, 5))
    return score


def source_candidates(pages: dict[str, Page], overrides: list[dict[str, Any]]) -> list[Page]:
    counts = Counter(clean(item.get("source_url", "")) for item in overrides)
    allowed = {"guide", "faq_article", "county_page", "state_hub", "guide_hub", "faq_hub", "county_directory"}
    candidates = [
        page for page in pages.values()
        if page.indexable
        and page.page_type in allowed
        and counts[page.url] < MAX_LINKS_PER_SOURCE
        and urlparse(page.url).path not in LEGAL_PATHS
    ]
    weights = {
        "guide": 0,
        "faq_article": 1,
        "state_hub": 2,
        "county_page": 3,
        "guide_hub": 4,
        "faq_hub": 5,
        "county_directory": 6,
    }
    candidates.sort(key=lambda page: (counts[page.url], len(page.outgoing), weights.get(page.page_type, 9), page.inbound, page.url))
    return candidates


def target_candidates(source: Page, pages: dict[str, Page], overrides: list[dict[str, Any]]) -> list[Page]:
    override_pairs = {(clean(item.get("source_url", "")), clean(item.get("target_url", ""))) for item in overrides}
    result: list[Page] = []
    for target in pages.values():
        if not target.indexable or target.url == source.url:
            continue
        if target.page_type in {"legal", "homepage", "other"}:
            continue
        if target.url in source.outgoing or (source.url, target.url) in override_pairs:
            continue
        if source.page_type in {"guide", "faq_article", "guide_hub", "faq_hub"} and target.page_type not in {"guide", "faq_article", "guide_hub", "faq_hub", "county_directory", "provider_directory"}:
            continue
        if source.page_type == "county_page" and target.page_type not in {"guide", "provider_directory", "state_hub"}:
            continue
        if source.page_type == "state_hub" and target.page_type not in {"county_page", "guide", "provider_directory"}:
            continue
        if source.page_type == "county_directory" and target.page_type not in {"state_hub", "guide", "provider_directory"}:
            continue
        result.append(target)
    result.sort(key=lambda target: (-semantic_score(source, target), target.inbound, target.url))
    return result


def anchor_text(target: Page) -> str:
    value = clean(target.h1 or target.title.split("|")[0] or url_slug(target.url).replace("-", " ").title())
    value = re.sub(r"^(How to|What is|What are)\s+", "", value, flags=re.I)
    if len(value) > 82:
        value = value[:79].rsplit(" ", 1)[0] + "…"
    return value


def summary_for(source: Page, target: Page) -> str:
    target_type = target.page_type
    if target_type == "guide":
        return "Use this related homeowner guide for the next practical decision, checklist, or maintenance step."
    if target_type == "faq_article":
        return "Read the focused answer for a closely related septic question."
    if target_type == "county_page":
        return "Continue to the local permitting authority, process, contacts, and official sources for this area."
    if target_type == "state_hub":
        return "Browse verified and in-progress county guidance throughout this state."
    if target_type == "provider_directory":
        return "Compare source-checked local septic service listings and verify current credentials before hiring."
    return "Continue with this related SepticScope resource."


def choose_improvement(pages: dict[str, Page], overrides: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    opportunities: list[dict[str, Any]] = []
    selected: dict[str, Any] | None = None
    for source in source_candidates(pages, overrides):
        targets = target_candidates(source, pages, overrides)
        if not targets:
            continue
        target = targets[0]
        score = semantic_score(source, target)
        # Require a meaningful relationship. County-to-guide and same-state hub links
        # receive explicit type bonuses, while unrelated pairs remain below threshold.
        if score < 7.0:
            continue
        candidate = {
            "source_url": source.url,
            "target_url": target.url,
            "anchor_text": anchor_text(target),
            "summary": summary_for(source, target),
            "source_page_type": source.page_type,
            "target_page_type": target.page_type,
            "reason": "contextual_internal_link_for_underlinked_or_low-navigation_page",
            "source_outgoing_internal_links": len(source.outgoing),
            "target_inbound_internal_links": target.inbound,
            "relevance_score": round(score, 2),
        }
        opportunities.append(candidate)
        if selected is None:
            selected = candidate
        if len(opportunities) >= 25:
            break
    return selected, opportunities


def coverage_backlog(site: Path) -> dict[str, Any]:
    manifest = load_json(site / "data" / "national-coverage-manifest.json", {"records": []})
    records = [item for item in manifest.get("records", []) if isinstance(item, dict)]
    today = date.today().isoformat()
    verified_without_provider = [
        item for item in records
        if item.get("verification_status") == "verified"
        and int(item.get("local_service_provider_count") or 0) == 0
    ]
    stale = [
        item for item in records
        if item.get("verification_status") == "verified"
        and item.get("next_review_date")
        and str(item.get("next_review_date")) <= today
    ]
    missing_review_date = [
        item for item in records
        if item.get("verification_status") == "verified" and not item.get("date_last_reviewed")
    ]
    return {
        "verified_counties_without_provider_count": len(verified_without_provider),
        "verified_counties_without_provider_sample": [
            {
                "state": item.get("state"),
                "county": item.get("county_or_equivalent_name"),
                "url": item.get("page_url"),
            }
            for item in verified_without_provider[:25]
        ],
        "verified_guides_due_for_source_review_count": len(stale),
        "verified_guides_due_for_source_review_sample": [
            {
                "state": item.get("state"),
                "county": item.get("county_or_equivalent_name"),
                "url": item.get("page_url"),
                "next_review_date": item.get("next_review_date"),
            }
            for item in stale[:25]
        ],
        "verified_guides_missing_review_date_count": len(missing_review_date),
    }


def content_gaps(pages: dict[str, Page]) -> list[dict[str, str]]:
    live_slugs = {url_slug(url) for url, page in pages.items() if page.indexable}
    return [item for item in CONTENT_GAP_CATALOG if item["slug"] not in live_slugs]


def write_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")


def run(site: Path, state_path: Path, report_path: Path, apply_one: bool) -> int:
    if not site.is_dir():
        raise RuntimeError(f"Built site directory does not exist: {site}")
    pages = scan_site(site)
    state = load_json(
        state_path,
        {
            "schema_version": 1,
            "last_updated": date.today().isoformat(),
            "policy": "Contextual internal links only; no filler or keyword stuffing.",
            "links": [],
        },
    )
    overrides = state_links(state)
    selected, opportunities = choose_improvement(pages, overrides)
    applied: dict[str, Any] | None = None

    if apply_one and selected:
        applied = dict(selected)
        applied["date_added"] = date.today().isoformat()
        applied["id"] = f"{url_slug(applied['source_url'])}-to-{url_slug(applied['target_url'])}-{len(overrides)+1:04d}"
        overrides.append(applied)
        state["links"] = overrides
        state["last_updated"] = date.today().isoformat()
        write_state(state_path, state)

    indexable_pages = [page for page in pages.values() if page.indexable]
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "site": DOMAIN,
        "mode": "apply_one_safe_improvement" if apply_one else "plan_only",
        "indexable_pages_reviewed": len(indexable_pages),
        "existing_growth_link_records": len(overrides),
        "selected_improvement": selected,
        "applied_improvement": applied,
        "changed_urls": [applied["source_url"]] if applied else [],
        "top_internal_link_opportunities": opportunities,
        "coverage_backlog": coverage_backlog(site),
        "remaining_content_gap_candidates": content_gaps(pages),
        "quality_policy": "Apply no change when a meaningful, supportable improvement is unavailable. Regulatory claims, indexability, and new article text are never generated automatically.",
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if applied:
        print(f"Continuous growth: added contextual link from {applied['source_url']} to {applied['target_url']}")
    elif selected:
        print(f"Continuous growth plan: next safe link is {selected['source_url']} -> {selected['target_url']}")
    else:
        print("Continuous growth: no evidence-backed automatic change available; report generated")
    return 0


def self_test() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        site = root / "site"
        for relative, title, h1, links in (
            ("guides/maintenance/index.html", "Septic Maintenance Checklist | SepticScope", "Septic Maintenance Checklist", ["/guides/"]),
            ("guides/pumping/index.html", "Septic Pumping Cost | SepticScope", "Septic Pumping Cost", ["/guides/"]),
            ("guides/index.html", "Septic Guides | SepticScope", "Septic System Homeowner Guides", ["/guides/maintenance/", "/guides/pumping/"]),
        ):
            path = site / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            url = DOMAIN + "/" + relative.removesuffix("index.html")
            anchors = "".join(f'<a href="{href}">Resource</a>' for href in links)
            path.write_text(
                f'<!doctype html><html><head><title>{title}</title><meta name="description" content="Maintenance and pumping guidance"><link rel="canonical" href="{url}"></head><body><main><h1>{h1}</h1>{anchors}</main></body></html>',
                encoding="utf-8",
            )
        (site / "data").mkdir(parents=True, exist_ok=True)
        (site / "data" / "national-coverage-manifest.json").write_text('{"records": []}\n')
        state = root / "growth-links.json"
        report = root / "report.json"
        run(site, state, report, apply_one=True)
        state_data = json.loads(state.read_text())
        assert len(state_data["links"]) == 1
        assert json.loads(report.read_text())["changed_urls"]
    print("PASS: continuous growth planner self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", default=str(DEFAULT_SITE))
    parser.add_argument("--state", default=str(DEFAULT_STATE))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--apply-one", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    return run(Path(args.site), Path(args.state), Path(args.report), args.apply_one)


if __name__ == "__main__":
    raise SystemExit(main())
