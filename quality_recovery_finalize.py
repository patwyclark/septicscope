#!/usr/bin/env python3
"""Finalize quality-recovery content and retire legacy indexable routes."""
from __future__ import annotations

from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
ADSENSE_CLIENT = "ca-pub-8782868222380999"

FAQ_ADDITION = '''<section class="sources" data-quality-recovery-addition="faq-use"><h2>How to use these answers for a real property</h2><p>A general answer should help you identify the next question, not substitute for the property file. Before calling an agency or professional, collect the legal property address, parcel number, owner name, building or bedroom information, known system type, alarm or symptom details, recent water use, inspection and pumping history, and any permit or as-built drawing you already have. A clear starting package makes it easier to determine whether the issue is plumbing, routine maintenance, an electrical or pump problem, a permit question, or a condition that needs onsite evaluation.</p><p>Describe what you can actually observe: which fixtures are affected, whether the problem is indoors or outdoors, when it began, whether heavy rain or freezing conditions occurred, whether an alarm is active, and whether sewage is present. Avoid opening electrical controls, entering tanks, or probing buried components when you do not know their location or condition. Keep children and pets away from wastewater and reduce water use when backup or surfacing sewage is possible.</p><h2>Why the local answer can differ</h2><p>Septic programs are administered by states, tribes, local governments, health districts, and delegated agencies. The required permit, inspection type, professional credential, setback, design flow, operating permit, maintenance contract, transfer rule, repair approval, or record-request process can therefore change by location and system type. Start with the legal county and then confirm whether another municipality, district, or state office has authority for the parcel.</p><p>When an answer affects a purchase, sale, bedroom addition, new structure, well, pool, driveway, repair, or replacement, obtain written property-specific information before relying on a general rule. SepticScope links the public sources used and provides a correction path, but the current agency instruction, approved design, and qualified onsite evaluation control the final decision.</p></section>'''

ABOUT_ADDITION = '''<section data-quality-recovery-addition="accountability"><h2>Quality review and release accountability</h2><p>A technically valid page is not automatically a useful page. Our release checks separately evaluate indexability, canonical URLs, internal links, external sources, advertising placement, source visibility, main-content depth, local evidence, and similarity to other location pages. A page can pass basic HTML validation and still be withheld when it does not offer enough original value for a homeowner making a real decision.</p><p>County publication is reversible. When a guide loses a source, becomes too similar to a statewide template, or lacks enough locally actionable detail, it can be removed from the sitemap, marked noindex, made ad-free, and routed back to a broader navigation page until the research is repaired. This is preferable to preserving a large page count that gives readers and search engines the wrong impression of coverage.</p><h2>What we will publish next</h2><p>Future additions should close a specific information gap: a local permit sequence, office and contact path, record-request process, inspection stage, current fee source, transfer requirement, operating or maintenance obligation, system-specific rule, or a substantive homeowner decision guide. We do not publish a page merely because a keyword exists or an automation schedule elapsed. Every new indexable page should have a clear audience, distinct purpose, supporting sources, useful next steps, and a reason to exist apart from a changed location name.</p><p>Site health is measured by useful search visibility, successful task completion, source accuracy, reader trust, and sustainable monetization—not by the number of generated URLs. That standard applies even when it means shrinking the public footprint before rebuilding it carefully.</p></section>'''


def visible_word_count(raw: str) -> int:
    main = raw.split("<main", 1)[-1].split("</main>", 1)[0]
    main = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", main, flags=re.I | re.S)
    main = re.sub(r"<[^>]+>", " ", main)
    return len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", main))


def append_before_main_close(path: Path, fragment: str, marker: str) -> None:
    if not path.exists():
        raise RuntimeError(f"Missing generated recovery page: {path}")
    raw = path.read_text(encoding="utf-8", errors="replace")
    if marker not in raw:
        if "</main>" not in raw:
            raise RuntimeError(f"Generated page lacks </main>: {path}")
        raw = raw.replace("</main>", fragment + "</main>", 1)
        path.write_text(raw, encoding="utf-8")


