"""Generate the SepticScope septic replacement cost guide after the site build."""
from __future__ import annotations

import atexit
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
GA_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"


def _write_replacement_guide() -> None:
    if not SITE.is_dir():
        return

    guide_dir = SITE / "guides" / "septic-system-replacement-cost"
    guide_dir.mkdir(parents=True, exist_ok=True)
    canonical = "https://septicscope.com/guides/septic-system-replacement-cost/"
    epa_maintain = "https://www.epa.gov/septic/why-maintain-your-septic-system"
    epa_types = "https://www.epa.gov/septic/types-septic-systems"

    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Septic System Replacement Cost in 2026: Repair vs. Replace | SepticScope</title>
<meta name="description" content="Plan for septic replacement costs in 2026. Learn when repair may be enough, what drives replacement cost, how system type and site conditions matter, and which local permits to check.">
<link rel="canonical" href="{canonical}">
<style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:1000px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}main{{padding-top:42px;padding-bottom:70px}}.crumb{{font-size:.92rem;color:var(--muted)}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}}h2{{margin-top:1.9em}}a{{color:var(--accent)}}.card,.note{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}table{{width:100%;border-collapse:collapse;margin:18px 0}}th,td{{text-align:left;border-bottom:1px solid var(--line);padding:10px;vertical-align:top}}footer{{border-top:1px solid var(--line);color:var(--muted)}}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"Septic System Replacement Cost in 2026: Repair vs. Replace","description":"A homeowner guide to septic replacement cost drivers, repair-versus-replace decisions, system type, site conditions and local permitting.","mainEntityOfPage":"{canonical}","publisher":{{"@type":"Organization","name":"SepticScope"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"How much does it cost to replace a septic system?","acceptedAnswer":{{"@type":"Answer","text":"EPA says repairing or replacing a malfunctioning conventional system can cost about $5,000 to $15,000, while alternative systems can cost more. Actual replacement cost depends on system type, site conditions, design, permits, excavation and local labor."}}}},{{"@type":"Question","name":"Can a failing septic system be repaired instead of replaced?","acceptedAnswer":{{"@type":"Answer","text":"Sometimes. A failed component, damaged baffle, pump, pipe or distribution box may be repairable, while a failed drainfield, undersized system or site that no longer meets current requirements may require more extensive work. A qualified local professional and the permitting authority should determine the approved scope."}}}},{{"@type":"Question","name":"Do I need a permit to replace a septic system?","acceptedAnswer":{{"@type":"Answer","text":"Septic repair and replacement requirements are set by state and local authorities. Many projects require permits, site evaluation, design review and inspections. Check the responsible county or local health or environmental agency before work begins."}}}}]}}</script>
</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / Septic replacement cost</div>
<h1>Septic system replacement cost in 2026: repair vs. replace</h1>
<p>A septic replacement quote is not just the price of a new tank. The expensive part of many projects is the property-specific work around it: diagnosing the failure, evaluating soil and available area, choosing an approved system type, obtaining permits, excavating, installing treatment and dispersal components, and passing inspections.</p>
<div class="note"><strong>Useful national benchmark:</strong> EPA currently says regular maintenance of about <strong>$250 to $500 every three to five years</strong> is small compared with <strong>$5,000 to $15,000</strong> to repair or replace a malfunctioning conventional system. EPA also notes that alternative systems can cost more. Treat that as planning context, not a local bid.</div>
<h2>What actually drives septic replacement cost?</h2><table><thead><tr><th>Cost driver</th><th>Why it matters</th></tr></thead><tbody>
<tr><td>Repair versus full replacement</td><td>Replacing one failed component is fundamentally different from replacing the tank, treatment components and drainfield.</td></tr>
<tr><td>System type</td><td>Conventional gravity systems are simpler than systems that use pumps, controls, aerobic treatment, mounds, sand filters or drip distribution.</td></tr>
<tr><td>Soil, groundwater and slope</td><td>Site conditions determine what dispersal methods can be approved and may require additional design or treatment.</td></tr>
<tr><td>Available replacement area</td><td>A property with a clear reserve area can be easier to redesign than a constrained lot with buildings, wells, water bodies or property-line setbacks.</td></tr>
<tr><td>Tank and design capacity</td><td>Required capacity is commonly tied to design flow and bedroom count, subject to state and local rules.</td></tr>
<tr><td>Permits and professional design</td><td>Local requirements can include applications, soil evaluation, engineered plans, inspections and separate fees.</td></tr>
<tr><td>Excavation and restoration</td><td>Access, demolition, rock, roots, grading, hauling and restoring the yard can materially change the total project cost.</td></tr>
</tbody></table>
<h2>Repair first or replace the system?</h2><p>The answer depends on what has actually failed. A bad pump, alarm, baffle, filter, pipe or distribution component may be repairable. A saturated or failed drainfield, a structurally failed tank, an undersized system, or a site that cannot support the existing design may require a substantially larger project.</p>
<div class="card"><strong>Before accepting a full-replacement quote, ask for:</strong><ul><li>The diagnosed failure and which component caused it.</li><li>Whether a code-compliant repair is allowed locally.</li><li>Whether the existing permit or as-built drawing was reviewed.</li><li>Whether the quoted scope includes tank, drainfield, pumps, controls and piping.</li><li>Which permits, soil evaluations, engineering or inspections are included.</li><li>What yard restoration, hauling or abandonment work is excluded.</li></ul></div>
<h2>System type can change both installation and long-term ownership cost</h2><p>EPA describes several common onsite wastewater designs, including conventional systems, chamber systems, drip distribution, aerobic treatment units, mound systems and recirculating sand filters. Advanced systems can solve difficult site conditions, but pumps, controls, timed dosing and treatment equipment can add installation and ongoing maintenance obligations.</p>
<p>If you do not know what system is installed, start with the property's permit or as-built record and compare it with EPA's <a rel="nofollow" href="{epa_types}">overview of septic system types</a>.</p>
<h2>Local permitting can change the project before a contractor starts digging</h2><p>Septic replacement is regulated locally. Depending on the jurisdiction, the process may require a repair or construction permit, site and soil evaluation, system design, setback review, inspection, abandonment of old components, or operating permits for advanced treatment. Use the <a href="/counties/">SepticScope county directory</a> to find the responsible permitting authority and verified local resources where available.</p>
<h2>Warning signs do not automatically mean replacement</h2><p>Slow drains, sewage backups, odors, standing water or unusually lush growth over the drainfield can indicate a septic problem, but they do not identify the failed component by themselves. Start with diagnosis. Pumping may be overdue, a mechanical component may have failed, or the drainfield may be compromised. See the <a href="/guides/septic-pumping-cost/">septic pumping cost guide</a> for routine maintenance and quote comparisons.</p>
<h2>Buying a home with an older septic system</h2><p>Age alone does not prove that a system needs replacement. For a purchase, combine a professional septic inspection with permit records, maintenance history, the approved system capacity and any local transfer requirements. The <a href="/guides/buying-home-with-septic/">SepticScope homebuyer checklist</a> and <a href="/guides/septic-inspection-cost/">inspection cost guide</a> cover that process in more detail.</p>
<h2>Official sources</h2><ul><li><a rel="nofollow" href="{epa_maintain}">U.S. EPA — Why Maintain Your Septic System</a></li><li><a rel="nofollow" href="{epa_types}">U.S. EPA — Types of Septic Systems</a></li></ul>
<p><em>Costs vary by site and market. SepticScope provides planning information and links to regulatory sources; local permitting requirements and site-specific professional findings control.</em></p>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    (guide_dir / "index.html").write_text(page, encoding="utf-8")

    hub = SITE / "guides" / "index.html"
    if hub.exists():
        text = hub.read_text(encoding="utf-8", errors="replace")
        if "/guides/septic-system-replacement-cost/" not in text:
            promo = '<section><h2>Septic repair vs. replacement cost</h2><p>Use the <a href="/guides/septic-system-replacement-cost/">septic system replacement cost guide</a> to understand repair-versus-replace decisions, major cost drivers, system types and local permitting.</p></section>'
            text = text.replace("</main>", promo + "</main>", 1) if "</main>" in text else text.replace("</body>", promo + "</body>", 1)
            hub.write_text(text, encoding="utf-8")

    sitemap = SITE / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        if canonical not in text:
            text = text.replace("</urlset>", f"<url><loc>{canonical}</loc><lastmod>2026-08-31</lastmod></url></urlset>")
            sitemap.write_text(text, encoding="utf-8")


atexit.register(_write_replacement_guide)
