"""Generate an evidence-grounded winter septic care and frozen-system guide."""
from __future__ import annotations

import atexit
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
GA_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"


def _write_winter_guide() -> None:
    if not SITE.is_dir():
        return

    out = SITE / "guides" / "septic-system-winter-care"
    out.mkdir(parents=True, exist_ok=True)
    canonical = "https://septicscope.com/guides/septic-system-winter-care/"
    mpca = "https://www.pca.state.mn.us/news-and-stories/dont-let-your-septic-system-freeze"
    umn_freeze = "https://septic.umn.edu/freezing-problems"
    umn_seasonal = "https://septic.umn.edu/seasonal-care"

    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Frozen Septic System? Winter Care, Prevention & What to Do | SepticScope</title>
<meta name="description" content="Evidence-grounded winter septic care: why systems freeze, warning signs, safe prevention steps, what not to do, and when winter pumping may or may not make sense.">
<link rel="canonical" href="{canonical}">
<style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b;--warn:#fff7e8}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:1000px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}main{{padding-top:42px;padding-bottom:70px}}.crumb{{font-size:.92rem;color:var(--muted)}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}}h2{{margin-top:1.9em}}h3{{margin-top:1.4em}}a{{color:var(--accent)}}.card,.note,.warn{{border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}.card,.note{{background:var(--panel)}}.warn{{background:var(--warn)}}table{{width:100%;border-collapse:collapse;margin:18px 0}}th,td{{text-align:left;border-bottom:1px solid var(--line);padding:10px;vertical-align:top}}footer{{border-top:1px solid var(--line);color:var(--muted)}}@media(max-width:700px){{table{{display:block;overflow-x:auto}}}}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"Frozen Septic System? Winter Care, Prevention & What to Do","description":"A homeowner guide to septic-system freezing, prevention, safe response and winter pumping decisions grounded in public-agency guidance.","mainEntityOfPage":"{canonical}","publisher":{{"@type":"Organization","name":"SepticScope"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Can a septic system freeze in winter?","acceptedAnswer":{{"@type":"Answer","text":"Yes. Pipes, tanks, pump lines and soil treatment areas can freeze, especially with little snow cover, compacted snow or soil, irregular use, leaking fixtures, poor pipe drainage or cold air entering through open components."}}}},{{"@type":"Question","name":"Should I leave water running to keep my septic system from freezing?","acceptedAnswer":{{"@type":"Answer","text":"No. Minnesota Pollution Control Agency guidance says not to leave water running continually because it can overload the system. Normal warm-water use spread through the day can help when freezing is a concern."}}}},{{"@type":"Question","name":"Should I pump my septic tank before winter?","acceptedAnswer":{{"@type":"Answer","text":"Not as a universal rule. Seasonal or vacant properties may sometimes benefit from pumping before an extended absence, but cold-climate guidance warns that routine winter pumping can create freezing problems. High-water-table conditions also require special caution. Follow local and system-specific professional guidance."}}}},{{"@type":"Question","name":"What should I do if my septic system is already frozen?","acceptedAnswer":{{"@type":"Answer","text":"Reduce water use and contact a qualified onsite septic professional. Do not add salt, antifreeze or septic additives, do not start a fire over the system, do not pump sewage onto the ground, and do not run water continuously to try to thaw it."}}}}]}}</script>
</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / Winter septic care</div>
<h1>Frozen septic system? Winter care and prevention</h1>
<p>Cold weather can freeze more than the tank itself. The house sewer, septic or pump tank, pressure or gravity lines, and the soil treatment area can all be affected. The highest-risk situations usually involve shallow or exposed components, little insulating snow, compacted ground, irregular use, plumbing leaks or a system that was already hydraulically stressed.</p>
<div class="note"><strong>Key point:</strong> winter advice is not one-size-fits-all. Public guidance from Minnesota — where septic freezing is a recurring cold-climate issue — specifically warns against several popular internet fixes, including continuously running water and adding antifreeze or salt to a frozen system.</div>
<h2>Quick winter decision table</h2><table><thead><tr><th>Situation</th><th>Best next step</th></tr></thead><tbody>
<tr><td>System working normally before freeze-up</td><td>Protect insulation, fix leaks, keep traffic off the septic area and continue normal household use.</td></tr>
<tr><td>New system with little grass cover</td><td>Consider 8–12 inches of loose mulch such as straw, leaves or hay over vulnerable system areas before they freeze.</td></tr>
<tr><td>Slow/no drains during a cold spell</td><td>Reduce water use and call an onsite septic professional to determine where the freeze or blockage is occurring.</td></tr>
<tr><td>Pump appears to run continuously</td><td>Shut the pump off and call a qualified professional; a frozen discharge line can prevent the pump from moving effluent.</td></tr>
<tr><td>Seasonal or vacant home</td><td>Plan before leaving. Pumping may be appropriate in some cases, but high-water-table conditions and local rules can change that decision.</td></tr>
</tbody></table>
<h2>Why septic systems freeze</h2><p>The University of Minnesota identifies several recurring causes: lack of insulating snow, compacted snow or soils, limited vegetative cover, irregular or very low system use, leaking plumbing fixtures that send a slow trickle into pipes, lines that sag or do not drain completely, open risers or inspection points that admit cold air, and already waterlogged treatment areas.</p>
<h3>Snow can be useful insulation</h3><p>Uncompacted snow helps hold heat in the soil. Avoid routine vehicle, ATV, snowmobile, livestock or heavy foot traffic over the tank, piping and drainfield because compaction can drive frost deeper. Do not plow snow off the treatment area just to expose it to cold air.</p>
<h3>Small leaks can be worse than normal use</h3><p>A leaking toilet, faucet, humidifier or furnace condensate line can create a slow film of water that freezes in a pipe. Fix leaks before sustained cold weather. If freezing is a concern, public guidance favors normal, distributed warm-water use over leaving a faucet running continuously.</p>
<h2>Before winter: practical prevention checklist</h2><div class="card"><ul><li>Know where the house sewer, tank, pump tank, lines and drainfield or mound are located. Use permits or as-built records when available.</li><li>Fix leaking toilets, faucets and other low-flow discharges.</li><li>Keep lids, risers and inspection pipes secure, closed and appropriately insulated.</li><li>Keep vehicles and heavy traffic off the system area.</li><li>If a new or exposed system lacks vegetative cover, consider a loose 8–12 inch mulch layer over vulnerable areas before freeze-up.</li><li>Review alarms, pumps and mechanical components before severe weather if your system uses them.</li><li>Keep routine records with the <a href="/guides/septic-maintenance-checklist/">SepticScope septic maintenance checklist</a>.</li></ul></div>
<h2>Should you pump the tank before winter?</h2><p><strong>Do not treat “pump before winter” as a universal rule.</strong> The University of Minnesota notes that routine cleaning/pumping during cold months can be problematic because an emptied tank and treatment system may receive little warm wastewater while refilling, increasing freeze risk. For Minnesota, its seasonal guidance gives a general rule of thumb to avoid routine pumping from November through April.</p>
<p>Seasonal cabins and homes that will be unused for an extended period are different. In some situations, pumping before leaving can be part of a winterization plan. However, University guidance specifically cautions that high-water-table sites need special consideration before a tank is pumped. Your local code, tank construction and site conditions control. Find the permitting authority through the <a href="/counties/">SepticScope county directory</a>.</p>
<div class="warn"><strong>Avoid blanket cost-saving advice:</strong> pumping because a calendar says “winter is coming” is not the same as pumping because solids levels or a professional inspection show it is due. Follow the <a href="/guides/septic-maintenance-checklist/">maintenance checklist</a> and local requirements.</div>
<h2>Signs a septic system may be frozen</h2><ul><li>Multiple fixtures suddenly drain slowly or stop draining during sustained cold weather.</li><li>Toilets will not flush normally or plumbing begins to back up.</li><li>A pump or alarm behaves abnormally, especially if a pump appears to run without moving effluent.</li><li>Seepage or ponding appears around the septic area.</li></ul><p>These symptoms can also indicate non-freezing failures. Use the timing, weather and professional diagnosis to separate a frozen line from a clog, pump problem or overloaded/failing drainfield.</p>
<h2>What to do if the system is already frozen</h2><ol><li><strong>Reduce water use.</strong> Wastewater has fewer places to go while the system is obstructed.</li><li><strong>Call an onsite septic professional.</strong> Professionals can use cameras and appropriate thawing equipment to identify where the freeze occurred.</li><li><strong>Correct the cause.</strong> A system thawed without fixing the underlying leak, sagging line, insulation problem or traffic pattern can freeze again.</li></ol>
<div class="warn"><strong>Do not:</strong> add antifreeze, salt or septic additives; pump sewage onto the ground; light a fire over the system; or run water continuously to force a thaw. MPCA explicitly advises against these actions.</div>
<h2>If the drainfield or treatment area is frozen</h2><p>If the soil treatment area cannot accept effluent, simply thawing an upstream line may not restore service. A professional may recommend operating the tank temporarily as a holding tank and arranging pumping as it fills until natural thaw occurs. Reduce water use during this period. If wet or surfacing conditions continue after thaw, review the <a href="/guides/septic-drainfield-repair-replacement/">drainfield repair vs. replacement guide</a> and obtain a site-specific diagnosis.</p>
<h2>Special considerations by system type</h2><p>Systems with pumps, controls, pressure distribution or other mechanical components can have different freeze points and alarm behavior than a basic gravity system. If you are unsure what you own, start with the permit/as-built and the <a href="/guides/types-of-septic-systems/">types of septic systems guide</a>. Never bypass an alarm or assume a pump problem is only weather-related.</p>
<h2>Official sources</h2><ul><li><a rel="nofollow" href="{mpca}">Minnesota Pollution Control Agency — Don't let your septic system freeze</a></li><li><a rel="nofollow" href="{umn_freeze}">University of Minnesota Onsite Sewage Treatment Program — Freezing problems and septic systems</a></li><li><a rel="nofollow" href="{umn_seasonal}">University of Minnesota Onsite Sewage Treatment Program — Seasonal care</a></li></ul>
<p><em>SepticScope provides general homeowner information. Climate, local code, system design, groundwater conditions and manufacturer requirements can change the correct action for a particular property.</em></p>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    (out / "index.html").write_text(page, encoding="utf-8")

    hub = SITE / "guides" / "index.html"
    if hub.exists():
        text = hub.read_text(encoding="utf-8", errors="replace")
        if "/guides/septic-system-winter-care/" not in text:
            promo = '<section><h2>Winter septic care and frozen systems</h2><p>Cold-climate homeowners can use the <a href="/guides/septic-system-winter-care/">winter septic care and frozen-system guide</a> for evidence-grounded prevention, warning signs, safe response and winter pumping guidance.</p></section>'
            text = text.replace("</main>", promo + "</main>", 1) if "</main>" in text else text.replace("</body>", promo + "</body>", 1)
            hub.write_text(text, encoding="utf-8")

    sitemap = SITE / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        if canonical not in text:
            text = text.replace("</urlset>", f"<url><loc>{canonical}</loc><lastmod>2026-08-31</lastmod></url></urlset>")
            sitemap.write_text(text, encoding="utf-8")


atexit.register(_write_winter_guide)
