"""County-specific Barren River quality improvements backed by current BRDHD sources."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "site"
BRDHD_LOGAN = "https://www.barrenriverhealth.org/locations/logan-county-health-department"
BRDHD_METCALFE = "https://www.barrenriverhealth.org/locations/metcalfe-county-health-department"
BRDHD_WARREN = "https://www.barrenriverhealth.org/locations/warren-county-health-department"


def enhance_logan() -> None:
    page = OUTPUT / "counties" / "kentucky" / "logan" / "index.html"
    if not page.exists():
        raise RuntimeError("Expected verified Logan County page is missing")

    text = page.read_text(encoding="utf-8")
    heading = "Logan County onsite-sewage contact and forms"
    if heading not in text:
        section = (
            "<h2>Logan County onsite-sewage contact and forms</h2>"
            "<p>Barren River District Health Department currently lists Rebecca Tyree, RN, CLC, "
            "at 270-781-8039 ext. 326 as the associated onsite-sewage contact for Butler, Logan, "
            "and Simpson counties. The district’s onsite-sewage page also publishes the DFS-319 "
            "site-evaluation application, DFS-326 existing-sewage-system application, DFS-330 "
            "installer affidavit, and BRDHD owner affidavit. For Logan County, BRDHD lists the "
            "Logan County Health Department at 151 S. Franklin Street, Russellville, KY 42276, "
            "phone 270-726-8341, with public hours of 8:00 a.m. to 4:00 p.m. Monday through "
            "Friday. Confirm current office availability and the forms required for the specific "
            "project before submitting or scheduling work.</p>"
        )
        marker = "<h2>Official sources</h2>"
        if marker not in text:
            raise RuntimeError("Logan County official-sources marker is missing")
        text = text.replace(marker, section + marker, 1)

    source = (
        f'<li><a href="{BRDHD_LOGAN}" rel="nofollow">'
        "Barren River District Health Department — Logan County Health Department"
        "</a></li>"
    )
    sources_marker = "<h2>Official sources</h2><ul>"
    if BRDHD_LOGAN not in text:
        if sources_marker not in text:
            raise RuntimeError("Logan County official-source list is missing")
        text = text.replace(sources_marker, sources_marker + source, 1)

    text = re.sub(
        r"Official sources checked [^<]+",
        "Official sources checked September 8, 2026",
        text,
        count=1,
    )
    page.write_text(text, encoding="utf-8")

    if heading not in text or BRDHD_LOGAN not in text:
        raise RuntimeError("Logan County quality enhancement failed")


def enhance_metcalfe() -> None:
    page = OUTPUT / "counties" / "kentucky" / "metcalfe" / "index.html"
    if not page.exists():
        raise RuntimeError("Expected verified Metcalfe County page is missing")

    text = page.read_text(encoding="utf-8")
    heading = "Metcalfe County onsite-sewage contact and local office"
    if heading not in text:
        section = (
            "<h2>Metcalfe County onsite-sewage contact and local office</h2>"
            "<p>Barren River District Health Department currently lists Katie Matthews, RN, at "
            "270-432-3214 ext. 483 as the associated onsite-sewage contact for Barren, Hart, and "
            "Metcalfe counties. The district’s onsite-sewage program performs soil evaluations, "
            "reviews installation drawings before permits are issued, and inspects systems after "
            "installation; its current page also publishes the DFS-319 site-evaluation application, "
            "DFS-326 existing-sewage-system application, DFS-330 installer affidavit, and BRDHD "
            "owner affidavit. BRDHD lists the Metcalfe County Health Department at 615 West "
            "Stockton Street, Edmonton, KY 42129, phone 270-432-3214, with public hours of "
            "8:00 a.m. to 4:00 p.m. Monday through Friday. Confirm current staff availability and "
            "the forms required for the specific project before submitting plans or scheduling an "
            "evaluation.</p>"
        )
        marker = "<h2>Official sources</h2>"
        if marker not in text:
            raise RuntimeError("Metcalfe County official-sources marker is missing")
        text = text.replace(marker, section + marker, 1)

    source = (
        f'<li><a href="{BRDHD_METCALFE}" rel="nofollow">'
        "Barren River District Health Department — Metcalfe County Health Department"
        "</a></li>"
    )
    sources_marker = "<h2>Official sources</h2><ul>"
    if BRDHD_METCALFE not in text:
        if sources_marker not in text:
            raise RuntimeError("Metcalfe County official-source list is missing")
        text = text.replace(sources_marker, sources_marker + source, 1)

    text = re.sub(
        r"Official sources checked [^<]+",
        "Official sources checked September 8, 2026",
        text,
        count=1,
    )
    page.write_text(text, encoding="utf-8")

    if heading not in text or BRDHD_METCALFE not in text:
        raise RuntimeError("Metcalfe County quality enhancement failed")


def enhance_warren() -> None:
    page = OUTPUT / "counties" / "kentucky" / "warren" / "index.html"
    if not page.exists():
        raise RuntimeError("Expected verified Warren County page is missing")

    text = page.read_text(encoding="utf-8")
    heading = "Warren County onsite-sewage contact and local office"
    if heading not in text:
        section = (
            "<h2>Warren County onsite-sewage contact and local office</h2>"
            "<p>Barren River District Health Department currently lists Brenna Wilson, RN, at "
            "270-597-2194 ext. 302 as the associated onsite-sewage contact for Edmonson and "
            "Warren counties. BRDHD says its onsite-sewage team conducts soil evaluations, "
            "reviews installation drawings before issuing permits, and inspects systems after "
            "installation. The district also publishes the DFS-319 site-evaluation application, "
            "DFS-326 existing-sewage-system application, DFS-330 installer affidavit, and BRDHD "
            "owner affidavit. For local assistance, BRDHD lists the Warren County Health "
            "Department at 1109 State Street, Bowling Green, KY 42101, phone 270-781-2490, with "
            "public hours of 8:00 a.m. to 4:00 p.m. Monday through Friday. Confirm current staff "
            "availability and the forms required for the specific property before submitting plans "
            "or scheduling an evaluation.</p>"
        )
        marker = "<h2>Official sources</h2>"
        if marker not in text:
            raise RuntimeError("Warren County official-sources marker is missing")
        text = text.replace(marker, section + marker, 1)

    source = (
        f'<li><a href="{BRDHD_WARREN}" rel="nofollow">'
        "Barren River District Health Department — Warren County Health Department"
        "</a></li>"
    )
    sources_marker = "<h2>Official sources</h2><ul>"
    if BRDHD_WARREN not in text:
        if sources_marker not in text:
            raise RuntimeError("Warren County official-source list is missing")
        text = text.replace(sources_marker, sources_marker + source, 1)

    text = re.sub(
        r"Official sources checked [^<]+",
        "Official sources checked September 8, 2026",
        text,
        count=1,
    )
    page.write_text(text, encoding="utf-8")

    if heading not in text or BRDHD_WARREN not in text:
        raise RuntimeError("Warren County quality enhancement failed")


if __name__ == "__main__":
    enhance_logan()
    enhance_metcalfe()
    enhance_warren()
    print(
        "Kentucky Barren River quality pass complete: "
        "Logan, Metcalfe, and Warren local guidance refreshed"
    )
