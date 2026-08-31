from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
GUIDE_DIR = SITE / "guides" / "septic-drainfield-repair-replacement"
GUIDE_DIR.mkdir(parents=True, exist_ok=True)

canonical = "https://septicscope.com/guides/septic-drainfield-repair-replacement/"

ga = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-F6RB8YERCM"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-F6RB8YERCM');</script>'''
ads = '''<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8782868222380999" crossorigin="anonymous"></script>'''

faq = [
    ("Can a failed septic drainfield be repaired instead of replaced?", "Sometimes. The right fix depends on the cause. A service professional may find a blocked pipe, damaged distribution box, pump problem, hydraulic overload, or another repairable issue. A chronically saturated or unsuitable soil absorption area can require a larger redesign or replacement under local rules."),
    ("Will pumping the septic tank fix a drainfield problem?", "Pumping removes accumulated solids from the tank and is important maintenance, but it does not repair a clogged, damaged, undersized, or saturated drainfield. It can temporarily reduce system loading while the underlying cause is evaluated."),
    ("What are common signs of drainfield failure?", "EPA lists standing water or damp spots, sewage odors, unusually bright green or spongy grass, slow drains, gurgling, and sewage backups among common warning signs of septic-system malfunction."),
    ("Can I drive or park over a septic drainfield?", "EPA advises homeowners not to park or drive on the drainfield because compaction and physical damage can interfere with treatment and distribution."),
]

schema = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Article", "headline": "Septic Drainfield Repair vs. Replacement: What Homeowners Should Know", "description": "How to distinguish potentially repairable septic drainfield problems from situations that may require replacement, plus inspection, maintenance and permit considerations.", "mainEntityOfPage": canonical, "publisher": {"@type": "Organization", "name": "SepticScope"}, "dateModified": "2026-08-31"},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q,a in faq]}
    ]
}

faq_html = ''.join(f'<h3>{q}</h3><p>{a}</p>' for q,a in faq)

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Septic Drainfield Repair vs. Replacement | SepticScope</title>
<meta name="description" content="Learn when a septic drainfield problem may be repairable, when replacement may be necessary, warning signs, inspection steps, and permit considerations.">
<link rel="canonical" href="{canonical}">{ga}{ads}
<script type="application/ld+json">{json.dumps(schema)}</script>
<style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:960px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}main{{padding-top:38px;padding-bottom:70px}}h1{{font-size:clamp(2rem,5vw,3.1rem);line-height:1.08}}h2{{margin-top:1.8em}}h3{{margin-top:1.35em}}a{{color:var(--accent)}}.card,.note{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}table{{border-collapse:collapse;width:100%;margin:22px 0}}th,td{{text-align:left;vertical-align:top;border:1px solid var(--line);padding:12px}}th{{background:var(--panel)}}footer{{border-top:1px solid var(--line);color:var(--muted)}}@media(max-width:650px){{table,thead,tbody,tr,th,td{{display:block}}th{{margin-top:10px}}}}</style></head><body>
<header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<p><a href="/guides/">← Septic guides</a></p>
<h1>Septic drainfield repair vs. replacement: what homeowners should know</h1>
<p>A wet or smelly drainfield does not automatically mean the entire septic system needs to be replaced. It does mean the system should be evaluated promptly. The useful first question is <strong>what failed</strong>: a pipe, distribution component, pump, overloaded tank, or the soil absorption area itself.</p>
<div class="note"><strong>Safety first:</strong> Avoid contact with sewage or wastewater surfacing on the property. EPA notes that sewage can contain harmful pathogens. Reduce water use and contact a qualified septic professional and your local health or environmental agency when a malfunction is suspected.</div>
<h2>Signs the drainfield may be in trouble</h2>
<p>EPA identifies several warning signs of septic-system malfunction: standing water or damp areas over the tank or drainfield, sewage odors, unusually green or spongy grass, slow drains, gurgling plumbing, and sewage backups. These symptoms can overlap with plumbing or tank problems, so they are clues—not a remote diagnosis.</p>
<h2>Repairable problem or replacement project?</h2>
<table><thead><tr><th>What an inspection may find</th><th>Why it matters</th></tr></thead><tbody>
<tr><td>Blocked or damaged pipe</td><td>A localized conveyance problem may be repairable without rebuilding the full soil absorption area.</td></tr>
<tr><td>Distribution-box or flow imbalance</td><td>Unequal distribution can overload part of a field. EPA includes distribution-box condition and equal flow among items that may be evaluated during an inspection.</td></tr>
<tr><td>Pump, control, or electrical failure</td><td>Advanced or pressure-dosed systems can malfunction because of mechanical or electrical components rather than because the soil treatment area has failed.</td></tr>
<tr><td>Hydraulic overload</td><td>Excess water use or stormwater directed toward the field can reduce treatment performance. Correcting the water source may be part of the remedy.</td></tr>
<tr><td>Persistent ponding, unsuitable soil, high groundwater, or severe clogging</td><td>These conditions can point toward a larger redesign, replacement field, or alternative treatment approach, subject to local permitting and site evaluation.</td></tr>
</tbody></table>
<h2>Why pumping is not the same as repairing a drainfield</h2>
<p>Routine pumping protects the drainfield by keeping excessive solids from leaving the tank. EPA generally recommends pumping household tanks every three to five years, with actual frequency depending on tank size, household size, water use and solids accumulation. But pumping cannot rebuild damaged piping, restore unsuitable soil, or permanently correct a failed absorption area.</p>
<p>If the tank is overdue, pumping may still be part of the service visit. Treat a promise that pumping alone will "fix" a failing field as something to verify against an actual inspection.</p>
<h2>What should be checked before approving a full replacement</h2>
<ul><li>Tank condition, liquid levels, inlet and outlet piping, and evidence of backup or leakage.</li><li>Distribution box or other distribution components.</li><li>Pumps, alarms, controls and wiring where the system uses them.</li><li>Drain lines for blockage or collapse when camera inspection is appropriate.</li><li>The drainfield for surfacing, unequal drainage, ponding, groundwater impacts or other failure evidence.</li><li>Existing permits, as-built drawings, prior repairs and maintenance records.</li><li>Whether the local authority requires a site evaluation, repair permit, replacement permit, reserve area or engineered design.</li></ul>
<h2>What changes the cost</h2>
<p>There is no reliable single national price for every drainfield repair or replacement. Current consumer cost publishers show that scope, field size, system type, excavation, site access and local labor materially change the total. The more useful distinction is whether the contractor is pricing a localized repair or a permitted replacement/redesign.</p>
<p>Ask for a written scope that separates diagnosis, pumping if needed, excavation, components, soil/site evaluation, permit fees, restoration and any required final inspection. For broader budgeting context, see the <a href="/guides/septic-system-replacement-cost/">septic replacement cost guide</a>.</p>
<h2>How to reduce future drainfield stress</h2>
<p>EPA recommends keeping vehicles off the drainfield, keeping roof drains and other rainwater drainage away from it, spacing out high water-use activities, and maintaining the tank so solids do not migrate into the field. Tree placement also matters because roots can damage septic components.</p>
<h2>Check the local permit path before work begins</h2>
<p>Repair and replacement rules vary by state and local jurisdiction. Before excavation or system alteration, use <a href="/counties/">SepticScope's county directory</a> to locate the permitting authority and official sources for your area. If you are buying or selling a property, also review the <a href="/guides/buying-home-septic-system/">homebuyer septic checklist</a>.</p>
<h2>Frequently asked questions</h2>{faq_html}
<h2>Sources</h2><ul>
<li><a href="https://www.epa.gov/septic/resolving-septic-system-malfunctions" rel="nofollow">U.S. EPA — Resolving Septic System Malfunctions</a></li>
<li><a href="https://www.epa.gov/septic/how-care-your-septic-system" rel="nofollow">U.S. EPA — How to Care for Your Septic System</a></li>
<li><a href="https://www.epa.gov/septic/frequent-questions-septic-systems" rel="nofollow">U.S. EPA — Frequent Questions on Septic Systems</a></li>
</ul>
<p><em>SepticScope provides general educational information. Local health, environmental and permitting agencies control applicable requirements.</em></p>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''

