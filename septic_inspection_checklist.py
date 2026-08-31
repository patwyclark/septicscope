"""Generate an EPA-grounded septic inspection checklist after the site build."""
from __future__ import annotations

import atexit
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
GA_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"


def _write_guide() -> None:
    if not SITE.is_dir():
        return
    out = SITE / "guides" / "septic-inspection-checklist"
    out.mkdir(parents=True, exist_ok=True)
    canonical = "https://septicscope.com/guides/septic-inspection-checklist/"
    epa_malfunction = "https://www.epa.gov/septic/resolving-septic-system-malfunctions"
    epa_faq = "https://www.epa.gov/septic/frequent-questions-septic-systems"
    epa_buyer = "https://www.epa.gov/septic/new-homebuyers-brochure-and-guide-septic-systems"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Septic Inspection Checklist: What a Good Inspection Should Cover | SepticScope</title>
<meta name="description" content="Use this septic inspection checklist before a home purchase or routine inspection. See records, tanks, sludge, filters, pumps, drainfield checks and questions to ask.">
<link rel="canonical" href="{canonical}">
<style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:1000px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}main{{padding-top:42px;padding-bottom:70px}}.crumb{{font-size:.92rem;color:var(--muted)}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}}h2{{margin-top:1.9em}}a{{color:var(--accent)}}.card,.note{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}.checks{{list-style:none;padding-left:0}}.checks li{{margin:.7rem 0;padding-left:1.8rem;position:relative}}.checks li:before{{content:'□';position:absolute;left:0;font-size:1.2rem}}table{{width:100%;border-collapse:collapse;margin:18px 0}}th,td{{text-align:left;border-bottom:1px solid var(--line);padding:10px;vertical-align:top}}footer{{border-top:1px solid var(--line);color:var(--muted)}}@media print{{header,footer{{display:none}}main{{padding:0;max-width:none}}.card,.note{{break-inside:avoid}}}}@media(max-width:700px){{table{{display:block;overflow-x:auto}}}}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"Septic Inspection Checklist: What a Good Inspection Should Cover","description":"A practical septic inspection checklist grounded in current EPA guidance.","mainEntityOfPage":"{canonical}","publisher":{{"@type":"Organization","name":"SepticScope"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"What should a septic inspection include?","acceptedAnswer":{{"@type":"Answer","text":"EPA describes a typical inspection as including review of permits and maintenance records, opening and inspecting tanks, measuring sludge and scum, checking an effluent filter if present, and evaluating applicable system components. Exact scope varies by system and local rules."}}}},{{"@type":"Question","name":"Should I get a septic inspection before buying a house?","acceptedAnswer":{{"@type":"Answer","text":"EPA recommends having the septic system inspected before purchasing a home. Local transfer, lender, or contract requirements may specify who can inspect it and what the report must include."}}}},{{"@type":"Question","name":"Is pumping the same as a septic inspection?","acceptedAnswer":{{"@type":"Answer","text":"No. Pumping removes accumulated solids. An inspection evaluates records, tank condition and levels, accessible components and system performance as applicable. Ask exactly what is included in the quoted service."}}}}]}}</script>
</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / Septic inspection checklist</div>
<h1>Septic inspection checklist: what should actually be checked?</h1>
<p>A septic inspection is more useful when you know the scope before the appointment. EPA's current guidance describes a typical inspection as more than a surface walk: it can include records review, opening tanks, measuring sludge and scum, checking the effluent filter when present, and evaluating system components. The exact inspection required for a home sale or permit is set locally.</p>
<div class="note"><strong>Buying a home?</strong> EPA recommends a septic inspection before purchase. Do not assume a general home inspection includes a full septic evaluation, and do not assume a recent pump receipt proves the drainfield or mechanical components are functioning.</div>
<h2>Before you hire an inspector</h2><ul class="checks"><li>Ask the local permitting authority whether a property-transfer inspection is required and whether the inspector needs a specific license or credential.</li><li>Get the septic permit, approved design or as-built drawing if available.</li><li>Collect pumping, repair, inspection and service-contract records.</li><li>Identify the system type: conventional gravity, pressure distribution, aerobic treatment, mound or another design can require different checks.</li><li>Ask for a written scope and price. Confirm whether locating lids, excavation, pumping, camera work or laboratory testing costs extra.</li></ul>
<h2>Records and system identification</h2><div class="card"><ul class="checks"><li>Permit/design records reviewed, including installation date and approved capacity where available.</li><li>Maintenance and pumping history reviewed.</li><li>Tank, pump tank, distribution components and drainfield locations compared with the approved plan where practical.</li><li>Unpermitted additions, bedroom changes or obvious structures over the system flagged for local verification.</li></ul></div>
<h2>Tank and accessible component checks</h2><p>EPA says a typical inspection includes opening and inspecting tanks and evaluating sludge and scum levels. What can safely and legally be inspected depends on the system and access.</p><ul class="checks"><li>Septic tank and other applicable tank access points opened by the professional.</li><li>Liquid level and visible evidence of leakage, deterioration or abnormal conditions documented.</li><li>Sludge and scum levels measured and pumping need evaluated.</li><li>Accessible inlet/outlet components and baffles or tees evaluated as applicable.</li><li>Effluent filter checked if installed.</li><li>Pumps, floats, alarms and control components checked when the system uses them and the inspection scope calls for it.</li></ul>
<h2>Drainfield and site checks</h2><ul class="checks"><li>Drainfield area checked for surfacing wastewater, persistent wetness, sewage odor or unusually lush/spongy growth.</li><li>Evidence of vehicle traffic, structures, grading changes or stormwater directed over the field noted.</li><li>System response or flow evaluated using the method appropriate to the jurisdiction and system type.</li><li>Any observed malfunction symptoms clearly separated from assumptions about the cause.</li></ul>
<h2>What the report should tell you</h2><table><thead><tr><th>Question</th><th>Why it matters</th></tr></thead><tbody><tr><td>What system and components were inspected?</td><td>Prevents a vague “passed” statement from hiding an incomplete scope.</td></tr><tr><td>What could not be accessed or tested?</td><td>Shows where uncertainty remains before a purchase or repair decision.</td></tr><tr><td>Were sludge/scum levels measured?</td><td>Separates measured maintenance need from a calendar-only recommendation.</td></tr><tr><td>Were malfunction symptoms observed?</td><td>Helps distinguish maintenance from a problem needing diagnosis.</td></tr><tr><td>What repairs or follow-up tests are recommended?</td><td>Lets you verify permits, obtain comparable quotes and negotiate from a written finding.</td></tr></tbody></table>
<h2>Inspection vs. pumping</h2><p>Pumping and inspection overlap, but they are not interchangeable. Pumping removes solids; inspection evaluates condition and function within the agreed scope. If a seller provides only a pumping receipt, ask what was inspected and whether a written report exists. For ongoing ownership, use the <a href="/guides/septic-maintenance-checklist/">septic maintenance checklist</a> to keep the records together.</p>
<h2>If the inspection finds a problem</h2><p>Do not jump directly from a symptom to full system replacement. Ask which component appears affected, what evidence supports the finding, whether additional diagnosis is needed, and what the local permitting authority requires. For wetness, odors or suspected soil-treatment problems, see the <a href="/guides/septic-drainfield-repair-replacement/">drainfield repair vs. replacement guide</a>. For system-specific questions, review the <a href="/guides/types-of-septic-systems/">types of septic systems guide</a>.</p>
<h2>Verify the local rule before closing</h2><p>Real-estate transfer requirements vary substantially. Some jurisdictions prescribe inspection forms, timing or inspector qualifications; others do not. Use the <a href="/counties/">SepticScope county directory</a> to find the relevant permitting authority and verify the rule for the property.</p>
<h2>Official sources</h2><ul><li><a rel="nofollow" href="{epa_malfunction}">U.S. EPA — Resolving Septic System Malfunctions</a></li><li><a rel="nofollow" href="{epa_faq}">U.S. EPA — Frequent Questions on Septic Systems</a></li><li><a rel="nofollow" href="{epa_buyer}">U.S. EPA — New Homebuyer's Brochure and Guide to Septic Systems</a></li></ul>
<p><em>SepticScope provides general information, not an inspection or engineering opinion. Local law, permit conditions, transaction documents and qualified professionals control when more specific.</em></p>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    (out / "index.html").write_text(page, encoding="utf-8")
    hub = SITE / "guides" / "index.html"
    if hub.exists():
        text = hub.read_text(encoding="utf-8", errors="replace")
        if "/guides/septic-inspection-checklist/" not in text:
            promo = '<section><h2>Septic inspection checklist</h2><p>Buying a home or scheduling routine service? Use the <a href="/guides/septic-inspection-checklist/">septic inspection checklist</a> to compare scope, records, tank checks, drainfield observations and follow-up questions.</p></section>'
            text = text.replace("</main>", promo + "</main>", 1) if "</main>" in text else text.replace("</body>", promo + "</body>", 1)
            hub.write_text(text, encoding="utf-8")
    sitemap = SITE / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        if canonical not in text:
            text = text.replace("</urlset>", f"<url><loc>{canonical}</loc><lastmod>2026-08-31</lastmod></url></urlset>")
            sitemap.write_text(text, encoding="utf-8")


atexit.register(_write_guide)
