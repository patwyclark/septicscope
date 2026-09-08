"""County-specific Northern Kentucky quality improvements backed by current NKY Health sources."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "site"
NKY_LOCATIONS = "https://nkyhealth.org/ourlocations/"
NKY_REQUESTS = "https://nkyhealth.org/requests/"


def _add_source(text: str, url: str, label: str, county: str) -> str:
    if url in text:
        return text
    marker = "<h2>Official sources</h2><ul>"
    if marker not in text:
        raise RuntimeError(f"{county} County official-source list is missing")
    source = f'<li><a href="{url}" rel="nofollow">{label}</a></li>'
    return text.replace(marker, marker + source, 1)


def _refresh_review_date(text: str) -> str:
    return re.sub(
        r"Official sources checked [^<]+",
        "Official sources checked September 8, 2026",
        text,
        count=1,
    )


def enhance_boone() -> None:
    page = OUTPUT / "counties" / "kentucky" / "boone" / "index.html"
    if not page.exists():
        raise RuntimeError("Expected verified Boone County page is missing")

    text = page.read_text(encoding="utf-8")
    heading = "Boone County local office and septic records"
    if heading not in text:
        section = (
            "<h2>Boone County local office and septic records</h2>"
            "<p>Northern Kentucky Health Department lists the Boone County Health Center at "
            "7505 Burlington Pike, Florence, KY 41042, phone 859-363-2060. Septic permitting "
            "and inspection work is handled through the district Environmental Health and Safety "
            "program; NKY Health says its District Office at 8001 Veterans Memorial Drive in "
            "Florence is where environmental-health permit and inspection fees, plans, forms, "
            "and associated costs can be handled. For an existing onsite-sewage record, NKY "
            "Health requires both its Open Records Request Form and its Onsite Sewage Request "
            "for Public Records Attachment Form. The septic program also accepts requests to "
            "inspect an existing system for situations such as a home sale, building addition, "
            "or rebuilding after a natural disaster. Check the current NKY Health instructions "
            "before submitting forms or scheduling an inspection.</p>"
        )
        marker = "<h2>Official sources</h2>"
        if marker not in text:
            raise RuntimeError("Boone County official-sources marker is missing")
        text = text.replace(marker, section + marker, 1)

    text = _add_source(
        text,
        NKY_LOCATIONS,
        "Northern Kentucky Health Department — locations and Boone County Health Center",
        "Boone",
    )
    text = _add_source(
        text,
        NKY_REQUESTS,
        "Northern Kentucky Health Department — public records and onsite-septic records requests",
        "Boone",
    )
    text = _refresh_review_date(text)
    page.write_text(text, encoding="utf-8")

    if heading not in text or NKY_LOCATIONS not in text or NKY_REQUESTS not in text:
        raise RuntimeError("Boone County quality enhancement failed")


def enhance_campbell() -> None:
    page = OUTPUT / "counties" / "kentucky" / "campbell" / "index.html"
    if not page.exists():
        raise RuntimeError("Expected verified Campbell County page is missing")

    text = page.read_text(encoding="utf-8")
    heading = "Campbell County local office and septic records"
    if heading not in text:
        section = (
            "<h2>Campbell County local office and septic records</h2>"
            "<p>Northern Kentucky Health Department lists the Campbell County Health Center at "
            "1098 Monmouth St., Newport, KY 41071, Suite 130 on the first floor of the Campbell "
            "County Fiscal Court building, phone 859-431-1704. Septic permitting and inspection "
            "work is handled through the district Environmental Health and Safety program; NKY "
            "Health says its District Office at 8001 Veterans Memorial Drive in Florence is where "
            "environmental-health permit and inspection fees, plans, forms, and associated costs "
            "can be handled. For an existing onsite-sewage record, NKY Health requires both its "
            "Open Records Request Form and its Onsite Sewage Request for Public Records Attachment "
            "Form. The septic program also accepts requests to inspect an existing system for a "
            "home sale, building addition, or rebuild after a natural disaster. Check the current "
            "NKY Health instructions before submitting forms or scheduling an inspection.</p>"
        )
        marker = "<h2>Official sources</h2>"
        if marker not in text:
            raise RuntimeError("Campbell County official-sources marker is missing")
        text = text.replace(marker, section + marker, 1)

    text = _add_source(
        text,
        NKY_LOCATIONS,
        "Northern Kentucky Health Department — locations and Campbell County Health Center",
        "Campbell",
    )
    text = _add_source(
        text,
        NKY_REQUESTS,
        "Northern Kentucky Health Department — public records and onsite-septic records requests",
        "Campbell",
    )
    text = _refresh_review_date(text)
    page.write_text(text, encoding="utf-8")

    if heading not in text or NKY_LOCATIONS not in text or NKY_REQUESTS not in text:
        raise RuntimeError("Campbell County quality enhancement failed")


if __name__ == "__main__":
    enhance_boone()
    enhance_campbell()
    print("Kentucky Northern Kentucky quality pass complete: Boone and Campbell local guidance refreshed")
