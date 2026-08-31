"""Generate an evidence-grounded septic system lifespan planning guide after the site build."""
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
    out = SITE / "guides" / "septic-system-lifespan"
    out.mkdir(parents=True, exist_ok=True)
    canonical = "https://septicscope.com/guides/septic-system-lifespan/"
    epa_care = "https://www.epa.gov/septic/how-care-your-septic-system"
    epa_malfunction = "https://www.epa.gov/septic/resolving-septic-system-malfunctions"
    umd = "https://extension.umd.edu/programs/environment-natural-resources/program-areas/wells-septics-and-water-quality/septicsunderstandingmaintaining/faqs-septic-systems"
    wsu = "https://shorestewards.cw.wsu.edu/faq/signs-of-a-failing-septic-system/"
    polk = "https://www.polkcountyor.gov/803/Sanitation-FAQs"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>How Long Does a Septic System Last? Lifespan & Replacement Planning | SepticScope</title>
<meta name="description" content="How long does a septic system last? Use a 20–30 year planning range carefully, learn what shortens system life, and know when age calls for inspection rather than automatic replacement.">
<link rel="canonical" href="{canonical}">
<style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b;--warn:#fff7df}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:1000px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}main{{padding-top:42px;padding-bottom:70px}}.crumb{{font-size:.92rem;color:var(--muted)}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}}h2{{margin-top:1.9em}}a{{color:var(--accent)}}.card,.note{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}.answer{{font-size:1.08rem;background:var(--warn)}}table{{width:100%;border-collapse:collapse;margin:18px 0}}th,td{{text-align:left;border-bottom:1px solid var(--line);padding:10px;vertical-align:top}}footer{{border-top:1px solid var(--line);color:var(--muted)}}@media(max-width:700px){{table{{display:block;overflow-x:auto}}}}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"How Long Does a Septic System Last? Lifespan & Replacement Planning","description":"A homeowner-focused septic system lifespan and replacement-planning guide grounded in public-agency and Extension guidance.","mainEntityOfPage":"{canonical}","publisher":{{"@type":"Organization","name":"SepticScope"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"How long does a septic system last?","acceptedAnswer":{{"@type":"Answer","text":"Public-agency and university Extension guidance commonly uses about 20 to 30 years as a planning range for conventional septic systems, while emphasizing that actual service life can be shorter or longer depending on design, installation, soil and groundwater conditions, water use, maintenance and damage."}}}},{{"@type":"Question","name":"Does a 30-year-old septic system need to be replaced?","acceptedAnswer":{{"@type":"Answer","text":"Not solely because of age. Age should trigger better records review, inspection and replacement planning. Actual replacement decisions should be based on system condition, performance, site constraints and local permitting requirements."}}}},{{"@type":"Question","name":"What shortens septic system life?","acceptedAnswer":{{"@type":"Answer","text":"Common contributors include inadequate maintenance, excessive hydraulic loading, surface or groundwater infiltration, root intrusion, compaction or vehicle traffic over the drainfield, unsuitable site conditions, poor design or installation, and solids reaching the soil treatment area."}}}}]}}</script>
</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / Septic system lifespan</div>
<h1>How long does a septic system last?</h1>
<div class="card answer"><strong>Short answer:</strong> For planning, several public agencies and university Extension programs use roughly <strong>20–30 years</strong> for a conventional septic system, while noting that properly maintained systems may last longer and poorly maintained or poorly sited systems may fail sooner. Treat that range as a planning signal—not an expiration date.</div>
<p>The most useful question is not simply “How old is my septic tank?” A septic system is a collection of components, and the tank, pipes, distribution components, pumps and soil treatment area do not necessarily age at the same rate. Site conditions and maintenance history can matter as much as the installation year.</p>
<h2>Age alone does not prove failure</h2>
<p>A system that is 25 or 30 years old is not automatically failed, and a newer system is not automatically healthy. Washington State University notes that many systems last beyond a 20–30 year design-life range, while improper maintenance is a common cause of early failure. University of Maryland Extension likewise identifies maintenance, groundwater or surface-water infiltration, roots and misuse as factors that can shorten life.</p>
<table><thead><tr><th>If your system is...</th><th>Practical next step</th></tr></thead><tbody><tr><td>Newer, documented and trouble-free</td><td>Keep permit/as-built records, follow the required inspection/service schedule and protect the drainfield.</td></tr><tr><td>Older but working normally</td><td>Do not replace it just because of age. Locate records, confirm system type and get a qualified inspection if history is unclear.</td></tr><tr><td>Older with no maintenance records</td><td>Treat the unknown history as a reason for inspection and budgeting, especially before a property sale or major renovation.</td></tr><tr><td>Showing backups, persistent wetness, sewage odor or multiple slow drains</td><td>Move from lifespan planning to diagnosis. Avoid assuming the tank or drainfield must be replaced until the cause is evaluated.</td></tr></tbody></table>
<h2>What can shorten septic system life?</h2>
<ul><li><strong>Solids reaching the drainfield.</strong> EPA recommends routine inspection and pumping because accumulated solids can impair the treatment system.</li><li><strong>Too much water.</strong> Leaks and concentrated household water use increase hydraulic loading and can stress the soil treatment area.</li><li><strong>Drainfield damage.</strong> Vehicles, structures, soil compaction, roots and excess surface water can interfere with the field.</li><li><strong>Groundwater or site constraints.</strong> Soil characteristics, seasonal groundwater and drainage conditions affect how well the system can treat and disperse wastewater.</li><li><strong>Mechanical-system neglect.</strong> Systems with pumps, controls or treatment units require more component-specific maintenance than a basic gravity system.</li><li><strong>Poor original design or installation.</strong> Maintenance cannot fully correct a system that was undersized, improperly installed or poorly matched to the site.</li></ul>
<h2>Tank age is not the same as system age</h2>
<p>Search results often publish precise lifespan tables for concrete, plastic, fiberglass, pumps and drainfields. Those figures can create false precision because material quality, installation, soil chemistry, groundwater, loading and local design standards vary. For homeowners, a better approach is to identify the actual system, obtain its permit/as-built records, document observed condition and let a qualified local professional evaluate components that are accessible and relevant.</p>
<p>If you do not know what type of system you own, start with the <a href="/guides/types-of-septic-systems/">types of septic systems guide</a>. If the property is changing hands, use the <a href="/guides/septic-inspection-checklist/">septic inspection checklist</a>.</p>
<h2>When should an older system be inspected?</h2>
<p>Inspection makes particular sense when the maintenance history is missing, the property is being purchased or sold, household use is changing, an addition may increase design flow, or warning signs appear. EPA identifies symptoms such as plumbing backups, slow drains, gurgling, standing water, sewage odors and unusually green or spongy drainfield areas as potential malfunction indicators.</p>
<div class="note"><strong>Important:</strong> Pumping can be necessary maintenance, but a pump-out is not proof that the rest of the system is healthy. Likewise, an older system that still drains is not proof that the soil treatment area is performing properly.</div>
<h2>How to extend useful system life</h2>
<ul><li>Follow the inspection and pumping schedule appropriate to your household and system type.</li><li>Fix plumbing leaks and avoid concentrating large water loads into a short period.</li><li>Keep vehicles, structures and heavy equipment off the drainfield.</li><li>Route roof and surface drainage away from the field.</li><li>Keep inappropriate solids, wipes, grease and harmful materials out of the plumbing.</li><li>Maintain pumps, alarms, filters and treatment-unit components when your design includes them.</li><li>Keep permits, as-built drawings, pumping receipts, inspection reports and repair records together.</li></ul>
<p>Use the <a href="/guides/septic-maintenance-checklist/">septic maintenance checklist</a> to organize recurring care. If there are already signs of soil-treatment trouble, see <a href="/guides/septic-drainfield-repair-replacement/">drainfield repair vs. replacement</a>.</p>
<h2>Planning for replacement without replacing too early</h2>
<p>Once a system moves into the older end of the common planning range, learn what replacement would require before an emergency forces the decision. Find the original permit and reserve-area information, verify current local rules and understand whether today's replacement standards differ from the original design. Use the <a href="/counties/">SepticScope county directory</a> to locate the relevant permitting authority.</p>
<h2>Official and Extension sources</h2><ul><li><a rel="nofollow" href="{epa_care}">U.S. EPA — How to Care for Your Septic System</a></li><li><a rel="nofollow" href="{epa_malfunction}">U.S. EPA — Resolving Septic System Malfunctions</a></li><li><a rel="nofollow" href="{umd}">University of Maryland Extension — FAQs on Septic Systems</a></li><li><a rel="nofollow" href="{wsu}">Washington State University Extension — Signs of a Failing Septic System</a></li><li><a rel="nofollow" href="{polk}">Polk County, Oregon — Sanitation FAQs</a></li></ul>
<p><em>SepticScope provides general information, not an engineering opinion or a determination that a system is compliant or failed. Local law, permit conditions, site conditions and qualified professionals control when more specific.</em></p>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    (out / "index.html").write_text(page, encoding="utf-8")
    hub = SITE / "guides" / "index.html"
    if hub.exists():
        text = hub.read_text(encoding="utf-8", errors="replace")
        if "/guides/septic-system-lifespan/" not in text:
            promo = '<section><h2>How long does a septic system last?</h2><p>Use the <a href="/guides/septic-system-lifespan/">septic system lifespan guide</a> to understand the common 20–30 year planning range, what shortens service life and when age should trigger inspection rather than automatic replacement.</p></section>'
            text = text.replace("</main>", promo + "</main>", 1) if "</main>" in text else text.replace("</body>", promo + "</body>", 1)
            hub.write_text(text, encoding="utf-8")
    sitemap = SITE / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        if canonical not in text:
            text = text.replace("</urlset>", f"<url><loc>{canonical}</loc><lastmod>2026-08-31</lastmod></url></urlset>")
            sitemap.write_text(text, encoding="utf-8")


atexit.register(_write_guide)
