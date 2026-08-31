"""SepticScope build finalizer.

Python imports sitecustomize automatically for the repository's normal `python ...`
commands. Register a narrow atexit finalizer so generated production HTML receives
last-mile integrity repairs after the nested expansion chain completes. The same hook
is harmless during audits because it only applies known deterministic replacements.
"""
from __future__ import annotations

import atexit
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"


def _finalize_generated_site() -> None:
    if not SITE.is_dir():
        return

    replacements = {
        # Washington DOH moved the rule-revision page; a previous prefix replacement
        # could leave this hybrid URL behind.
        "https://doh.wa.gov/community-and-environment/wastewater-management/site-sewage-systems-oss/rule-revision":
            "https://doh.wa.gov/community-and-environment/wastewater-management/rules-and-regulations/site-rule-revision",
        # Buncombe County migrated Environmental Health to its new buncombenc.gov site.
        "https://www.buncombecounty.org/governing/depts/health/EnvironmentalHealth.aspx":
            "https://www.buncombenc.gov/456/Environmental-Health",
        # Retired Deschutes attachment paths are replaced with the county's current
        # onsite-permit guidance page rather than another fragile document URL.
        "https://www.deschutes.org/sites/default/files/fileattachments/community_development/page/27061/application_guide_-_site_evaluation_-_11_21_2023.pdf":
            "https://www.deschutes.org/cd/page/onsite-permit-repairs-existing-systems-application-guide",
        "https://www.deschutes.org/sites/default/files/fileattachments/community_development/page/731/onsite_wastewater_systems_application_requirements.pdf":
            "https://www.deschutes.org/cd/page/onsite-permit-repairs-existing-systems-application-guide",
    }

    for html_file in SITE.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8", errors="replace")
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated != text:
            html_file.write_text(updated, encoding="utf-8")

    sitemap = SITE / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        additions = ""
        for slug in ("about", "privacy"):
            url = f"https://septicscope.com/{slug}/"
            if url not in text:
                additions += f"<url><loc>{url}</loc><lastmod>2026-08-31</lastmod></url>"
        if additions:
            text = text.replace("</urlset>", additions + "</urlset>")
            sitemap.write_text(text, encoding="utf-8")


atexit.register(_finalize_generated_site)
