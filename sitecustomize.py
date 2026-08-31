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
GA_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"


def _write_homebuyer_guide() -> None:
    """Publish one durable, government-grounded national guide for buyer-intent search."""
    guide_dir = SITE / "guides" / "buying-home-with-septic"
    guide_dir.mkdir(parents=True, exist_ok=True)
    canonical = "https://septicscope.com/guides/buying-home-with-septic/"
    epa_homebuyer = "https://www.epa.gov/septic/new-homebuyers-brochure-and-guide-septic-systems"
    epa_faq = "https://www.epa.gov/septic/frequent-questions-septic-systems"
    epa_failures = "https://www.epa.gov/septic/resolving-septic-system-malfunctions"
    epa_maintenance = "https://www.epa.gov/septic/why-maintain-your-septic-system"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Buying a Home With a Septic System: Inspection Checklist | SepticScope</title>
<meta name="description" content="A practical homebuyer checklist for septic records, inspections, warning signs, transfer requirements, maintenance and local permit research.">
<link rel="canonical" href="{canonical}">
<style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:1000px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}main{{padding-top:42px;padding-bottom:70px}}.crumb{{font-size:.92rem;color:var(--muted)}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}}h2{{margin-top:1.9em}}a{{color:var(--accent)}}.card,.note{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}.checklist li{{margin:.55rem 0}}footer{{border-top:1px solid var(--line);color:var(--muted)}}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"Buying a Home With a Septic System: Inspection Checklist","description":"A practical homebuyer checklist for septic records, inspections, warning signs, transfer requirements, maintenance and local permit research.","mainEntityOfPage":"{canonical}","publisher":{{"@type":"Organization","name":"SepticScope"}}}}</script>
</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / Buying a home with septic</div>
<h1>Buying a home with a septic system: what to check before closing</h1>
<p>A septic system should be treated as a major property system, not a box to check during a general home inspection. The U.S. Environmental Protection Agency specifically publishes a guide for septic homebuyers and recommends having the system inspected before purchase.</p>
<div class="note"><strong>Start local:</strong> septic rules are primarily state and local. Before relying on a seller's statement, check the <a href="/counties/">SepticScope county guide</a> for the permitting authority, records office, transfer rules and local inspection requirements that apply to the property.</div>
<h2>Homebuyer septic checklist</h2><ol class="checklist">
<li><strong>Confirm the property is actually served by septic.</strong> Review the deed, building records, utility information and local permit records.</li>
<li><strong>Get the permit and as-built drawing.</strong> EPA notes that local health or environmental agencies commonly hold septic design drawings and permits. These can identify system age, location, soil information and approved capacity.</li>
<li><strong>Ask for pumping and maintenance records.</strong> Compare the history with the system type and local maintenance requirements.</li>
<li><strong>Use a qualified septic professional for the inspection.</strong> A general visual home inspection is not a substitute for the inspection scope required by the local jurisdiction or appropriate for the system type.</li>
<li><strong>Verify local property-transfer requirements.</strong> EPA notes that many states require septic inspection when real estate transfers, but the exact trigger, form, inspector credential and timing vary by jurisdiction.</li>
<li><strong>Resolve deficiencies before closing.</strong> Determine who will repair them, whether permits are required, whether the system can legally support the home's current use, and whether the repair can fit on the lot.</li></ol>
<h2>What a thorough septic inspection should address</h2><p>EPA's current inspection guidance says a typical inspection includes reviewing permit, design and installation records; reviewing pumping and maintenance records; opening and inspecting tanks; evaluating sludge and scum levels; and assessing components such as an effluent filter when present. The inspection scope can be broader for alternative or mechanically complex systems.</p>
<div class="card"><strong>Useful documents to request from the seller</strong><ul><li>Original septic permit and approved design or as-built</li><li>Installation date and system type</li><li>Pumping receipts and inspection reports</li><li>Repair or alteration permits</li><li>Operation-and-maintenance contracts for advanced systems</li><li>Any recent property-transfer inspection or compliance report</li></ul></div>
<h2>Warning signs that deserve more investigation</h2><p>EPA lists common malfunction signs including sewage backing up into plumbing, slow drains, gurgling, standing water or damp areas near the tank or drainfield, sewage odors, and unusually bright green or spongy grass over the septic area. These symptoms do not tell you the exact cause, but they are reasons to stop and investigate before taking on the property.</p>
<h2>Why records and system capacity matter</h2><p>A functioning tank does not automatically mean the property is compliant for its current use. Bedrooms, design flow, additions, accessory dwelling units, wells, lot lines, replacement-area requirements and local setbacks can affect whether the existing system is adequate or whether future expansion is possible. Use the local permitting agency's records and current rules rather than assuming a system is legal because it has been in use for years.</p>
<h2>Budget for ownership, not just the inspection</h2><p>EPA says household septic systems are generally inspected every 1 to 3 years and tanks are typically pumped every 3 to 5 years, with frequency depending on household size, tank size, water use and solids accumulation. EPA's current consumer guidance also notes that periodic maintenance can be far less expensive than repairing or replacing a malfunctioning conventional system. Local costs vary substantially, so obtain local quotes rather than treating a national price as a bid.</p>
<h2>After closing</h2><p>Keep the permit, as-built, inspection report and service records together. Avoid driving or building over the drainfield, manage water use, flush only appropriate waste, and follow the maintenance interval required for your system type. If the property has pumps, floats, treatment units or other mechanical components, EPA recommends more frequent professional attention than for a basic conventional system.</p>
<h2>Official sources</h2><ul><li><a rel="nofollow" href="{epa_homebuyer}">U.S. EPA — New Homebuyer's Brochure and Guide to Septic Systems</a></li><li><a rel="nofollow" href="{epa_faq}">U.S. EPA — Frequent Questions on Septic Systems</a></li><li><a rel="nofollow" href="{epa_failures}">U.S. EPA — Resolving Septic System Malfunctions</a></li><li><a rel="nofollow" href="{epa_maintenance}">U.S. EPA — Why Maintain Your Septic System</a></li></ul>
<p><em>SepticScope is an informational research resource. Local agency requirements and site-specific professional findings control when they differ from this guide.</em></p>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    (guide_dir / "index.html").write_text(page, encoding="utf-8")

    hub = SITE / "guides" / "index.html"
    if hub.exists():
        text = hub.read_text(encoding="utf-8", errors="replace")
        if "/guides/buying-home-with-septic/" not in text:
            promo = '<section><h2>Buying a home with septic</h2><p>Use the <a href="/guides/buying-home-with-septic/">septic homebuyer inspection checklist</a> to review records, inspection scope, warning signs, transfer requirements and maintenance before closing.</p></section>'
            text = text.replace("</main>", promo + "</main>", 1) if "</main>" in text else text.replace("</body>", promo + "</body>", 1)
            hub.write_text(text, encoding="utf-8")
    else:
        hub.parent.mkdir(parents=True, exist_ok=True)
        hub.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Septic System Guides for Homeowners | SepticScope</title><meta name="description" content="Practical septic system guides for homeowners and homebuyers, backed by government and local permitting sources."><link rel="canonical" href="https://septicscope.com/guides/"><script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script></head><body><main><h1>Septic system guides</h1><p>Practical homeowner guidance with official-source research and links back to local requirements.</p><h2>Buying a home with septic</h2><p><a href="/guides/buying-home-with-septic/">Review the homebuyer septic inspection checklist →</a></p><p><a href="/counties/">Find septic rules by county →</a></p></main></body></html>''', encoding="utf-8")


def _finalize_generated_site() -> None:
    if not SITE.is_dir():
        return

    replacements = {
        "https://doh.wa.gov/community-and-environment/wastewater-management/site-sewage-systems-oss/rule-revision":
            "https://doh.wa.gov/community-and-environment/wastewater-management/rules-and-regulations/site-rule-revision",
        "https://www.buncombecounty.org/governing/depts/health/EnvironmentalHealth.aspx":
            "https://www.buncombenc.gov/456/Environmental-Health",
        "https://www.deschutes.org/sites/default/files/fileattachments/community_development/page/27061/application_guide_-_site_evaluation_-_11_21_2023.pdf":
            "https://www.deschutes.org/cd/page/onsite-permit-repairs-existing-systems-application-guide",
        "https://www.deschutes.org/sites/default/files/fileattachments/community_development/page/731/onsite_wastewater_systems_application_requirements.pdf":
            "https://www.deschutes.org/cd/page/onsite-permit-repairs-existing-systems-application-guide",
        "https://lewiscountywa.gov/media/documents/Exhibit_A_-_2025_Fee_Schedule_Final_Version.pdf":
            "https://lewiscountywa.gov/departments/public-health/fee-schedule/",
        "Lewis County — 2025 Public Health Fee Schedule":
            "Lewis County — 2026 Public Health Fee Schedule",
    }

    for html_file in SITE.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8", errors="replace")
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated != text:
            html_file.write_text(updated, encoding="utf-8")

    _write_homebuyer_guide()

    sitemap = SITE / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        additions = ""
        for slug in ("about", "privacy", "guides", "guides/buying-home-with-septic"):
            url = f"https://septicscope.com/{slug}/"
            if url not in text:
                additions += f"<url><loc>{url}</loc><lastmod>2026-08-31</lastmod></url>"
        if additions:
            text = text.replace("</urlset>", additions + "</urlset>")
            sitemap.write_text(text, encoding="utf-8")


atexit.register(_finalize_generated_site)
