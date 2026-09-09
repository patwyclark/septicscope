#!/usr/bin/env python3
"""Apply the final conservative publication threshold to county guides.

The first recovery pass gathers evidence and calculates similarity. This second pass
keeps only the strongest local pages so a borderline 300-word county template cannot
remain public merely because it barely crossed the initial diagnostic threshold.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

import quality_recovery as recovery

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
REPORT = SITE / "data" / "adsense-quality-recovery.json"
REPORT_TEXT = SITE / "data" / "adsense-quality-recovery.txt"
LOOKUP = SITE / "data" / "county-lookup.json"
DOMAIN = "https://septicscope.com"

THRESHOLDS = {
    "minimum_main_words": 350,
    "minimum_external_sources": 5,
    "minimum_local_sources": 2,
    "minimum_local_detail_score": 5,
    "maximum_shared_template_ratio": 0.35,
    "maximum_public_county_guides": 100,
}


def route_path(url: str) -> Path:
    path = urlparse(url).path.strip("/")
    return SITE / path / "index.html"


def state_hub_for_lookup(row: dict) -> str:
    state = str(row.get("s", "")).lower()
    state_slug = re.sub(r"[^a-z0-9]+", "-", state).strip("-")
    return f"/counties/{state_slug}/"


def passes(item: dict) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if int(item.get("main_words", 0)) < THRESHOLDS["minimum_main_words"]:
        reasons.append("strict_main_content_depth")
    if int(item.get("external_sources", 0)) < THRESHOLDS["minimum_external_sources"]:
        reasons.append("strict_source_count")
    if int(item.get("local_sources", 0)) < THRESHOLDS["minimum_local_sources"]:
        reasons.append("strict_local_source_count")
    if int(item.get("local_detail_score", 0)) < THRESHOLDS["minimum_local_detail_score"]:
        reasons.append("strict_local_detail_depth")
    if float(item.get("shared_template_ratio", 1.0)) > THRESHOLDS["maximum_shared_template_ratio"]:
        reasons.append("strict_template_similarity")
    if not str(item.get("authority", "")).strip():
        reasons.append("missing_identified_authority")
    return not reasons, reasons


def filter_sitemap(approved_urls: set[str]) -> int:
    sitemap = SITE / "sitemap.xml"
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    tree = ET.parse(sitemap)
    root = tree.getroot()
    for node in list(root):
        loc = node.find(f"{{{ns}}}loc")
        url = str(loc.text or "").strip() if loc is not None else ""
        if "/counties/" in url and url != f"{DOMAIN}/counties/" and url not in approved_urls:
            root.remove(node)
    tree.write(sitemap, encoding="utf-8", xml_declaration=True)
    return len(root.findall(f"{{{ns}}}url"))


def write_text_report(report: dict) -> None:
    REPORT_TEXT.write_text(
        "\n".join([
            "SepticScope AdSense/search quality recovery",
            f"Generated: {report.get('generated_at', '')}",
            f"County pages scanned: {report.get('county_pages_scanned', 0)}",
            f"Previously indexable county candidates: {report.get('previously_indexable_county_candidates', 0)}",
            f"Quality-approved county guides: {report.get('quality_approved_counties', 0)}",
            f"Withheld county pages: {report.get('quality_withheld_counties', 0)}",
            f"State hubs made noindex/ad-free: {report.get('state_hubs_noindex_ad_free', 0)}",
            f"FAQ leaves consolidated: {report.get('faq_leaf_pages_consolidated', 0)}",
            f"Retained long-form guides: {report.get('retained_long_form_guides', 0)}",
            f"Final sitemap URLs: {report.get('sitemap_urls', 0)}",
            "Strict county thresholds: " + json.dumps(THRESHOLDS, sort_keys=True),
            "",
        ]),
        encoding="utf-8",
    )


def apply() -> dict:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    initial = [item for item in report.get("approved_counties", []) if isinstance(item, dict)]
    retained: list[dict] = []
    newly_withheld: list[dict] = []
    for item in initial:
        ok, reasons = passes(item)
        if ok:
            retained.append(item)
            continue
        demoted = dict(item)
        demoted["decision_reasons"] = list(dict.fromkeys(list(item.get("decision_reasons", [])) + reasons))
        newly_withheld.append(demoted)
        path = route_path(str(item.get("url", "")))
        if not path.exists():
            raise RuntimeError(f"Strict recovery county page is missing: {item.get('url')}")
        raw = path.read_text(encoding="utf-8", errors="replace")
        path.write_text(
            recovery.strip_ads(recovery.ensure_noindex(raw, "withheld-strict-local-quality")),
            encoding="utf-8",
        )

    retained.sort(
        key=lambda item: (
            -int(item.get("local_detail_score", 0)),
            float(item.get("shared_template_ratio", 1)),
            -int(item.get("main_words", 0)),
            str(item.get("route", "")),
        )
    )
    if len(retained) > THRESHOLDS["maximum_public_county_guides"]:
        overflow = retained[THRESHOLDS["maximum_public_county_guides"]:]
        retained = retained[:THRESHOLDS["maximum_public_county_guides"]]
        for item in overflow:
            demoted = dict(item)
            demoted["decision_reasons"] = list(dict.fromkeys(list(item.get("decision_reasons", [])) + ["strict_public_footprint_ceiling"]))
            newly_withheld.append(demoted)
            path = route_path(str(item.get("url", "")))
            raw = path.read_text(encoding="utf-8", errors="replace")
            path.write_text(
                recovery.strip_ads(recovery.ensure_noindex(raw, "withheld-strict-footprint-ceiling")),
                encoding="utf-8",
            )

    retained_fips = {str(item.get("fips", "")) for item in retained if re.fullmatch(r"\d{5}", str(item.get("fips", "")))}
    retained_urls = {str(item.get("url", "")) for item in retained}

    lookup = json.loads(LOOKUP.read_text(encoding="utf-8"))
    for row in lookup.get("counties", []):
        fips = str(row.get("f", ""))
        if fips in retained_fips:
            row["v"] = True
        else:
            row["v"] = False
            row["u"] = state_hub_for_lookup(row)
            row["o"] = ""
            row["r"] = ""
    LOOKUP.write_text(json.dumps(lookup, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    report["strict_gate"] = THRESHOLDS
    report["initial_quality_approved_counties"] = len(initial)
    report["strict_gate_newly_withheld_counties"] = len(newly_withheld)
    report["approved_counties"] = retained
    report["approved_county_fips"] = sorted(retained_fips)
    report["demoted_counties"] = list(report.get("demoted_counties", [])) + newly_withheld
    report["quality_approved_counties"] = len(retained)
    report["quality_withheld_counties"] = int(report.get("county_pages_scanned", 3144)) - len(retained)

    recovery.build_homepage(retained, list(report.get("retained_guide_routes", [])))
    report["sitemap_urls"] = filter_sitemap(retained_urls)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_text_report(report)
    print(
        f"Strict county quality gate: {len(retained)} retained from {len(initial)}; "
        f"{len(newly_withheld)} newly withheld; sitemap {report['sitemap_urls']} URLs"
    )
    return report


def check() -> int:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    errors: list[str] = []
    gate = report.get("strict_gate")
    if gate != THRESHOLDS:
        errors.append(f"Strict gate configuration drift: {gate}")
    approved = [item for item in report.get("approved_counties", []) if isinstance(item, dict)]
    if not 20 <= len(approved) <= THRESHOLDS["maximum_public_county_guides"]:
        errors.append(f"Unexpected strict county count: {len(approved)}")
    for item in approved:
        ok, reasons = passes(item)
        if not ok:
            errors.append(f"Approved county fails strict gate: {item.get('url')} — {reasons}")
    lookup = json.loads(LOOKUP.read_text(encoding="utf-8"))
    flagged = {str(row.get("f")) for row in lookup.get("counties", []) if row.get("v")}
    expected = {str(item.get("fips")) for item in approved}
    if flagged != expected:
        errors.append(f"County lookup strict flags drift: {len(flagged)} versus {len(expected)}")
    if errors:
        print("STRICT RECOVERY ERRORS:")
        for error in errors[:100]:
            print(" -", error)
        return 1
    print(f"PASS: strict recovery retains {len(approved)} locally differentiated county guides")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        return check()
    apply()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
