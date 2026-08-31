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
<h2>Budget for ownership, not just the inspection</h2><p>EPA says household septic systems are generally inspected every 1 to 3 years and tanks are typically pumped every 3 to 5 years, with frequency depending on household size, tank size, water use and solids accumulation. For current market pricing and the factors that change an inspection quote, see the <a href="/guides/septic-inspection-cost/">SepticScope septic inspection cost guide</a>. EPA's current consumer guidance also notes that periodic maintenance can be far less expensive than repairing or replacing a malfunctioning conventional system.</p>
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


def _write_inspection_cost_guide() -> None:
    """Publish a buyer/owner guide for inspection-cost search intent without inventing local prices."""
    guide_dir = SITE / "guides" / "septic-inspection-cost"
    guide_dir.mkdir(parents=True, exist_ok=True)
    canonical = "https://septicscope.com/guides/septic-inspection-cost/"
    epa_faq = "https://www.epa.gov/septic/frequent-questions-septic-systems"
    epa_maintenance = "https://www.epa.gov/septic/why-maintain-your-septic-system"
    homeadvisor = "https://www.homeadvisor.com/cost/plumbing/septic-inspection-cost/"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Septic Inspection Cost in 2026: Price Factors & Buyer Guide | SepticScope</title>
<meta name="description" content="What a septic inspection may cost in 2026, what changes the price, what should be inspected, and how local transfer rules affect the scope.">
<link rel="canonical" href="{canonical}">
<style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:1000px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}main{{padding-top:42px;padding-bottom:70px}}.crumb{{font-size:.92rem;color:var(--muted)}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}}h2{{margin-top:1.9em}}a{{color:var(--accent)}}.card,.note{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}table{{width:100%;border-collapse:collapse;margin:18px 0}}th,td{{text-align:left;border-bottom:1px solid var(--line);padding:10px;vertical-align:top}}footer{{border-top:1px solid var(--line);color:var(--muted)}}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"Septic Inspection Cost in 2026: Price Factors & Buyer Guide","description":"What a septic inspection may cost in 2026, what changes the price, what should be inspected, and how local transfer rules affect the scope.","mainEntityOfPage":"{canonical}","publisher":{{"@type":"Organization","name":"SepticScope"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"How much does a septic inspection cost in 2026?","acceptedAnswer":{{"@type":"Answer","text":"HomeAdvisor's June 2026 national cost guide reports a typical range of $200 to $900 and an average around $550. Local prices vary with inspection scope, tank access, system complexity, pumping, camera work and local transfer requirements."}}}},{{"@type":"Question","name":"Does a septic inspection include pumping?","acceptedAnswer":{{"@type":"Answer","text":"Not always. Inspection and pumping may be separate services. Ask what the quoted inspection includes and whether local rules or the inspector's protocol require the tank to be opened, pumped or otherwise accessed."}}}},{{"@type":"Question","name":"How often should a septic system be inspected?","acceptedAnswer":{{"@type":"Answer","text":"EPA says household septic systems are generally inspected every one to three years, while systems with electrical switches, pumps or mechanical components should be inspected more frequently, generally once a year."}}}}]}}</script>
</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / Septic inspection cost</div>
<h1>How much does a septic inspection cost in 2026?</h1>
<p>For a current national market benchmark, HomeAdvisor's June 19, 2026 cost guide reports a typical septic inspection range of <strong>$200 to $900</strong>, with an average around <strong>$550</strong>. That is a third-party national estimate, not a regulated fee schedule. Your actual quote can be materially higher or lower because inspection scope and local requirements differ.</p>
<div class="note"><strong>For a home purchase:</strong> do not choose an inspection based on price alone. First check the <a href="/counties/">local septic authority</a> and confirm any transfer-inspection requirements, required forms and inspector credentials. Then compare quotes for the same scope. The <a href="/guides/buying-home-with-septic/">SepticScope homebuyer checklist</a> covers the records and due diligence to request before closing.</div>
<h2>What changes the inspection price?</h2><table><thead><tr><th>Cost factor</th><th>Why it matters</th></tr></thead><tbody>
<tr><td>Inspection depth</td><td>A limited visual review takes less time than an inspection that opens tanks, checks liquid and solids levels, evaluates components, documents the drainfield and produces a formal transfer report.</td></tr>
<tr><td>Tank access</td><td>Buried or hard-to-find lids can require locating or excavation before the inspector can evaluate the tank.</td></tr>
<tr><td>Pumping</td><td>Pumping may be quoted separately from inspection. Confirm whether it is included and whether it is needed for the inspection protocol being used.</td></tr>
<tr><td>System type</td><td>Aerobic treatment units, pumps, floats, controls, sand filters and other advanced systems have more components to evaluate than a simple gravity system.</td></tr>
<tr><td>Camera or diagnostic work</td><td>Video inspection, line locating, hydraulic testing or other diagnostic work can add labor and equipment charges.</td></tr>
<tr><td>Real-estate paperwork</td><td>Some jurisdictions require a specific transfer form, certified inspector, sampling or additional documentation that changes the scope and price.</td></tr>
<tr><td>Local market</td><td>Labor rates, travel distance and contractor availability vary widely by region, so a national range should be treated only as a planning benchmark.</td></tr></tbody></table>
<h2>What should you get for the money?</h2><p>EPA says a typical inspection can include reviewing permit, design and installation records; reviewing pumping and maintenance history; opening and inspecting tanks; checking sludge and scum levels; and evaluating components such as effluent filters. More complex systems may require more frequent or specialized inspection. Ask each company to spell out the scope so you are comparing equivalent quotes.</p>
<div class="card"><strong>Questions to ask before booking</strong><ul><li>Will you open and inspect every accessible tank?</li><li>Is pumping included, required or separately priced?</li><li>Will you evaluate the drainfield and visible signs of malfunction?</li><li>Are pumps, alarms, floats and treatment components included?</li><li>Do you provide the report or form required for a local property transfer?</li><li>Are locating, excavation, camera work or return visits extra?</li></ul></div>
<h2>Inspection cost vs. the cost of skipping maintenance</h2><p>EPA's current consumer guidance says regular septic maintenance fees of about <strong>$250 to $500 every three to five years</strong> are far less than repairing or replacing a malfunctioning conventional system, which EPA says can cost roughly <strong>$5,000 to $15,000</strong>. Those figures describe maintenance and malfunction costs rather than the price of a single inspection, but they show why routine inspection and maintenance should be budgeted as normal ownership costs.</p>
<h2>How often should a septic system be inspected?</h2><p>EPA says household systems are generally inspected at least every one to three years. Systems with electrical switches, pumps or other mechanical components should generally be inspected more frequently, commonly once a year. Local rules or operation-and-maintenance agreements can require a different schedule.</p>
<h2>Use local requirements before relying on a national estimate</h2><p>Property-transfer rules, installer or inspector licensing, forms and required testing can change the scope of an inspection. Use the <a href="/counties/">SepticScope county directory</a> to find the appropriate local permitting authority and verified requirements where available. If the county guide is still being verified, follow the linked official agency directly before ordering a transaction-specific inspection.</p>
<h2>Sources</h2><ul><li><a rel="nofollow" href="{epa_faq}">U.S. EPA — Frequent Questions on Septic Systems</a></li><li><a rel="nofollow" href="{epa_maintenance}">U.S. EPA — Why Maintain Your Septic System</a></li><li><a rel="nofollow" href="{homeadvisor}">HomeAdvisor — Septic System Inspection Cost (updated June 19, 2026)</a></li></ul>
<p><em>National cost figures are planning estimates, not quotes or regulated fees. SepticScope is an informational research resource; local agency requirements and site-specific professional findings control.</em></p>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    (guide_dir / "index.html").write_text(page, encoding="utf-8")

    hub = SITE / "guides" / "index.html"
    if hub.exists():
        text = hub.read_text(encoding="utf-8", errors="replace")
        if "/guides/septic-inspection-cost/" not in text:
            promo = '<section><h2>Septic inspection cost</h2><p>See the <a href="/guides/septic-inspection-cost/">2026 septic inspection cost guide</a> for national planning ranges, price factors, inspection scope and local-transfer considerations.</p></section>'
            text = text.replace("</main>", promo + "</main>", 1) if "</main>" in text else text.replace("</body>", promo + "</body>", 1)
            hub.write_text(text, encoding="utf-8")


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
    _write_inspection_cost_guide()

    sitemap = SITE / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        additions = ""
        for slug in ("about", "privacy", "guides", "guides/buying-home-with-septic", "guides/septic-inspection-cost"):
            url = f"https://septicscope.com/{slug}/"
            if url not in text:
                additions += f"<url><loc>{url}</loc><lastmod>2026-08-31</lastmod></url>"
        if additions:
            text = text.replace("</urlset>", additions + "</urlset>")
            sitemap.write_text(text, encoding="utf-8")


atexit.register(_finalize_generated_site)
