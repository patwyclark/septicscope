from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SITE = ROOT / 'site'
OUT = SITE / 'guides' / 'septic-tank-size-calculator'
OUT.mkdir(parents=True, exist_ok=True)
canonical = 'https://septicscope.com/guides/septic-tank-size-calculator/'

ga = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-F6RB8YERCM"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-F6RB8YERCM');</script>'''
ads = '''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8782868222380999" crossorigin="anonymous"></script>'''

faq = [
    ('Is septic tank size the same in every state?', 'No. Minimum tank capacity and design rules vary by jurisdiction. Use the calculator only as a planning reference and verify the current rule with the permitting authority for the property.'),
    ('Are septic tanks sized by bedrooms or people?', 'Many residential codes use bedroom count, but the exact rule is jurisdiction-specific. New York, Indiana and Washington each publish bedroom-based minimums, and their tables are not identical.'),
    ('Does this calculator size my drainfield?', 'No. Drainfield design depends on local rules and site conditions such as soil, groundwater, slope and design flow. This tool intentionally does not estimate drainfield area.'),
    ('Can I use the result for a permit application?', 'No. A permit-ready design must follow the current requirements of the authority having jurisdiction and may require a site evaluation or licensed designer.'),
]

schema = {
    '@context': 'https://schema.org',
    '@graph': [
        {
            '@type': 'Article',
            'headline': 'Septic Tank Size Calculator: Bedroom-Based Planning Guide',
            'description': 'Compare bedroom-based septic tank minimums from selected official state rules and learn why local verification is required.',
            'mainEntityOfPage': canonical,
            'publisher': {'@type': 'Organization', 'name': 'SepticScope'},
            'dateModified': '2026-08-31',
        },
        {
            '@type': 'FAQPage',
            'mainEntity': [
                {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                for q, a in faq
            ],
        },
    ],
}
faq_html = ''.join(f'<h3>{q}</h3><p>{a}</p>' for q, a in faq)

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Septic Tank Size Calculator by Bedrooms | SepticScope</title><meta name="description" content="Use this septic tank size planning calculator to compare official bedroom-based minimums in selected states, then verify your local permit requirements."><link rel="canonical" href="{canonical}">{ga}{ads}<script type="application/ld+json">{json.dumps(schema)}</script><style>:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,system-ui,sans-serif;color:var(--ink);line-height:1.65}}header{{border-bottom:1px solid var(--line)}}.nav,main,footer div{{max-width:960px;margin:auto;padding:20px 24px}}main{{padding-top:38px;padding-bottom:70px}}h1{{font-size:clamp(2rem,5vw,3.1rem);line-height:1.08}}h2{{margin-top:1.8em}}a{{color:var(--accent)}}.brand{{font-weight:800;color:var(--ink);text-decoration:none}}.card,.note{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}}label,select{{font-size:1rem}}select{{display:block;margin-top:8px;padding:10px;min-width:220px;max-width:100%}}.result{{font-size:1.15rem;font-weight:700;margin-top:14px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid var(--line);padding:10px;text-align:left}}th{{background:var(--panel)}}footer{{border-top:1px solid var(--line);color:var(--muted)}}</style></head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><p><a href="/guides/">← Septic guides</a></p><h1>Septic tank size calculator: start with bedrooms, finish with your local code</h1><p>Tank sizing looks simple until you compare actual state rules. Current search results often present one national bedroom chart, but official requirements differ. This tool shows that difference instead of pretending one formula works everywhere.</p><div class="note"><strong>Planning tool, not a permit design.</strong> Choose a state rule below to see the published minimum for a single-family residence. Always verify the current state/local rule and approved design before buying or installing a tank.</div><div class="card"><label for="state"><strong>Official rule set</strong></label><select id="state"><option value="ny">New York Appendix 75-A</option><option value="in">Indiana 410 IAC 6-8.3-60</option><option value="wa">Washington WAC 246-272A-0232</option></select><label for="beds" style="display:block;margin-top:16px"><strong>Bedrooms</strong></label><select id="beds">{''.join(f'<option>{n}</option>' for n in range(1, 11))}</select><div class="result" id="result" aria-live="polite"></div></div><script>const s=document.getElementById('state'),b=document.getElementById('beds'),r=document.getElementById('result');function calc(){{let n=+b.value,g;if(s.value==='ny')g=n<=3?1000:1000+(n-3)*250;else if(s.value==='in')g=n<=2?750:n===3?1000:n===4?1250:n===5?1500:1500+(n-5)*300;else g=n<=4?1000:1000+(n-4)*250;r.textContent='Published minimum under this selected state rule: '+g.toLocaleString()+' gallons.'}}s.onchange=b.onchange=calc;calc();</script><h2>Why the calculator changes by state</h2><table><tr><th>Rule</th><th>Published residential minimum pattern</th></tr><tr><td>New York Appendix 75-A</td><td>1–3 bedrooms: 1,000 gallons; 4: 1,250; 5: 1,500; 6: 1,750; then +250 gallons per additional bedroom.</td></tr><tr><td>Indiana 410 IAC 6-8.3-60</td><td>2 or fewer: 750 gallons; 3: 1,000; 4: 1,250; 5: 1,500; then +300 gallons per bedroom over five.</td></tr><tr><td>Washington WAC 246-272A-0232</td><td>Up to 4 bedrooms: 1,000 gallons; then +250 gallons per additional bedroom.</td></tr></table><p>The disagreement is the point: a generic web calculator cannot determine your legal minimum without knowing the applicable jurisdiction and project details.</p><h2>What bedroom count does—and does not—tell you</h2><p>Bedroom count is a common residential design input because it represents potential occupancy, but definitions can be broader than the rooms currently used for sleeping. Local rules can also impose tank construction, compartment, access, setback, treatment, site-evaluation and design-flow requirements. A larger tank does not make an unsuitable drainfield site suitable.</p><h2>Do not use a tank calculator to size the drainfield</h2><p>Soil absorption areas depend on site-specific conditions and local design standards. Soil characteristics, seasonal groundwater, slope, setbacks and approved design flow can materially change what is allowed. SepticScope therefore does not generate a nationwide drainfield square-footage number from an unsupported formula.</p><h2>How to turn this estimate into a permit-ready answer</h2><ol><li>Confirm the bedroom count used by the permitting authority.</li><li>Find the state and local septic rules for the property.</li><li>Retrieve existing permits or as-built records when replacing or evaluating an existing system.</li><li>Complete any required soil/site evaluation and professional design.</li><li>Use the approved design—not an online estimate—to order equipment.</li></ol><p>Start with <a href="/counties/">SepticScope's county directory</a> to find the relevant permitting authority. For repair planning, see the <a href="/guides/septic-drainfield-repair-replacement/">drainfield repair vs. replacement guide</a>.</p><h2>Frequently asked questions</h2>{faq_html}<h2>Official sources</h2><ul><li><a rel="nofollow" href="https://www.health.ny.gov/regulations/nycrr/title_10/part_75/appendix_75-a.htm">New York Department of Health — Appendix 75-A</a></li><li><a rel="nofollow" href="https://www.in.gov/health/eph/onsite-sewage-systems-program/historic-bulletins-and-rules">Indiana Department of Health — current and historic onsite sewage rules</a></li><li><a rel="nofollow" href="https://app.leg.wa.gov/WAC/default.aspx?cite=246-272A-0232">Washington State Legislature — WAC 246-272A-0232</a></li><li><a rel="nofollow" href="https://www.epa.gov/septic/septic-system-care-and-maintenance">U.S. EPA — Septic System Care and Maintenance</a></li></ul><p><em>SepticScope provides educational planning information. Current requirements of the permitting authority control.</em></p></main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''

(OUT / 'index.html').write_text(page, encoding='utf-8')

hub = SITE / 'guides' / 'index.html'
if hub.exists():
    t = hub.read_text(encoding='utf-8')
    if canonical.replace('https://septicscope.com', '') not in t:
        block = '<section><h2>Septic tank size calculator</h2><p>Compare bedroom-based minimum tank sizes from selected official state rules—and see why one national sizing chart can be misleading. <a href="/guides/septic-tank-size-calculator/">Use the septic tank size calculator →</a></p></section>'
        t = t.replace('</main>', block + '</main>', 1) if '</main>' in t else t.replace('</body>', block + '</body>', 1)
        hub.write_text(t, encoding='utf-8')

sm = SITE / 'sitemap.xml'
if sm.exists():
    t = sm.read_text(encoding='utf-8')
    if canonical not in t:
        t = t.replace('</urlset>', f'<url><loc>{canonical}</loc><lastmod>2026-08-31</lastmod></url></urlset>')
    sm.write_text(t, encoding='utf-8')

print('Added', canonical)
