"""County-specific Northern Kentucky quality improvements backed by current NKY Health sources."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "site"
NKY_LOCATIONS = "https://nkyhealth.org/ourlocations/"
NKY_REQUESTS = "https://nkyhealth.org/requests/"


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

    sources_marker = "<h2>Official sources</h2><ul>"
    additions = (
        (
            NKY_LOCATIONS,
            "Northern Kentucky Health Department — locations and Boone County Health Center",
        ),
        (
            NKY_REQUESTS,
            "Northern Kentucky Health Department — public records and onsite-septic records requests",
        ),
    )
    for url, label in additions:
        if url not in text:
            if sources_marker not in text:
                raise RuntimeError("Boone County official-source list is missing")
            source = f'<li><a href="{url}" rel="nofollow">{label}</a></li>'
            text = text.replace(sources_marker, sources_marker + source, 1)

    text = re.sub(
        r"Official sources checked [^<]+",
        "Official sources checked September 8, 2026",
        text,
        count=1,
    )
    page.write_text(text, encoding="utf-8")

    if heading not in text or NKY_LOCATIONS not in text or NKY_REQUESTS not in text:
        raise RuntimeError("Boone County quality enhancement failed")


if __name__ == "__main__":
    enhance_boone()
    print("Kentucky Northern Kentucky quality pass complete: Boone local guidance refreshed")
