"""Generate a SepticScope septic-safe household use guide after the site build."""
from __future__ import annotations

import atexit
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
GA_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"


def _write_septic_safe_guide() -> None:
    if not SITE.is_dir():
        return

    out = SITE / "guides" / "what-not-to-flush-septic-system"
    out.mkdir(parents=True, exist_ok=True)
    canonical = "https://septicscope.com/guides/what-not-to-flush-septic-system/"
    epa_care = "https://www.epa.gov/septic/how-care-your-septic-system"
    epa_faq = "https://www.epa.gov/septic/frequent-questions-septic-systems"
    epa_smart = "https://www.epa.gov/septic/septicsmart"
    epa_meds = "https://www.epa.gov/household-medication-disposal/limited-role-food-and-drug-administrations-flush-list"

    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>What Not to Flush With a Septic System: Septic-Safe Guide | SepticScope</title>
<meta name="description" content="An EPA-grounded guide to what not to flush or pour down drains with a septic system, including wipes, grease, cleaners, medications, garbage disposals and additives.">
<link rel="canonical" href="{canonical}">
<style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:1000px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}main{{padding-top:42px;padding-bottom:70px}}.crumb{{font-size:.92rem;color:var(--muted)}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}}h2{{margin-top:1.9em}}a{{color:var(--accent)}}.card,.note{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}table{{width:100%;border-collapse:collapse;margin:18px 0}}th,td{{text-align:left;border-bottom:1px solid var(--line);padding:10px;vertical-align:top}}footer{{border-top:1px solid var(--line);color:var(--muted)}}@media(max-width:700px){{table{{display:block;overflow-x:auto}}}}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"What Not to Flush With a Septic System: Septic-Safe Guide","description":"EPA-grounded homeowner guidance on what should and should not enter a septic system.","mainEntityOfPage":"{canonical}","publisher":{{"@type":"Organization","name":"SepticScope"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"What can you safely flush with a septic system?","acceptedAnswer":{{"@type":"Answer","text":"EPA's simple rule is to flush only human waste and toilet paper. Items such as wipes, paper towels, hygiene products, diapers, cat litter and dental floss should not be flushed."}}}},{{"@type":"Question","name":"Are flushable wipes safe for septic systems?","acceptedAnswer":{{"@type":"Answer","text":"EPA lists wipes among items that should not be flushed into a septic system, including wipes marketed for household use."}}}},{{"@type":"Question","name":"Do septic tank additives help?","acceptedAnswer":{{"@type":"Answer","text":"EPA does not recommend septic tank additives for domestic wastewater treatment because normal systems already contain microorganisms needed for treatment and some additives can be ineffective or harmful."}}}},{{"@type":"Question","name":"Can a garbage disposal be used with septic?","acceptedAnswer":{{"@type":"Answer","text":"EPA says garbage disposal use can increase solids in the septic tank and may increase how often the tank needs pumping. Limiting disposal use reduces that additional solids load."}}}}]}}</script>
</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / What not to flush</div>
<h1>What not to flush with a septic system</h1>
<p>The simplest septic-safe rule is also the most useful: EPA says toilets should receive <strong>human waste and toilet paper only</strong>. Everything else adds clogging risk, unnecessary solids, chemical stress or contaminants that the system was not designed to handle.</p>
<div class="note"><strong>Quick answer:</strong> put wipes, paper towels, hygiene products, diapers, condoms, dental floss, cigarette butts, cat litter and similar trash in the trash—not the toilet. Keep grease, oils, paint, solvents, pesticides and other household chemicals out of drains. Use local disposal or take-back programs for materials that need special handling.</div>
<h2>Quick septic-safe decision table</h2><table><thead><tr><th>Item</th><th>Put it in septic?</th><th>Why</th></tr></thead><tbody>
<tr><td>Human waste and toilet paper</td><td><strong>Yes</strong></td><td>EPA identifies these as the appropriate materials to flush.</td></tr>
<tr><td>Wipes, including products marketed as flushable</td><td><strong>No</strong></td><td>They can contribute to clogs and do not belong in a septic toilet stream.</td></tr>
<tr><td>Paper towels, diapers, feminine hygiene products, condoms, floss, cat litter</td><td><strong>No</strong></td><td>These are trash rather than wastewater and can add persistent solids or blockages.</td></tr>
<tr><td>Cooking grease, fats and oils</td><td><strong>No</strong></td><td>EPA advises keeping grease and oils out of drains because they add problematic material to the tank and system.</td></tr>
<tr><td>Coffee grounds and food waste</td><td><strong>Avoid</strong></td><td>Food solids increase the material the tank must retain and can increase pumping needs.</td></tr>
<tr><td>Paint, solvents, pesticides, gasoline, antifreeze and similar chemicals</td><td><strong>No</strong></td><td>EPA warns that household chemicals can harm treatment biology and may reach groundwater.</td></tr>
<tr><td>Unused medications</td><td><strong>Usually no</strong></td><td>EPA and FDA prefer take-back options. A limited FDA flush list exists for specific medicines when take-back is unavailable, so follow current official medication-disposal guidance.</td></tr>
</tbody></table>
<h2>Are “flushable” wipes septic-safe?</h2><p>Do not treat a “flushable” label as permission to put wipes into a septic system. EPA's current homeowner-care guidance says to flush only human waste and toilet paper and lists wipes among materials that should not be flushed. That rule is easier to follow than trying to judge individual wipe brands.</p>
<h2>Can you use a garbage disposal with septic?</h2><p>EPA says garbage disposals can increase the amount of food solids entering the septic tank. Those solids can build up as sludge and scum and may require the tank to be pumped more often. If a home has a disposal, limiting its use is a practical way to reduce unnecessary solids loading.</p>
<h2>What about household cleaners?</h2><p>Normal household wastewater is expected, but septic systems are not hazardous-waste disposal systems. EPA specifically advises against sending large amounts of toxic cleaners, drain openers, paints, solvents, oils, pesticides and similar chemicals down drains. For a clog, EPA recommends mechanical approaches such as a drain snake rather than relying on chemical drain openers.</p>
<h2>Do septic additives or bacteria treatments help?</h2><p>EPA does <strong>not</strong> recommend septic tank additives for domestic wastewater treatment. Septic systems already contain bacteria, enzymes and other microorganisms involved in treatment, and EPA notes that marketed additives may be ineffective or can harm operation or the environment. If a system has odors, backups, alarms or poor performance, diagnose the cause instead of assuming an additive will fix it.</p>
<h2>Medication disposal is a special case</h2><p>For unwanted medicines, EPA and FDA prefer drug take-back or mail-back programs whenever available. FDA maintains a limited flush list for certain medicines when a take-back option is not available because accidental exposure can be dangerous. That is a medication-safety exception, not a general septic-care recommendation. Check current EPA/FDA instructions for the specific medicine.</p>
<h2>Water use matters too</h2><p>Septic care is not only about what goes down the drain; it is also about how much water arrives at once. EPA recommends water efficiency and spreading out high-water-use activities so the system is not unnecessarily overloaded. If your system already shows slow drains, gurgling, odors, standing water or sewage backup, see the <a href="/guides/septic-system-failure-signs/">septic failure warning-sign guide</a> instead of trying household treatments.</p>
<h2>Turn good habits into lower maintenance risk</h2><p>Keeping trash, grease and unnecessary solids out of the system can reduce avoidable load, but it does not eliminate normal maintenance. EPA still recommends routine inspection and pumping based on household use and system type. See the <a href="/guides/septic-pumping-cost/">pumping and maintenance guide</a>, compare <a href="/guides/types-of-septic-systems/">common septic system types</a>, or use the <a href="/counties/">county directory</a> to find local permitting and maintenance rules.</p>
<h2>Official sources</h2><ul><li><a rel="nofollow" href="{epa_care}">U.S. EPA — How to Care for Your Septic System</a></li><li><a rel="nofollow" href="{epa_faq}">U.S. EPA — Frequent Questions on Septic Systems</a></li><li><a rel="nofollow" href="{epa_smart}">U.S. EPA — SepticSmart</a></li><li><a rel="nofollow" href="{epa_meds}">U.S. EPA — Limited Role of the FDA Flush List</a></li></ul>
<p><em>SepticScope provides general homeowner information. Follow local regulations and current official disposal guidance when they are more specific.</em></p>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    (out / "index.html").write_text(page, encoding="utf-8")

    hub = SITE / "guides" / "index.html"
    if hub.exists():
        text = hub.read_text(encoding="utf-8", errors="replace")
        if "/guides/what-not-to-flush-septic-system/" not in text:
            promo = '<section><h2>What not to flush with septic</h2><p>Use the <a href="/guides/what-not-to-flush-septic-system/">septic-safe household use guide</a> for wipes, grease, cleaners, garbage disposals, medications and additives.</p></section>'
            text = text.replace("</main>", promo + "</main>", 1) if "</main>" in text else text.replace("</body>", promo + "</body>", 1)
            hub.write_text(text, encoding="utf-8")

    sitemap = SITE / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        if canonical not in text:
            text = text.replace("</urlset>", f"<url><loc>{canonical}</loc><lastmod>2026-08-31</lastmod></url></urlset>")
            sitemap.write_text(text, encoding="utf-8")


atexit.register(_write_septic_safe_guide)
