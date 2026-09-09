#!/usr/bin/env python3
"""Apply a quality-first publication filter before AdSense review.

The county lookup remains nationally complete, but a dedicated county URL is published
only when the final page is source-verified. Navigation and utility screens remain
ad-free. Editorial pages receive transparent publisher notes and only substantive
long-form pages carry the AdSense site code while the site is under review.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date
from html import escape
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
MANIFEST = SITE / "data" / "national-coverage-manifest.json"
STATUS_FILE = SITE / "data" / "adsense-readiness.json"
DOMAIN = "https://septicscope.com"
GA_MEASUREMENT_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"
TODAY = date.today().isoformat()
EPA_STATE_CONTACTS = "https://www.epa.gov/septic/state-septic-system-program-contacts"
USA_LOCAL_GOV = "https://www.usa.gov/state-local-governments"

ADSENSE_TAG = (
    '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?'
    f'client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>'
)
ADSENSE_SCRIPT_RE = re.compile(
    r'<script\b[^>]*pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^>]*>\s*</script>',
    flags=re.I,
)
ADSENSE_UNIT_RE = re.compile(
    r'<ins\b[^>]*class=["\'][^"\']*adsbygoogle[^"\']*["\'][^>]*>.*?</ins>',
    flags=re.I | re.S,
)
ADSENSE_PUSH_RE = re.compile(
    r'<script\b[^>]*>\s*\(adsbygoogle\s*=\s*window\.adsbygoogle\s*\|\|\s*\[\]\)\.push\([^)]*\);?\s*</script>',
    flags=re.I | re.S,
)
EDITORIAL_MARKER = 'data-septicscope-editorial-note="1"'
EDITORIAL_STYLE_MARKER = 'data-septicscope-editorial-style="1"'

EDITORIAL_STYLE = r'''
.ss-editorial-note{border:1px solid #dce3e8;border-radius:13px;background:#f7fafb;padding:13px 15px;margin:18px 0 25px;color:#5b6672;font-size:.9rem}.ss-editorial-note strong{color:#17212b}.ss-editorial-note a{font-weight:750}.ss-editorial-note__meta{display:block;margin-top:4px}
'''

STATE_STYLE = r'''
:root{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b;--soft:#eaf5f1}*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}a{color:var(--accent)}header,footer{border-color:var(--line);border-style:solid;border-width:0 0 1px}.nav,main,.footer-inner{max-width:1080px;margin:auto;padding:20px 24px}.nav{display:flex;align-items:center;justify-content:space-between;gap:16px}.brand{font-weight:900;color:var(--ink);text-decoration:none}.nav-links{display:flex;gap:15px;flex-wrap:wrap}.nav-links a{text-decoration:none;font-weight:750}main{padding-top:42px;padding-bottom:70px}.crumb{font-size:.9rem;color:var(--muted)}h1{font-size:clamp(2.1rem,5vw,3.7rem);line-height:1.06;letter-spacing:-.03em}h2{margin-top:1.9em}.lede{font-size:1.12rem;color:#43515b;max-width:790px}.note{border:1px solid var(--line);border-radius:14px;background:var(--soft);padding:17px;margin:24px 0}.guide-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px}.guide-card{display:block;border:1px solid var(--line);border-radius:14px;background:#fff;padding:16px;text-decoration:none;color:var(--ink)}.guide-card strong{display:block;color:var(--accent)}.guide-card span{display:block;color:var(--muted);font-size:.88rem;margin-top:5px}.fips-tools{display:flex;gap:10px;align-items:center;margin:18px 0}.fips-tools input{width:100%;padding:12px 13px;border:1px solid #bcc9ce;border-radius:10px;font:inherit}.fips-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px 15px;list-style:none;padding:0}.fips-grid li{border-bottom:1px solid #edf0f2;padding:8px 0}.fips-grid small{display:block;color:var(--muted)}footer{border-width:1px 0 0;color:var(--muted)}@media(max-width:780px){.guide-grid,.fips-grid{grid-template-columns:1fr 1fr}}@media(max-width:540px){.guide-grid,.fips-grid{grid-template-columns:1fr}.nav{display:block}.nav-links{margin-top:10px}}
'''

ABOUT_STYLE = r'''
:root{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b;--soft:#eaf5f1;--warm:#fff8ed}*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.72}a{color:var(--accent)}header,footer{border-color:var(--line);border-style:solid;border-width:0 0 1px}.nav,main,.footer-inner{max-width:940px;margin:auto;padding:20px 24px}.nav{display:flex;align-items:center;justify-content:space-between;gap:16px}.brand{font-weight:900;color:var(--ink);text-decoration:none}.nav-links{display:flex;gap:15px;flex-wrap:wrap}.nav-links a{text-decoration:none;font-weight:750}main{padding-top:44px;padding-bottom:74px}.crumb{font-size:.9rem;color:var(--muted)}h1{font-size:clamp(2.25rem,5vw,4rem);line-height:1.05;letter-spacing:-.035em}h2{font-size:clamp(1.45rem,3vw,2rem);line-height:1.2;margin-top:2em}.lede{font-size:1.15rem;color:#43515b}.panel{border:1px solid var(--line);border-radius:16px;padding:20px;margin:27px 0;background:var(--panel)}.panel.soft{background:var(--soft)}.panel.warm{background:var(--warm)}.standards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.standard{border:1px solid var(--line);border-radius:14px;padding:17px;background:#fff}.standard h3{margin:0 0 8px}.standard p{margin:0;color:var(--muted)}.source-table{border-collapse:collapse;width:100%;margin:22px 0}.source-table th,.source-table td{border:1px solid var(--line);padding:12px;text-align:left;vertical-align:top}.source-table th{background:var(--panel)}footer{border-width:1px 0 0;color:var(--muted)}@media(max-width:700px){.standards{grid-template-columns:1fr}.nav{display:block}.nav-links{margin-top:10px}.source-table{display:block;overflow-x:auto}}
'''


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def load_records() -> list[dict]:
    if not MANIFEST.exists():
        raise RuntimeError("Run site_inventory.py before the AdSense publication filter")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = [row for row in data.get("records", []) if isinstance(row, dict)]
    if len(records) != 3144 or len({clean(row.get("fips")) for row in records}) != 3144:
        raise RuntimeError("AdSense recovery requires 3,144 unique county lookup records")
    return records


def local_path_for_url(url: str) -> Path:
    if not url.startswith(DOMAIN + "/"):
        raise RuntimeError(f"Unexpected SepticScope URL: {url}")
    relative = url.removeprefix(DOMAIN).strip("/")
    return SITE / relative / "index.html"


def strip_adsense(text: str) -> str:
    text = ADSENSE_SCRIPT_RE.sub("", text)
    text = ADSENSE_UNIT_RE.sub("", text)
    text = ADSENSE_PUSH_RE.sub("", text)
    return text


def visible_text(text: str) -> str:
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return clean(text)


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", visible_text(text)))


def prune_unverified_county_pages(records: list[dict]) -> tuple[int, int]:
    expected_verified: set[Path] = set()
    for record in records:
        if record.get("verification_status") == "verified":
            expected_verified.add(local_path_for_url(clean(record.get("page_url"))))

    removed = 0
    county_root = SITE / "counties"
    for path in list(county_root.glob("*/*/index.html")):
        if path in expected_verified:
            continue
        path.unlink()
        removed += 1
        parent = path.parent
        try:
            parent.rmdir()
        except OSError:
            pass

    missing_verified = [path for path in expected_verified if not path.exists()]
    if missing_verified:
        raise RuntimeError(
            "The publication filter would leave verified county pages missing: "
            + ", ".join(str(path.relative_to(SITE)) for path in missing_verified[:10])
        )
    return removed, len(expected_verified)


def write_state_hubs(records: list[dict]) -> tuple[int, int]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        grouped[clean(record.get("state"))].append(record)

    written = 0
    removed = 0
    for state, rows in sorted(grouped.items()):
        state_slug = slugify(state)
        out = SITE / "counties" / state_slug / "index.html"
        verified = [
            row for row in rows
            if row.get("verification_status") == "verified"
            and local_path_for_url(clean(row.get("page_url"))).exists()
        ]
        if not verified:
            if out.exists():
                out.unlink()
                removed += 1
            continue

        verified.sort(key=lambda row: clean(row.get("county_or_equivalent_name")))
        rows.sort(key=lambda row: clean(row.get("county_or_equivalent_name")))
        guide_cards = []
        for row in verified:
            name = clean(row.get("county_or_equivalent_name"))
            fips = clean(row.get("fips"))
            authority = clean(row.get("official_regulating_authority"))
            reviewed = clean(row.get("date_last_reviewed"))
            details = [f"County FIPS {fips}"]
            if authority:
                details.append(authority)
            if reviewed:
                details.append(f"sources reviewed {reviewed}")
            guide_cards.append(
                f'<a class="guide-card" href="{escape(clean(row.get("page_url")).removeprefix(DOMAIN))}">'
                f'<strong>{escape(name)}</strong><span>{escape(" · ".join(details))}</span></a>'
            )

        fips_items = []
        verified_fips = {clean(row.get("fips")) for row in verified}
        for row in rows:
            name = clean(row.get("county_or_equivalent_name"))
            fips = clean(row.get("fips"))
            if fips in verified_fips:
                label = (
                    f'<a href="{escape(clean(row.get("page_url")).removeprefix(DOMAIN))}">'
                    f'{escape(name)}</a>'
                )
                status = "published source-verified guide"
            else:
                label = f'<span>{escape(name)}</span>'
                status = "county-code reference"
            fips_items.append(
                f'<li data-fips-search="{escape((name + " " + fips).lower())}">{label}'
                f'<small>FIPS {escape(fips)} · {status}</small></li>'
            )

        canonical = f"{DOMAIN}/counties/{state_slug}/"
        state_gov = f"https://www.usa.gov/states/{state_slug}"
        page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(state)} Septic Guides and County FIPS Codes | SepticScope</title><meta name="description" content="Browse published source-verified septic guides and county FIPS codes for {escape(state)}. Use official state and EPA starting points where a local guide is not published."><link rel="canonical" href="{canonical}"><style>{STATE_STYLE}</style><script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}');</script></head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a><nav class="nav-links" aria-label="Primary"><a href="/counties/">County lookup</a><a href="/guides/">Guides</a><a href="/faq/">FAQs</a><a href="/about/">Research standards</a></nav></div></header><main><p class="crumb"><a href="/">Home</a> / <a href="/counties/">County lookup</a> / {escape(state)}</p><h1>{escape(state)} septic guides and county FIPS codes</h1><p class="lede">This page is a reference for {len(rows):,} {escape(state)} counties and county-equivalents. SepticScope links a dedicated county guide only when the page contains a source-supported permitting authority, visible official sources and an editorial review date.</p><div class="note"><strong>{len(verified):,} published county guide{'s' if len(verified) != 1 else ''}.</strong> A county name without a link remains available as a FIPS reference in the lookup instead of opening a filler or construction page. For a property without a published guide, confirm the legal county and start with the official <a href="{state_gov}" rel="nofollow noopener">{escape(state)} government directory</a> or the <a href="{EPA_STATE_CONTACTS}" rel="nofollow noopener">EPA state septic program contacts</a>.</div><h2>Published source-verified county guides</h2><div class="guide-grid">{''.join(guide_cards)}</div><h2>All {escape(state)} county and county-equivalent codes</h2><p>The five-digit county FIPS code combines the two-digit state code and three-digit county or county-equivalent code. Codes identify geography; they do not identify the septic regulator or prove which permit rules apply to a parcel.</p><div class="fips-tools"><label for="fips-filter" style="position:absolute;left:-9999px">Filter county codes</label><input id="fips-filter" type="search" placeholder="Filter by county name or FIPS code" autocomplete="off"></div><ul class="fips-grid">{''.join(fips_items)}</ul><h2>Official starting points</h2><ul><li><a href="{state_gov}" rel="nofollow noopener">{escape(state)} government directory on USA.gov</a></li><li><a href="{EPA_STATE_CONTACTS}" rel="nofollow noopener">EPA state septic system program contacts</a></li><li><a href="{USA_LOCAL_GOV}" rel="nofollow noopener">USA.gov state and local government directory</a></li></ul><p><em>County codes and directory links are starting points. The agency serving the property and its current instructions control.</em></p></main><footer><div class="footer-inner">© 2026 SepticScope · <a href="/about/">About our research</a> · <a href="/privacy/">Privacy</a> · <a href="/contact/">Corrections &amp; feedback</a></div></footer><script>(function(){{const q=document.getElementById('fips-filter');if(!q)return;q.addEventListener('input',()=>{{const v=q.value.toLowerCase().trim();document.querySelectorAll('[data-fips-search]').forEach(row=>{{row.hidden=v&&!row.dataset.fipsSearch.includes(v)}})}})}})();</script></body></html>'''
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        written += 1
    return written, removed


def write_about() -> None:
    out = SITE / "about"
    out.mkdir(parents=True, exist_ok=True)
    canonical = f"{DOMAIN}/about/"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>About SepticScope and Our Editorial Standards</title><meta name="description" content="Learn who publishes SepticScope, how county septic information is sourced, what source-verified means, how automation is used, and how to report corrections."><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:title" content="About SepticScope and Our Editorial Standards"><meta property="og:description" content="A transparent explanation of SepticScope sourcing, publication, automation, corrections and advertising standards."><meta property="og:url" content="{canonical}"><style>{ABOUT_STYLE}</style><script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}');</script><script type="application/ld+json">{{"@context":"https://schema.org","@type":"AboutPage","name":"About SepticScope and Our Editorial Standards","url":"{canonical}","publisher":{{"@type":"Organization","name":"SepticScope","url":"{DOMAIN}/","email":"feedback@septicscope.com"}},"dateModified":"{TODAY}"}}</script></head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a><nav class="nav-links" aria-label="Primary"><a href="/counties/">County lookup</a><a href="/guides/">Guides</a><a href="/faq/">FAQs</a><a href="/contact/">Contact</a></nav></div></header><main><p class="crumb"><a href="/">Home</a> / About</p><h1>About SepticScope and our editorial standards</h1><p class="lede">SepticScope is an independent U.S. informational publisher focused on septic permits, onsite-wastewater agencies, county geography and practical homeowner decisions. It is not a government agency, contractor referral service, engineering firm or substitute for the authority serving a property.</p><div class="panel soft"><strong>Editorial responsibility</strong><p>Site content is published and maintained by the <strong>SepticScope Editorial Desk</strong>. Questions, corrections and source updates can be sent through the <a href="/contact/">public feedback route</a> or to <a href="mailto:feedback@septicscope.com">feedback@septicscope.com</a>. The correction path is displayed throughout the site because agency assignments, forms, fees and web addresses can change.</p></div>

<h2>Why SepticScope exists</h2><p>Septic information is unusually fragmented. One property may be regulated by a county environmental-health office, another by a regional health district, another by a city, and another directly by a state program. A mailing city or ZIP code may cross a county line. The office that holds an older installation drawing may be different from the office that issues a current repair permit. Homeowners are often forced to search several government sites before they can even determine which question to ask.</p><p>SepticScope organizes that process around the property’s legal county or county-equivalent. The national lookup includes all 3,144 federal county and county-equivalent codes so a visitor can identify the geography even when a dedicated SepticScope guide has not been published. A local page is linked only when the final page contains enough source-supported information to be useful on its own. Counties without a published guide remain lookup records with direct official starting points; they do not receive location-name-swapped filler pages.</p>

<h2>What “source-verified county guide” means</h2><p>A county guide is treated as source-verified only when the final published page is indexable and contains a named permitting authority, a visible official-sources section and a source-review date. The page must explain the local or state process supported by those sources. Mere page existence, a business directory listing, a search-result snippet or a nearby city is not enough.</p><p>Verification describes the evidence used for the page; it is not a guarantee that every fact will remain current forever. Government departments reorganize, links move and rules change. For that reason, county pages identify the source and date used and remind readers that the agency’s current instructions control.</p><div class="standards"><article class="standard"><h3>Authority before advice</h3><p>We first identify the office or program that appears to control onsite wastewater for the location. General homeowner advice is kept separate from local permit claims.</p></article><article class="standard"><h3>Sources shown to readers</h3><p>Important local claims should be traceable to visible government, public-health, code, university-extension or other recognized public sources.</p></article><article class="standard"><h3>Jurisdiction labels stay narrow</h3><p>Statewide rules are not described as county-created rules. Regional and municipal responsibilities are identified when the evidence supports them.</p></article><article class="standard"><h3>No fabricated certainty</h3><p>When a source does not answer a question, the page tells the reader what to confirm rather than inventing a fee, setback, permit duration or credential rule.</p></article></div>

<h2>Source hierarchy</h2><table class="source-table"><thead><tr><th>Source type</th><th>How it is used</th><th>Typical examples</th></tr></thead><tbody><tr><td>Controlling government source</td><td>Primary support for permit authority, forms, regulations, inspections and official contacts.</td><td>County code, health department, state environmental agency, delegated local program.</td></tr><tr><td>Recognized public institution</td><td>Explanations and homeowner education when the institution has relevant expertise.</td><td>Cooperative Extension, public university, public health district.</td></tr><tr><td>Company-owned provider source</td><td>Business identity, public phone, stated services and stated service area.</td><td>Provider website or an official licensing directory.</td></tr><tr><td>Discovery-only source</td><td>Used to find a possible source, never as the final evidence for a local claim.</td><td>Search-result snippet, aggregator, copied directory or unsourced summary.</td></tr></tbody></table><p>External links are checked automatically when practical, but government websites sometimes block automated requests or respond inconsistently. A blocked automated check is not treated as proof that a source is invalid. Editorial status depends on the source content and the final page, not only on a link-check response.</p>

<h2>How automation and AI are used</h2><p>SepticScope uses software automation to organize public county identifiers, generate navigation, monitor internal links, test canonical URLs, detect missing metadata, check whether cited links still respond, and maintain repeatable publication gates. Automated tools may also help structure research notes or draft a page framework from source material.</p><p>Automation is not treated as an authority. It may not infer a permit rule from a nearby county, turn a search snippet into evidence, invent a service area, or mark a county verified merely because a page was generated. A county page reaches the source-verified category only when its final output contains the required authority, sources and review information. The build also removes unpublished county placeholders rather than exposing thousands of construction pages to visitors or advertising systems.</p><p>Some regulatory language necessarily repeats when a state program administers the same process across many counties. We still look for the local office, local contact, delegated responsibility, county-specific form or other location-specific evidence that makes a county page useful. Repeated-content checks are part of the site audit, and high-similarity groups are reviewed as an editorial risk rather than celebrated as scale.</p>

<h2>What the county lookup does—and does not do</h2><p>The lookup can match a county name, state, five-digit county FIPS code, ZIP code or city-and-state query. ZIP and city searches use public geographic services to resolve representative coordinates to one or more possible counties. Because postal geography does not always match parcel geography, the result always asks the visitor to confirm the legal county in the property record.</p><p>A verified result links to a SepticScope county guide. An unverified result displays the county name and FIPS code with official state and EPA starting points directly in the results. It does not open an empty local page. The lookup is a routing tool; it does not determine property boundaries, issue permits or establish which system can be approved on a particular site.</p>

<h2>Provider and commercial-content standards</h2><p>Provider information is kept separate from regulatory guidance. A business may be included only when a company-owned source or official directory supports the identity, public contact information, septic or onsite-wastewater service and geographic relationship shown. Ordinary listings are not endorsements or rankings. SepticScope does not copy star ratings, manufacture reviews or infer countywide coverage from a nearby address.</p><p>The national service finder is withheld until every county and county-equivalent has a source-reviewed provider relationship. This prevents a visitor from entering a ZIP code and receiving an empty result presented as a complete directory. Sponsorship, affiliate relationships or paid placement must be disclosed and must not change the factual publication standard.</p>

<h2>Advertising and editorial independence</h2><p>Advertising may support the cost of hosting, source monitoring and ongoing research. Ads do not determine which county is marked verified, which business is listed, or what a guide says. During AdSense review, Google ad code is limited to the homepage and substantive long-form guide pages. County lookup, state indexes, policy pages, contact pages, unpublished locations and other navigation or utility screens remain ad-free.</p><p>Ad placement is reviewed separately from content. A page should still be useful when advertising is unavailable. SepticScope does not ask users to click ads, disguise navigation as advertising or place ads on screens whose main purpose is an alert, lookup action or unfinished notice.</p>

<h2>Corrections, updates and limitations</h2><p>Readers can report a broken source, changed agency assignment, incorrect contact, missing local form or other factual problem through the <a href="/contact/">Contact &amp; Feedback page</a>. Useful reports include the SepticScope URL, the statement that appears wrong and the current official source. Corrections are evaluated against the best available source and may result in a page update, a narrower statement or temporary withdrawal of a local guide.</p><p>SepticScope provides planning information, not legal, engineering, environmental-health or contractor advice. Soil conditions, setbacks, lot layout, water supply, design flow, system type, prior approvals and project scope can change what an agency requires. Current instructions from the authority serving the property, licensed professionals and qualified field inspection control real-world decisions.</p><div class="panel warm"><strong>Last editorial standards update: {TODAY}</strong><p>This page is updated when the publication process, advertising implementation, privacy practices or correction standards materially change.</p></div><p>For general questions, source corrections or business-record corrections, use <a href="/contact/">Contact &amp; Feedback</a>.</p></main><footer><div class="footer-inner">© 2026 SepticScope · <a href="/counties/">County lookup</a> · <a href="/guides/">Guides</a> · <a href="/privacy/">Privacy</a> · <a href="/contact/">Corrections &amp; feedback</a></div></footer></body></html>'''
    (out / "index.html").write_text(page, encoding="utf-8")


def write_privacy() -> None:
    out = SITE / "privacy"
    out.mkdir(parents=True, exist_ok=True)
    canonical = f"{DOMAIN}/privacy/"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Privacy Policy | SepticScope</title><meta name="description" content="SepticScope privacy policy for analytics, AdSense, cookies, optional location lookup, feedback submissions and external links."><link rel="canonical" href="{canonical}"><style>{ABOUT_STYLE}</style></head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a><nav class="nav-links" aria-label="Primary"><a href="/counties/">County lookup</a><a href="/guides/">Guides</a><a href="/about/">About</a><a href="/contact/">Contact</a></nav></div></header><main><p class="crumb"><a href="/">Home</a> / Privacy</p><h1>Privacy Policy</h1><p class="lede">Last updated {TODAY}</p><h2>Overview</h2><p>SepticScope is an informational website for septic-system permitting, county lookup and homeowner education. This policy explains information that may be processed when the site is used.</p><h2>Analytics</h2><p>SepticScope uses Google Analytics to understand aggregate usage such as pages viewed, approximate traffic source, device or browser information and interaction patterns. Google Analytics may use cookies or similar identifiers. This information is used to improve navigation, detect broken pages and understand which resources are useful.</p><h2>Advertising and Google AdSense</h2><p>SepticScope uses Google AdSense on selected substantive pages. Third-party vendors, including Google, use cookies to serve ads based on a user’s prior visits to this website or other websites. Google’s advertising cookies enable Google and its partners to serve ads based on visits to SepticScope and other sites on the Internet.</p><p>Users may opt out of personalized advertising through <a href="https://adssettings.google.com/" rel="nofollow noopener">Google Ads Settings</a>. Information about how Google uses data from partner sites is available at <a href="https://policies.google.com/technologies/partner-sites" rel="nofollow noopener">How Google uses information from sites or apps that use its services</a>.</p><h2>Optional location lookup</h2><p>The “Use my current location” button is optional and is activated only by the visitor. The browser asks for permission before providing coordinates. When permission is granted, the page sends the coordinates over an encrypted connection to public FCC or U.S. Census geography services to identify a likely county FIPS code. SepticScope does not store the coordinates in its own database. The third-party public service receives the request under its own privacy practices. Visitors can instead enter a ZIP code, city and state, county and state, or FIPS code without granting location access.</p><h2>Feedback and email</h2><p>If a visitor contacts SepticScope, the information voluntarily provided may include a name, reply email, page URL and message. It is used to respond, evaluate corrections and improve the site. Do not send passwords, financial account details, medical information or other sensitive personal information.</p><h2>External links</h2><p>County guides link to government, public-health, environmental, university and provider websites. SepticScope does not control those sites. Their privacy policies and cookie practices apply after a visitor follows the link.</p><h2>Children</h2><p>SepticScope is a general property-information resource and is not directed to children under 13.</p><h2>Policy changes and contact</h2><p>This policy may change when site features, analytics, advertising providers or legal requirements change. Privacy questions and correction requests can be sent through <a href="/contact/">Contact &amp; Feedback</a> or emailed to <a href="mailto:feedback@septicscope.com">feedback@septicscope.com</a>.</p></main><footer><div class="footer-inner">© 2026 SepticScope · <a href="/about/">About</a> · <a href="/contact/">Contact &amp; Feedback</a></div></footer></body></html>'''
    (out / "index.html").write_text(page, encoding="utf-8")


def normalize_public_copy(text: str) -> str:
    text = re.sub(
        r'<a\b[^>]*href=["\']/counties/indiana/?["\'][^>]*>.*?Indiana(?: septic)? rules.*?</a>',
        '<a href="/counties/">County lookup</a>',
        text,
        flags=re.I | re.S,
    )
    replacements = {
        "county and county-equivalent pages": "county and county-equivalent lookup records",
        "Search all 3,144 county pages": "Search all 3,144 county records",
        "Browse every county": "Browse the county lookup",
        "Verified and in-progress pages are labeled": "Published guides and lookup-only results are clearly separated",
        "Source-checked local guides are separated from official-help pages still under research.": "Source-checked local guides are linked; other results show county codes and official starting points without opening filler pages.",
        "Every state hub distinguishes source-checked guides from in-progress official-help pages.": "State hubs link only to source-checked county guides and retain county FIPS references for the rest.",
        "unfinished county research remains clearly labeled": "counties without source-supported guides remain lookup records instead of filler pages",
        "Verified guides and in-progress official-help pages are not presented as equivalent.": "Published guides and lookup-only county records are not presented as equivalent.",
        "Unfinished county pages remain noindex until local authority, process, and sources are supportable.": "Only source-supported county guides receive published local pages.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def editorial_note(path: Path, text: str) -> str:
    text = re.sub(
        r'<aside\b[^>]*data-septicscope-editorial-note=["\']1["\'][^>]*>.*?</aside>',
        "",
        text,
        flags=re.I | re.S,
    )
    parts = path.relative_to(SITE).parts
    is_county = len(parts) == 4 and parts[0] == "counties" and parts[-1] == "index.html"
    is_guide = len(parts) == 3 and parts[0] == "guides" and parts[-1] == "index.html"
    is_faq = len(parts) == 3 and parts[0] == "faq" and parts[-1] == "index.html"
    if not (is_county or is_guide or is_faq) or "noindex" in text.lower():
        return text
    if is_county and not ("Official sources" in text and "Permitting authority" in text):
        return text

    review = ""
    match = re.search(r"Official sources checked\s+([^<\n]+)", text, flags=re.I)
    if match:
        review = clean(match.group(1)).strip(" .")
    detail = f" Sources checked {escape(review)}." if review else ""
    note = (
        f'<aside {EDITORIAL_MARKER} class="ss-editorial-note"><strong>Published by the SepticScope Editorial Desk.</strong>'
        f'<span class="ss-editorial-note__meta">{detail} <a href="/about/">Editorial and source standards</a> · '
        '<a href="/contact/">Report a correction</a></span></aside>'
    )
    if EDITORIAL_STYLE_MARKER not in text:
        style = f'<style {EDITORIAL_STYLE_MARKER}>{EDITORIAL_STYLE}</style>'
        text = re.sub(r"</head>", style + "</head>", text, count=1, flags=re.I)
    return re.sub(r"</h1>", "</h1>" + note, text, count=1, flags=re.I)


def is_monetizable(path: Path, text: str) -> bool:
    if "noindex" in text.lower():
        return False
    parts = path.relative_to(SITE).parts
    if parts == ("index.html",):
        return word_count(text) >= 500
    if len(parts) == 3 and parts[0] == "guides" and parts[-1] == "index.html":
        return word_count(text) >= 500
    return False


def finalize_html() -> tuple[int, int, int]:
    monetized = 0
    ad_free = 0
    editorial = 0
    for path in sorted(SITE.rglob("*.html")):
        text = path.read_text(encoding="utf-8", errors="replace")
        text = strip_adsense(text)
        text = normalize_public_copy(text)
        before_note = text
        text = editorial_note(path, text)
        if EDITORIAL_MARKER in text and EDITORIAL_MARKER not in before_note:
            editorial += 1
        if is_monetizable(path, text):
            if "</head>" not in text:
                raise RuntimeError(f"Monetizable page lacks </head>: {path}")
            text = re.sub(r"</head>", ADSENSE_TAG + "</head>", text, count=1, flags=re.I)
            monetized += 1
        else:
            ad_free += 1
        path.write_text(text, encoding="utf-8")
    return monetized, ad_free, editorial


def page_url(path: Path) -> str:
    rel = path.relative_to(SITE).as_posix()
    if rel == "index.html":
        return DOMAIN + "/"
    if rel.endswith("/index.html"):
        return DOMAIN + "/" + rel[:-10]
    return DOMAIN + "/" + rel


def rebuild_sitemap() -> int:
    urls = []
    for path in sorted(SITE.rglob("*.html")):
        if path.name == "404.html":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "noindex" in text.lower():
            continue
        url = page_url(path)
        if url in {DOMAIN + "/providers/", DOMAIN + "/septic-services-near-me/"}:
            continue
        urls.append(url)
    urls = sorted(set(urls))
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    root = ET.Element(f"{{{ns}}}urlset")
    for url in urls:
        node = ET.SubElement(root, f"{{{ns}}}url")
        ET.SubElement(node, f"{{{ns}}}loc").text = url
        ET.SubElement(node, f"{{{ns}}}lastmod").text = TODAY
    ET.ElementTree(root).write(SITE / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    return len(urls)


def write_status(
    records: list[dict],
    *,
    removed_placeholders: int,
    state_hubs: int,
    monetized_pages: int,
    ad_free_pages: int,
    editorial_notes: int,
    sitemap_urls: int,
) -> None:
    published_counties = len(list((SITE / "counties").glob("*/*/index.html")))
    payload = {
        "schema_version": 1,
        "generated_at": TODAY,
        "recovery_reason": "Google AdSense low value content",
        "publication_policy": "All 3,144 county-equivalents remain searchable, but only source-verified county guides receive dedicated public pages.",
        "county_lookup_records": len(records),
        "published_source_verified_county_guides": published_counties,
        "lookup_only_counties": len(records) - published_counties,
        "placeholder_county_pages": 0,
        "placeholder_pages_removed_this_pass": removed_placeholders,
        "published_state_hubs": state_hubs,
        "monetized_substantive_pages": monetized_pages,
        "ad_free_pages": ad_free_pages,
        "editorial_notes": editorial_notes,
        "sitemap_urls": sitemap_urls,
        "adsense_scope": "Homepage and long-form guide articles with at least 500 visible words; navigation, lookup, policy, contact, state, county, FAQ and unpublished-location screens are ad-free.",
    }
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATUS_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def assert_recovery(records: list[dict]) -> None:
    verified_urls = {
        clean(row.get("page_url"))
        for row in records
        if row.get("verification_status") == "verified"
    }
    leaf_pages = list((SITE / "counties").glob("*/*/index.html"))
    actual_urls = {page_url(path) for path in leaf_pages}
    if actual_urls != verified_urls:
        missing = sorted(verified_urls - actual_urls)
        extra = sorted(actual_urls - verified_urls)
        raise RuntimeError(
            f"County publication filter mismatch; missing={missing[:8]}, extra={extra[:8]}"
        )

    exempt = {
        SITE / "providers" / "index.html",
        SITE / "septic-services-near-me" / "index.html",
    }
    forbidden = (
        "local guide in progress",
        "while we finish this local guide",
        "all 3,144 county pages",
        "official-help pages still under research",
    )
    for path in SITE.rglob("*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        if path not in exempt:
            found = [phrase for phrase in forbidden if phrase in lower]
            if found:
                raise RuntimeError(f"Public construction/filler language remains in {path}: {found}")
        has_ads = ADSENSE_CLIENT in text or "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" in text
        if has_ads and not is_monetizable(path, text):
            raise RuntimeError(f"AdSense code remains on a non-substantive or utility page: {path}")

    about = (SITE / "about" / "index.html").read_text(encoding="utf-8", errors="replace")
    if word_count(about) < 900:
        raise RuntimeError("About/editorial standards page is too thin")
    for phrase in ("SepticScope Editorial Desk", "How automation and AI are used", "Advertising and editorial independence", "Corrections, updates and limitations"):
        if phrase not in about:
            raise RuntimeError(f"About page is missing trust disclosure: {phrase}")

    privacy = (SITE / "privacy" / "index.html").read_text(encoding="utf-8", errors="replace")
    if "Optional location lookup" not in privacy or "does not store the coordinates" not in privacy:
        raise RuntimeError("Privacy policy does not disclose the optional geolocation lookup")


def main() -> None:
    if not SITE.is_dir():
        raise RuntimeError("site/ is missing; run the production build first")
    records = load_records()
    removed_placeholders, verified_count = prune_unverified_county_pages(records)
    state_hubs, removed_hubs = write_state_hubs(records)
    write_about()
    write_privacy()
    monetized, ad_free, editorial = finalize_html()
    sitemap_urls = rebuild_sitemap()
    write_status(
        records,
        removed_placeholders=removed_placeholders,
        state_hubs=state_hubs,
        monetized_pages=monetized,
        ad_free_pages=ad_free,
        editorial_notes=editorial,
        sitemap_urls=sitemap_urls,
    )
    assert_recovery(records)
    print(
        "AdSense recovery complete: "
        f"removed {removed_placeholders:,} placeholder county pages and {removed_hubs} empty state hubs; "
        f"kept {verified_count:,} source-verified county guides and {len(records):,} lookup records; "
        f"AdSense limited to {monetized} substantive pages"
    )


if __name__ == "__main__":
    main()