(GUIDE_DIR / "index.html").write_text(page, encoding="utf-8")

hub = SITE / "guides" / "index.html"
if hub.exists():
    text = hub.read_text(encoding="utf-8")
    if "/guides/septic-drainfield-repair-replacement/" not in text:
        block = '<section><h2>Drainfield repair or replacement?</h2><p>Learn which septic drainfield problems may be localized repairs, what can point toward replacement, and what should be inspected before approving major work. <a href="/guides/septic-drainfield-repair-replacement/">Read the drainfield repair vs. replacement guide →</a></p></section>'
        text = text.replace('</main>', block + '</main>', 1) if '</main>' in text else text.replace('</body>', block + '</body>', 1)
        hub.write_text(text, encoding="utf-8")

# Add contextually relevant links from existing national guides when those pages exist.
for rel, anchor in [
    ("guides/signs-septic-system-failure/index.html", '<p><strong>Drainfield-specific problem?</strong> See <a href="/guides/septic-drainfield-repair-replacement/">how to distinguish potential drainfield repairs from replacement scenarios</a>.</p>'),
    ("guides/septic-system-replacement-cost/index.html", '<p>Before assuming the entire system must be replaced, review the <a href="/guides/septic-drainfield-repair-replacement/">drainfield repair vs. replacement guide</a>.</p>')
]:
    path = SITE / rel
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if "/guides/septic-drainfield-repair-replacement/" not in text:
            text = text.replace('</main>', anchor + '</main>', 1) if '</main>' in text else text
            path.write_text(text, encoding="utf-8")

sitemap = SITE / "sitemap.xml"
if sitemap.exists():
    sm = sitemap.read_text(encoding="utf-8")
    if canonical not in sm:
        entry = f'<url><loc>{canonical}</loc><lastmod>2026-08-31</lastmod></url>'
        sm = sm.replace('</urlset>', entry + '</urlset>')
        sitemap.write_text(sm, encoding="utf-8")

print(f"Added {canonical}")
