"""Generate an EPA-grounded septic maintenance checklist after the site build."""
from __future__ import annotations

import atexit
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
GA_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"


def _write_maintenance_checklist() -> None:
    if not SITE.is_dir():
        return

    out = SITE / "guides" / "septic-maintenance-checklist"
    out.mkdir(parents=True, exist_ok=True)
    canonical = "https://septicscope.com/guides/septic-maintenance-checklist/"
    epa_care = "https://www.epa.gov/septic/how-care-your-septic-system"
    epa_tools = "https://www.epa.gov/septic/tools-about-septic-systems-homeowners"
    epa_faq = "https://www.epa.gov/septic/frequent-questions-septic-systems"
    epa_top10 = "https://www.epa.gov/septic/top-10-ways-be-good-septic-owner"

    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Septic Maintenance Checklist: Monthly, Yearly & Pumping Tasks | SepticScope</title>
<meta name="description" content="A practical septic maintenance checklist for homeowners: records, inspections, pumping, water use, drainfield protection, alarms and warning signs, grounded in current EPA guidance.">
<link rel="canonical" href="{canonical}">
<style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:1000px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}main{{padding-top:42px;padding-bottom:70px}}.crumb{{font-size:.92rem;color:var(--muted)}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}}h2{{margin-top:1.9em}}a{{color:var(--accent)}}.card,.note{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}.checks{{list-style:none;padding-left:0}}.checks li{{margin:.7rem 0;padding-left:1.8rem;position:relative}}.checks li:before{{content:'□';position:absolute;left:0;font-size:1.2rem}}table{{width:100%;border-collapse:collapse;margin:18px 0}}th,td{{text-align:left;border-bottom:1px solid var(--line);padding:10px;vertical-align:top}}footer{{border-top:1px solid var(--line);color:var(--muted)}}@media print{{header,footer{{display:none}}main{{padding:0;max-width:none}}.card,.note{{break-inside:avoid}}}}@media(max-width:700px){{table{{display:block;overflow-x:auto}}}}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"Septic Maintenance Checklist: Monthly, Yearly & Pumping Tasks","description":"A practical septic maintenance checklist grounded in current EPA homeowner guidance.","mainEntityOfPage":"{canonical}","publisher":{{"@type":"Organization","name":"SepticScope"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"How often should a septic system be inspected?","acceptedAnswer":{{"@type":"Answer","text":"EPA says the average household septic system should be inspected at least every three years. Systems with electrical float switches, pumps or mechanical components generally need more frequent inspection, often yearly."}}}},{{"@type":"Question","name":"How often should a septic tank be pumped?","acceptedAnswer":{{"@type":"Answer","text":"EPA says household septic tanks are typically pumped every three to five years, with frequency affected by household size, wastewater volume, solids accumulation and tank size."}}}},{{"@type":"Question","name":"What records should a septic homeowner keep?","acceptedAnswer":{{"@type":"Answer","text":"Keep the permit and as-built drawing, inspection reports, pumping receipts, repair records, service contracts and measurements or notes from maintenance visits."}}}}]}}</script>
</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / Maintenance checklist</div>
<h1>Septic maintenance checklist for homeowners</h1>
<p>A good septic maintenance plan is mostly routine record keeping, sensible water use, periodic professional inspection and protecting the drainfield. EPA's current homeowner guidance organizes care around four core tasks: inspect and pump, use water efficiently, dispose of waste properly and maintain the drainfield.</p>
<div class="note"><strong>Baseline schedule:</strong> EPA says the average household system should be inspected at least every <strong>three years</strong>, while household tanks are typically pumped every <strong>three to five years</strong>. Systems with pumps, floats or other mechanical components generally need more frequent professional attention. Local rules and your system's operating permit can require a different schedule.</div>
<h2>One-time setup: build your septic file</h2><ul class="checks"><li>Get the septic permit and approved design or as-built drawing from the local permitting authority.</li><li>Record the tank size, system type, installation date and known component locations.</li><li>Save pumping receipts, inspection reports, repair permits and service-contract documents together.</li><li>Mark tank lids, risers, distribution components and the drainfield on a property sketch without driving stakes into buried components.</li><li>Use the <a href="/counties/">SepticScope county directory</a> to verify the agency responsible for permits, records and local maintenance requirements.</li></ul>
<h2>Monthly and everyday habits</h2><ul class="checks"><li>Watch for unusual slow drains, gurgling, sewage odors, backups, standing water or unusually green/spongy grass over the septic area.</li><li>Fix leaking toilets and faucets instead of sending unnecessary water to the system.</li><li>Spread laundry and other high-water-use activities across the week when practical.</li><li>Flush only human waste and toilet paper. Use the <a href="/guides/what-not-to-flush-septic-system/">what-not-to-flush guide</a> for wipes, grease, cleaners, medications and additives.</li><li>Keep vehicles, heavy equipment, patios, sheds and other loads off the drainfield and tank area.</li><li>Keep roof drains, sump discharge and other stormwater away from the drainfield.</li></ul>
<h2>Once or twice a year</h2><ul class="checks"><li>Walk the tank and drainfield area and look for settlement, surfacing wastewater, wet areas, erosion or new root growth.</li><li>Confirm access lids and risers remain secure and undamaged.</li><li>If the system has an alarm, pump, float or treatment unit, follow the manufacturer and permit-required service schedule rather than waiting for symptoms.</li><li>Review your service history and schedule the next inspection or pumping visit before it becomes overdue.</li><li>After landscaping or construction, confirm no one has covered access points, redirected runoff toward the field or driven over system components.</li></ul>
<h2>Professional inspection checklist</h2><p>EPA says a typical inspection can include review of permits and maintenance records, opening and inspecting tanks, checking sludge and scum levels, and evaluating system components. Inspection scope varies by system type and jurisdiction.</p><div class="card"><ul class="checks"><li>Provide the professional your permit/as-built and prior service records.</li><li>Ask for measured sludge and scum levels when applicable, not just a calendar-based pumping recommendation.</li><li>Ask that visible tank condition, baffles/outlet devices, effluent filter and accessible mechanical components be documented as applicable.</li><li>Keep the written report and note the recommended next service date.</li><li>If repairs are recommended, determine whether local permits or inspections are required before work begins.</li></ul></div>
<h2>Pumping checklist</h2><ul class="checks"><li>Confirm which tank compartments will be pumped and whether locating or excavation is included.</li><li>Ask whether filter cleaning or inspection is included or separately priced.</li><li>Keep the pumping receipt and service notes.</li><li>Record any sludge/scum measurements and the next recommended inspection date.</li><li>If you are comparing quotes, use the <a href="/guides/septic-pumping-cost/">septic pumping cost guide</a> so each contractor is pricing the same scope.</li></ul>
<h2>Do not use the calendar as a diagnosis</h2><p>A routine maintenance interval is not a substitute for troubleshooting symptoms. If sewage is backing up, multiple drains are slow, the yard smells like sewage, the drainfield is wet or an alarm is active, use the <a href="/guides/septic-system-failure-signs/">septic failure warning-sign guide</a> and arrange appropriate professional diagnosis. Pumping may be part of the response, but it does not repair every drainfield, pipe, pump or distribution problem.</p>
<h2>When you buy or sell a home</h2><p>Do not rely only on the seller's recollection of maintenance. Obtain permits, design records, pumping history and a transaction-appropriate septic inspection. Transfer requirements vary by jurisdiction, so combine the <a href="/guides/buying-home-with-septic/">homebuyer septic checklist</a> with the local county guide.</p>
<h2>Simple maintenance record</h2><table><thead><tr><th>Date</th><th>Service</th><th>Provider / result</th><th>Next action</th></tr></thead><tbody><tr><td>________</td><td>Inspection</td><td>________________</td><td>________________</td></tr><tr><td>________</td><td>Pumping</td><td>________________</td><td>________________</td></tr><tr><td>________</td><td>Filter / mechanical service</td><td>________________</td><td>________________</td></tr><tr><td>________</td><td>Repair / permit</td><td>________________</td><td>________________</td></tr></tbody></table>
<p class="note"><strong>Print-friendly:</strong> this page is styled so the checklist and maintenance record can be printed or saved as a PDF from your browser without the header/footer.</p>
<h2>Official sources</h2><ul><li><a rel="nofollow" href="{epa_care}">U.S. EPA — How to Care for Your Septic System</a></li><li><a rel="nofollow" href="{epa_tools}">U.S. EPA — Tools about Septic Systems for Homeowners</a></li><li><a rel="nofollow" href="{epa_faq}">U.S. EPA — Frequent Questions on Septic Systems</a></li><li><a rel="nofollow" href="{epa_top10}">U.S. EPA — Top 10 Ways to Be a Good Septic Owner</a></li></ul>
<p><em>SepticScope provides general homeowner information. Local regulations, permit conditions and system-specific professional recommendations control when they are more specific.</em></p>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    (out / "index.html").write_text(page, encoding="utf-8")

    hub = SITE / "guides" / "index.html"
    if hub.exists():
        text = hub.read_text(encoding="utf-8", errors="replace")
        if "/guides/septic-maintenance-checklist/" not in text:
            promo = '<section><h2>Septic maintenance checklist</h2><p>Use the <a href="/guides/septic-maintenance-checklist/">print-friendly septic maintenance checklist</a> for routine care, inspection and pumping records, drainfield protection and warning signs.</p></section>'
            text = text.replace("</main>", promo + "</main>", 1) if "</main>" in text else text.replace("</body>", promo + "</body>", 1)
            hub.write_text(text, encoding="utf-8")

    sitemap = SITE / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        if canonical not in text:
            text = text.replace("</urlset>", f"<url><loc>{canonical}</loc><lastmod>2026-08-31</lastmod></url></urlset>")
            sitemap.write_text(text, encoding="utf-8")


atexit.register(_write_maintenance_checklist)
