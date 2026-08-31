"""Generate the SepticScope septic failure troubleshooting guide after the site build."""
from __future__ import annotations

import atexit
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
GA_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"


def _write_failure_guide() -> None:
    if not SITE.is_dir():
        return
    d = SITE / "guides" / "septic-system-failure-signs"
    d.mkdir(parents=True, exist_ok=True)
    canonical = "https://septicscope.com/guides/septic-system-failure-signs/"
    epa_fail = "https://www.epa.gov/septic/resolving-septic-system-malfunctions"
    epa_care = "https://www.epa.gov/septic/how-care-your-septic-system"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>7 Signs of Septic System Failure: What to Do Next | SepticScope</title>
<meta name="description" content="Learn the common signs of septic system failure, what each symptom can mean, when to stop using water, and when pumping alone may not solve the problem.">
<link rel="canonical" href="{canonical}">
<style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:1000px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}main{{padding-top:42px;padding-bottom:70px}}.crumb{{font-size:.92rem;color:var(--muted)}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}}h2{{margin-top:1.9em}}a{{color:var(--accent)}}.card,.warning{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}table{{width:100%;border-collapse:collapse;margin:18px 0}}th,td{{text-align:left;border-bottom:1px solid var(--line);padding:10px;vertical-align:top}}footer{{border-top:1px solid var(--line);color:var(--muted)}}@media(max-width:700px){{table{{display:block;overflow-x:auto}}}}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"7 Signs of Septic System Failure: What to Do Next","description":"A homeowner troubleshooting guide to common septic failure symptoms and practical next steps.","mainEntityOfPage":"{canonical}","publisher":{{"@type":"Organization","name":"SepticScope"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"What are the most common signs of septic system failure?","acceptedAnswer":{{"@type":"Answer","text":"EPA lists sewage backups, very slow drains, plumbing gurgling, standing water or damp areas over the tank or drainfield, sewage odors, and unusually bright green or spongy grass over the septic area among common warning signs."}}}},{{"@type":"Question","name":"Will pumping fix a failing septic system?","acceptedAnswer":{{"@type":"Answer","text":"Not necessarily. Pumping removes accumulated tank contents, but symptoms can also involve pipes, pumps, controls, the distribution system, drainfield or site conditions. A professional diagnosis is appropriate when failure signs are present."}}}},{{"@type":"Question","name":"What should I do if sewage backs up into my home?","acceptedAnswer":{{"@type":"Answer","text":"Avoid contact with sewage, reduce wastewater use, and contact a septic professional and the local health or regulatory agency for guidance. EPA warns that sewage can contain harmful pathogens."}}}}]}}</script>
</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / Septic failure signs</div>
<h1>7 signs of septic system failure—and what to do next</h1>
<p>One slow sink is not automatically a failed septic system. But several household and yard symptoms are recognized by the U.S. EPA as warning signs of a malfunction. The useful question is not just “does it need pumping?” but whether the problem is in the house plumbing, tank, pump and controls, distribution components, or drainfield.</p>
<div class="warning"><strong>Sewage backing up indoors:</strong> avoid contact with sewage because it may contain harmful pathogens. Reduce wastewater use and contact a qualified septic professional. EPA also advises contacting your local health department or regulatory agency for guidance.</div>
<h2>Quick symptom checker</h2><table><thead><tr><th>What you notice</th><th>Why it matters</th><th>Useful next step</th></tr></thead><tbody>
<tr><td>Sewage or wastewater backing up</td><td>EPA identifies backup from toilets, drains and sinks as a failure sign.</td><td>Limit water use, avoid sewage contact and arrange professional diagnosis promptly.</td></tr>
<tr><td>Several drains are very slow</td><td>Whole-house slow drainage can point beyond a single clogged fixture.</td><td>Note which fixtures are affected and whether gurgling or yard symptoms occur too.</td></tr>
<tr><td>Gurgling plumbing</td><td>EPA includes gurgling among common malfunction signs.</td><td>Do not assume the cause; have the plumbing and onsite system evaluated if it persists.</td></tr>
<tr><td>Standing water or damp soil</td><td>Wet areas near the tank or drainfield can indicate surfacing wastewater or hydraulic trouble.</td><td>Keep people and pets away and call a professional; avoid driving over the area.</td></tr>
<tr><td>Sewage odor</td><td>Odor near the tank or drainfield can accompany a problem, although EPA notes some odors can come from normal venting.</td><td>Look for other symptoms and have persistent or strong odors investigated.</td></tr>
<tr><td>Bright green, spongy grass</td><td>Unusually lush growth over the septic area during dry weather is an EPA-listed warning sign.</td><td>Do not dig into or compact the area; arrange an evaluation.</td></tr>
<tr><td>Pump or high-water alarm</td><td>Advanced systems may depend on pumps, floats, controls and electrical equipment.</td><td>Reduce water use and follow the system's service instructions; do not disable the alarm.</td></tr>
</tbody></table>
<h2>Does a slow drain mean the septic system is failing?</h2><p>Not by itself. A localized clog can make one fixture drain slowly. Concern increases when multiple fixtures are slow, toilets or sinks gurgle, wastewater backs up, or the yard shows wet or unusually lush areas over the onsite system. Those combinations justify a septic-system evaluation rather than repeated drain clearing alone.</p>
<h2>Will pumping fix the problem?</h2><p>Sometimes a tank is overdue for service, but pumping is not a universal repair. EPA explains that poor maintenance can allow solids to migrate toward the drainfield and contribute to clogging. A malfunction can also involve inadequate site conditions, damaged components, pumps or controls, distribution problems, or the drainfield itself. Pumping removes tank contents; it does not rebuild a failed drainfield.</p>
<p>If you are planning routine service rather than diagnosing a malfunction, use the <a href="/guides/septic-pumping-cost/">septic pumping cost and maintenance guide</a>. If a professional identifies a major failure, the <a href="/guides/septic-system-replacement-cost/">repair vs. replacement guide</a> explains the scope and cost drivers to clarify before approving work.</p>
<h2>What to do while waiting for service</h2><div class="card"><ul><li>Reduce water use so you are not adding unnecessary hydraulic load.</li><li>Avoid contact with sewage or surfaced wastewater and keep children and pets away.</li><li>Do not drive or park vehicles over the tank or drainfield.</li><li>Write down when symptoms began and which fixtures or yard areas are affected.</li><li>Find your septic permit or as-built drawing so the professional knows the approved system type and layout.</li><li>If you have an advanced system, locate its service records and alarm/control information.</li></ul></div>
<h2>How to prevent repeat problems</h2><p>EPA's current homeowner guidance says the average household system should be inspected at least every three years and household tanks are typically pumped every three to five years. Systems with electrical float switches, pumps or mechanical components generally need more frequent inspection. Water efficiency, keeping inappropriate waste out of drains, and protecting the drainfield are also core maintenance practices.</p>
<h2>Find the local agency and your septic records</h2><p>Septic requirements are state and local. Use the <a href="/counties/">SepticScope county directory</a> to find the responsible permitting authority and available records resources. Your permit or as-built drawing can identify the system type, design flow and layout that a service provider may need. You can also review the <a href="/guides/types-of-septic-systems/">septic system types guide</a> before discussing repairs.</p>
<h2>Official sources</h2><ul><li><a rel="nofollow" href="{epa_fail}">U.S. EPA — Resolving Septic System Malfunctions</a></li><li><a rel="nofollow" href="{epa_care}">U.S. EPA — How to Care for Your Septic System</a></li></ul>
<p><em>This guide is general homeowner information, not a site diagnosis. Local rules, permit conditions and a qualified professional's site-specific findings control.</em></p>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    (d / "index.html").write_text(page, encoding="utf-8")
    hub = SITE / "guides" / "index.html"
    if hub.exists():
        text = hub.read_text(encoding="utf-8", errors="replace")
        if "/guides/septic-system-failure-signs/" not in text:
            promo = '<section><h2>Septic system failure signs</h2><p>Seeing slow drains, gurgling, odors or wet ground? Use the <a href="/guides/septic-system-failure-signs/">septic failure symptom checker</a> to understand the warning signs and next steps.</p></section>'
            text = text.replace("</main>", promo + "</main>", 1) if "</main>" in text else text.replace("</body>", promo + "</body>", 1)
            hub.write_text(text, encoding="utf-8")
    sitemap = SITE / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        if canonical not in text:
            text = text.replace("</urlset>", f"<url><loc>{canonical}</loc><lastmod>2026-08-31</lastmod></url></urlset>")
            sitemap.write_text(text, encoding="utf-8")


atexit.register(_write_failure_guide)