def noindex_and_remove_ads(path: Path) -> None:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if re.search(r'<meta\s+[^>]*name=["\']robots["\'][^>]*>', raw, flags=re.I):
        raw = re.sub(
            r'<meta\s+[^>]*name=["\']robots["\'][^>]*>',
            '<meta name="robots" content="noindex,follow">',
            raw,
            count=1,
            flags=re.I,
        )
    else:
        raw = re.sub(r"</head>", '<meta name="robots" content="noindex,follow"></head>', raw, count=1, flags=re.I)
    if "septicscope-quality-status" not in raw:
        raw = re.sub(r"</head>", '<meta name="septicscope-quality-status" content="retired-legacy-route"></head>', raw, count=1, flags=re.I)
    raw = re.sub(
        r'<script\b[^>]*src=["\'][^"\']*pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^"\']*["\'][^>]*>\s*</script>',
        "",
        raw,
        flags=re.I | re.S,
    )
    raw = re.sub(r'<ins\b[^>]*class=["\'][^"\']*adsbygoogle[^"\']*["\'][^>]*>.*?</ins>', "", raw, flags=re.I | re.S)
    raw = re.sub(r'<script\b[^>]*>[^<]{0,500}adsbygoogle\.push\([^<]{0,500}</script>', "", raw, flags=re.I | re.S)
    path.write_text(raw, encoding="utf-8")


def retire_legacy_indiana() -> int:
    legacy = SITE / "indiana"
    if not legacy.is_dir():
        return 0
    redirects: list[str] = []
    count = 0
    for path in sorted(legacy.rglob("index.html")):
        noindex_and_remove_ads(path)
        rel = path.relative_to(SITE).as_posix()
        source = "/" if rel == "index.html" else "/" + rel.removesuffix("index.html")
        if source == "/indiana/":
            target = "/counties/indiana/"
        else:
            leaf = path.parent.name
            county_leaf = re.sub(r"-county$", "", leaf)
            candidate = SITE / "counties" / "indiana" / county_leaf / "index.html"
            target = f"/counties/indiana/{county_leaf}/" if candidate.exists() else "/counties/indiana/"
        redirects.append(f"{source} {target} 301")
        count += 1

    redirects_path = SITE / "_redirects"
    existing = redirects_path.read_text(encoding="utf-8", errors="replace") if redirects_path.exists() else ""
    existing = re.sub(r"(?s)\n?# BEGIN RETIRED LEGACY INDIANA.*?# END RETIRED LEGACY INDIANA\n?", "\n", existing)
    block = "# BEGIN RETIRED LEGACY INDIANA\n" + "\n".join(redirects) + "\n# END RETIRED LEGACY INDIANA"
    redirects_path.write_text(existing.rstrip() + "\n\n" + block + "\n", encoding="utf-8")
    return count


def main() -> None:
    faq = SITE / "faq" / "index.html"
    about = SITE / "about" / "index.html"
    append_before_main_close(faq, FAQ_ADDITION, 'data-quality-recovery-addition="faq-use"')
    append_before_main_close(about, ABOUT_ADDITION, 'data-quality-recovery-addition="accountability"')
    retired = retire_legacy_indiana()

    faq_raw = faq.read_text(encoding="utf-8", errors="replace")
    about_raw = about.read_text(encoding="utf-8", errors="replace")
    faq_words = visible_word_count(faq_raw)
    about_words = visible_word_count(about_raw)
    if faq_words < 1100 or '"@type": "FAQPage"' not in faq_raw:
        raise RuntimeError(f"Expanded FAQ quality check failed: {faq_words} words")
    if about_words < 800 or "How automation is used" not in about_raw or "Advertising and commercial separation" not in about_raw:
        raise RuntimeError(f"Expanded About quality check failed: {about_words} words")
    for path in (faq,):
        if ADSENSE_CLIENT not in path.read_text(encoding="utf-8", errors="replace"):
            raise RuntimeError("Substantive FAQ hub lost AdSense site code")
    if ADSENSE_CLIENT in about_raw:
        raise RuntimeError("Editorial transparency page must remain ad-free")
    print(f"Quality recovery finalized: FAQ={faq_words} words; About={about_words} words; retired legacy Indiana routes={retired}")


if __name__ == "__main__":
    main()
