"""Generate the SepticScope septic system types comparison guide after the site build."""
from __future__ import annotations

import atexit
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
GA_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"


def _write_system_types_guide() -> None:
    if not SITE.is_dir():
        return

    guide_dir = SITE / "guides" / "types-of-septic-systems"
    guide_dir.mkdir(parents=True, exist_ok=True)
    canonical = "https://septicscope.com/guides/types-of-septic-systems/"
    epa_types = "https://www.epa.gov/septic/types-septic-systems"
    epa_care = "https://www.epa.gov/septic/how-care-your-septic-system"
    epa_faq = "https://www.epa.gov/septic/frequent-questions-septic-systems"

    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Types of Septic Systems: Conventional, Aerobic, Mound & More | SepticScope</title>
<meta name="description" content="Compare common septic system types, including conventional, chamber, aerobic, mound, drip and sand-filter systems. Learn how to identify yours and what changes maintenance and permitting.">
<link rel="canonical" href="{canonical}">
<style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:1000px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}main{{padding-top:42px;padding-bottom:70px}}.crumb{{font-size:.92rem;color:var(--muted)}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}}h2{{margin-top:1.9em}}h3{{margin-top:1.45em}}a{{color:var(--accent)}}.card,.note{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}table{{width:100%;border-collapse:collapse;margin:18px 0}}th,td{{text-align:left;border-bottom:1px solid var(--line);padding:10px;vertical-align:top}}footer{{border-top:1px solid var(--line);color:var(--muted)}}@media(max-width:700px){{table{{display:block;overflow-x:auto}}}}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"Types of Septic Systems: Conventional, Aerobic, Mound & More","description":"A homeowner comparison of common septic system types, how they work, why a site may need them, and how system type changes maintenance and permitting.","mainEntityOfPage":"{canonical}","publisher":{{"@type":"Organization","name":"SepticScope"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"How can I find out what type of septic system I have?","acceptedAnswer":{{"@type":"Answer","text":"Start with the property's septic permit, approved design or as-built drawing from the local permitting authority. Those records are more reliable than identifying a system only from what is visible in the yard."}}}},{{"@type":"Question","name":"What is the difference between a conventional and aerobic septic system?","acceptedAnswer":{{"@type":"Answer","text":"A conventional system typically relies on a septic tank and soil-based drainfield. An aerobic treatment unit adds oxygen to increase biological treatment and may include additional treatment and disinfection components, so it generally has more mechanical equipment and maintenance needs."}}}},{{"@type":"Question","name":"Why would a property need a mound septic system?","acceptedAnswer":{{"@type":"Answer","text":"EPA says mound systems can be used where soil is shallow, groundwater is high or bedrock is shallow. The mound creates an elevated treatment area and normally uses a pump chamber to dose effluent into the mound."}}}}]}}</script>
</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / Types of septic systems</div>
<h1>Types of septic systems: how to identify and compare them</h1>
<p>“Septic system” can describe several different treatment and dispersal designs. That distinction matters because the equipment you own can change maintenance, electricity use, service needs, replacement planning and the permits that apply to your property.</p>
<div class="note"><strong>Best way to identify your system:</strong> get the septic permit, approved design or as-built drawing from the local permitting authority. Yard clues can help, but records are more reliable. Use the <a href="/counties/">SepticScope county directory</a> to find the responsible agency and available records resources.</div>
<h2>Quick comparison of common septic system types</h2>
<table><thead><tr><th>System type</th><th>How it works</th><th>What homeowners should notice</th></tr></thead><tbody>
<tr><td>Conventional</td><td>A septic tank separates solids, and effluent moves to a soil-based drainfield for additional treatment.</td><td>Relatively simple design, but soil, setbacks and available drainfield area still control whether it is appropriate for a site.</td></tr>
<tr><td>Chamber</td><td>Open-bottom chambers replace gravel in the drainfield trenches and distribute effluent into the soil.</td><td>Still relies on soil treatment; the dispersal hardware differs from a traditional gravel trench.</td></tr>
<tr><td>Drip distribution</td><td>Effluent is dosed through shallow drip tubing in the dispersal area.</td><td>EPA notes it requires a dose tank and additional components such as electrical power, increasing maintenance needs.</td></tr>
<tr><td>Aerobic treatment unit (ATU)</td><td>Oxygen is introduced into treatment to increase biological activity; some designs add disinfection or additional treatment stages.</td><td>More mechanical equipment and regular lifetime maintenance should be expected.</td></tr>
<tr><td>Mound</td><td>A pump doses effluent to a constructed sand mound where treatment occurs before dispersal into native soil.</td><td>Often used for shallow soil, high groundwater or shallow bedrock and requires space plus periodic maintenance.</td></tr>
<tr><td>Recirculating sand filter</td><td>Effluent is pumped through a sand filter for additional treatment before final dispersal.</td><td>Provides a higher level of treatment but adds pumps and treatment components compared with a basic gravity system.</td></tr>
</tbody></table>
<h2>Conventional septic systems</h2>
<p>A conventional system generally combines a septic tank with a subsurface wastewater infiltration system, commonly called a drainfield. Wastewater separates in the tank, and liquid effluent then moves into the soil, where natural processes provide additional treatment.</p>
<p>“Conventional” does not mean every property can use one. Soil characteristics, seasonal groundwater, bedrock, slope, lot size, wells, water bodies and required setbacks can determine whether the local authority approves a conventional design or requires another approach.</p>
<h2>Chamber systems</h2>
<p>EPA describes chamber systems as a widely used alternative to gravel drainfields. A series of connected chambers creates space in the soil for wastewater to contact the treatment area. For a homeowner, the important point is that a chamber system is still a soil-based dispersal system even though its drainfield construction differs from a traditional gravel trench.</p>
<h2>Aerobic treatment units</h2>
<p>An aerobic treatment unit uses many of the same biological concepts as a municipal treatment plant on a much smaller scale. EPA explains that introducing oxygen increases bacterial activity and treatment. Some ATUs also use pretreatment, final treatment or disinfection stages.</p>
<div class="card"><strong>Why ATUs matter to ownership:</strong> EPA says they can be useful on smaller lots, where soils are inadequate, where groundwater is high, or near nutrient-sensitive surface water. They also contain active treatment equipment, so regular lifetime maintenance should be expected. Check the local permit before assuming a generic maintenance schedule applies.</div>
<h2>Mound systems</h2>
<p>Mound systems raise the treatment area above existing grade with an engineered sand mound. Effluent is normally pumped in controlled doses from a pump chamber to the mound. EPA identifies shallow soil, high groundwater and shallow bedrock as conditions where mound systems may be an option.</p>
<p>If you are buying a property with a mound, verify the approved design, pump and alarm information, service history, the boundaries of the mound and any reserve area. Do not assume the visible mound is simply landscaping.</p>
<h2>Drip distribution systems</h2>
<p>Drip distribution places dispersal tubing relatively close to the ground surface rather than using a large conventional trench or mound. EPA notes that this can avoid the need for a large mound, but the system requires a dose tank and additional components, including electrical power. That makes the permit, control equipment and maintenance documentation especially useful to keep with the property records.</p>
<h2>Recirculating sand filters and other advanced treatment</h2>
<p>A recirculating sand filter pumps effluent through a sand treatment unit before it reaches the final dispersal area. These systems can provide a higher level of treatment where site conditions or environmental requirements call for it. Other jurisdictions may approve additional proprietary or engineered treatment technologies. The local permit is the authoritative record for the system installed on a specific parcel.</p>
<h2>System type changes maintenance and replacement planning</h2>
<p>A basic tank-and-gravity-drainfield system has fewer mechanical components than a design with pumps, floats, controls, aeration or timed dosing. EPA's homeowner guidance says the average household septic system should be inspected at least every three years, while systems with electrical switches, pumps or mechanical components should generally be inspected more frequently, typically once a year. Local operating permits and manufacturer requirements may be stricter.</p>
<p>For routine service planning, see the <a href="/guides/septic-pumping-cost/">septic pumping cost and maintenance guide</a>. If a major component has failed, the <a href="/guides/septic-system-replacement-cost/">repair vs. replacement guide</a> explains why system type and site conditions can materially change the scope of work.</p>
<h2>Buying a home? Do not rely on the listing description</h2>
<p>Real-estate listings may say only “septic,” which is not enough to understand the equipment or future obligations. Request the permit, as-built drawing, maintenance history and latest inspection. Then compare the approved design with what is actually on the property. The <a href="/guides/buying-home-with-septic/">SepticScope homebuyer septic checklist</a> covers the rest of the due-diligence process.</p>
<h2>What to look for in your local records</h2>
<div class="card"><ul><li>Approved system type and design flow</li><li>Tank and treatment-unit capacity</li><li>Drainfield or dispersal layout</li><li>Pump, alarm or control-panel requirements</li><li>Reserve or replacement area</li><li>Operation-and-maintenance conditions</li><li>Inspection or reporting requirements for advanced systems</li><li>Repair, alteration and replacement permits</li></ul></div>
<h2>Official sources</h2><ul><li><a rel="nofollow" href="{epa_types}">U.S. EPA — Types of Septic Systems</a></li><li><a rel="nofollow" href="{epa_care}">U.S. EPA — How to Care for Your Septic System</a></li><li><a rel="nofollow" href="{epa_faq}">U.S. EPA — Frequent Questions on Septic Systems</a></li></ul>
<p><em>System names and requirements vary by jurisdiction. SepticScope provides general homeowner information and routes users to official local sources; the approved permit, local regulations and site-specific professional findings control.</em></p>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    (guide_dir / "index.html").write_text(page, encoding="utf-8")

    hub = SITE / "guides" / "index.html"
    if hub.exists():
        text = hub.read_text(encoding="utf-8", errors="replace")
        if "/guides/types-of-septic-systems/" not in text:
            promo = '<section><h2>Types of septic systems</h2><p>Compare <a href="/guides/types-of-septic-systems/">conventional, chamber, aerobic, mound, drip and sand-filter septic systems</a>, then use local permit records to identify the system on your property.</p></section>'
            text = text.replace("</main>", promo + "</main>", 1) if "</main>" in text else text.replace("</body>", promo + "</body>", 1)
            hub.write_text(text, encoding="utf-8")

    sitemap = SITE / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        if canonical not in text:
            text = text.replace("</urlset>", f"<url><loc>{canonical}</loc><lastmod>2026-08-31</lastmod></url></urlset>")
            sitemap.write_text(text, encoding="utf-8")


atexit.register(_write_system_types_guide)
