"""County-specific Green River quality improvements backed by current GRDHD sources."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "site"
GRDHD_WEBSTER = "https://healthdepartment.org/location/webster-county-health-center/"
GRDHD_UNION = "https://healthdepartment.org/location/union-county-health-center/"


def enhance_webster() -> None:
    page = OUTPUT / "counties" / "kentucky" / "webster" / "index.html"
    if not page.exists():
        raise RuntimeError("Expected verified Webster County page is missing")

    text = page.read_text(encoding="utf-8")
    heading = "Webster County local septic starting point"
    if heading not in text:
        section = (
            "<h2>Webster County local septic starting point</h2>"
            "<p>Green River District Health Department directs onsite-sewage applicants to apply "
            "in person at their county health center for the required site evaluation and to "
            "contact the Environmentalist at the local health center for project questions. For "
            "Webster County, GRDHD lists the Webster County Health Center at 80 Clayton Avenue, "
            "Dixon, KY 42409, phone 270-639-9315. Its current location page publishes weekday "
            "hours of 8:00 a.m. to noon and 1:00 p.m. to 4:30 p.m., Monday through Friday. "
            "Because the office closes at noon, confirm current Environmental Health availability "
            "and any county-specific plat, survey, or floor-plan requirements before making a "
            "trip or submitting plans.</p>"
        )
        marker = "<h2>Official sources</h2>"
        if marker not in text:
            raise RuntimeError("Webster County official-sources marker is missing")
        text = text.replace(marker, section + marker, 1)

    source = (
        f'<li><a href="{GRDHD_WEBSTER}" rel="nofollow">'
        "Green River District Health Department — Webster County Health Center"
        "</a></li>"
    )
    sources_marker = "<h2>Official sources</h2><ul>"
    if GRDHD_WEBSTER not in text:
        if sources_marker not in text:
            raise RuntimeError("Webster County official-source list is missing")
        text = text.replace(sources_marker, sources_marker + source, 1)

    text = re.sub(
        r"Official sources checked [^<]+",
        "Official sources checked September 8, 2026",
        text,
        count=1,
    )
    page.write_text(text, encoding="utf-8")

    if heading not in text or GRDHD_WEBSTER not in text:
        raise RuntimeError("Webster County quality enhancement failed")


def enhance_union() -> None:
    page = OUTPUT / "counties" / "kentucky" / "union" / "index.html"
    if not page.exists():
        raise RuntimeError("Expected verified Union County page is missing")

    text = page.read_text(encoding="utf-8")
    heading = "Union County local septic starting point"
    if heading not in text:
        section = (
            "<h2>Union County local septic starting point</h2>"
            "<p>Green River District Health Department says the first step for a property without "
            "municipal sewer is a site evaluation and directs applicants to apply in person at "
            "their county health center. For Union County, GRDHD lists the Union County Health "
            "Center at 218 W. McElroy Street, Morganfield, KY 42437, phone 270-389-1230, with "
            "published hours of 8:00 a.m. to 4:30 p.m. Monday through Friday. Bring the location "
            "map and site drawing described in the district's onsite-sewage guidance, and confirm "
            "current Environmental Health availability plus any county-specific plat, survey, or "
            "floor-plan requirements before making a trip or submitting plans.</p>"
        )
        marker = "<h2>Official sources</h2>"
        if marker not in text:
            raise RuntimeError("Union County official-sources marker is missing")
        text = text.replace(marker, section + marker, 1)

    source = (
        f'<li><a href="{GRDHD_UNION}" rel="nofollow">'
        "Green River District Health Department — Union County Health Center"
        "</a></li>"
    )
    sources_marker = "<h2>Official sources</h2><ul>"
    if GRDHD_UNION not in text:
        if sources_marker not in text:
            raise RuntimeError("Union County official-source list is missing")
        text = text.replace(sources_marker, sources_marker + source, 1)

    text = re.sub(
        r"Official sources checked [^<]+",
        "Official sources checked September 8, 2026",
        text,
        count=1,
    )
    page.write_text(text, encoding="utf-8")

    if heading not in text or GRDHD_UNION not in text:
        raise RuntimeError("Union County quality enhancement failed")


if __name__ == "__main__":
    enhance_webster()
    enhance_union()
    print("Kentucky Green River quality pass complete: Webster and Union local guidance refreshed")
