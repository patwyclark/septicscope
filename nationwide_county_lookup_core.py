# Nationwide county/county-equivalent lookup layer.
# Detailed septic facts are never inferred: unresearched locations remain useful help pages
# while verified county guides use locally sourced information.
import base64, gzip, json
import xml.etree.ElementTree as ET

DATA_DIR = ROOT / 'nationwide_data'
payload = ''.join((DATA_DIR / f'part{i:02d}.txt').read_text(encoding='utf-8').strip() for i in range(8))
rows = json.loads(gzip.decompress(base64.b64decode(payload, validate=True)).decode('utf-8'))
if len(rows) != 3144 or len({r[3] for r in rows}) != 3144:
    raise RuntimeError(f'Nationwide county dataset integrity failure: {len(rows)} rows')

STATE_NAMES = {
    'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado',
    'CT':'Connecticut','DE':'Delaware','DC':'District of Columbia','FL':'Florida','GA':'Georgia',
    'HI':'Hawaii','ID':'Idaho','IL':'Illinois','IN':'Indiana','IA':'Iowa','KS':'Kansas',
    'KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan',
    'MN':'Minnesota','MS':'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada',
    'NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina',
    'ND':'North Dakota','OH':'Ohio','OK':'Oklahoma','OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island',
    'SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont',
    'VA':'Virginia','WA':'Washington','WV':'West Virginia','WI':'Wisconsin','WY':'Wyoming'
}

LOCAL_GOV = 'https://www.usa.gov/state-local-governments'
EPA_STATE_CONTACTS = 'https://www.epa.gov/septic/state-septic-system-program-contacts'
EPA = 'https://www.epa.gov/septic'


def display_name(name, lsad):
    if not lsad:
        return name
    if lsad == 'CA':
        lsad = 'Census Area'
    return name if lsad.lower() in name.lower() else f'{name} {lsad}'


def county_slug_name(name, lsad):
    return slugify(name)


counties_root = OUTPUT / 'counties'
counties_root.mkdir(parents=True, exist_ok=True)

# Expansion scripts run before this layer. Any county page that already exists at this
# point is a researched guide and must never be overwritten by a generic help page.
verified = set()
for state_dir in counties_root.iterdir():
    if not state_dir.is_dir():
        continue
    for county_dir in state_dir.iterdir():
        if county_dir.is_dir() and (county_dir / 'index.html').exists():
            verified.add((state_dir.name, county_dir.name))

by_state = {}
fallback_count = 0
fallback_urls = set()
verified_urls = set()
search_rows = []

for abbr, name, lsad, fips in rows:
    state = STATE_NAMES[abbr]
    state_slug = slugify(state)
    county_slug = county_slug_name(name, lsad)
    display = display_name(name, lsad)
    status = 'verified' if (state_slug, county_slug) in verified else 'lookup'
    by_state.setdefault((state, state_slug), []).append((display, county_slug, status, fips))
    canonical = f'https://septicscope.com/counties/{state_slug}/{county_slug}/'
    search_rows.append({'n': display, 's': state, 'u': f'/counties/{state_slug}/{county_slug}/', 'v': status == 'verified'})

    if status == 'verified':
        verified_urls.add(canonical)
        continue

    fallback_count += 1
    fallback_urls.add(canonical)
    state_help = f'https://www.usa.gov/states/{state_slug}'
    safe_display = html.escape(display)
    safe_state = html.escape(state)

    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{safe_display} {safe_state} Septic Help & Official Contacts | SepticScope</title>
<meta name="description" content="Find official government starting points for septic permits and onsite wastewater help in {safe_display}, {safe_state}, while SepticScope completes its local source review.">
<meta name="robots" content="noindex,follow"><link rel="canonical" href="{canonical}"><style>{COMMON_STYLE}</style>{ga_tag}{adsense_tag}</head><body>
<header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<div class="crumb"><a href="/">Home</a> / <a href="/counties/">Counties</a> / <a href="/counties/{state_slug}/">{safe_state}</a> / {safe_display}</div>
<p><span class="verified" style="background:#eef5ff;color:#315a7d">Local guide in progress</span></p>
<h1>{safe_display}, {safe_state} septic help</h1>
<div class="note"><strong>We’re still source-checking the county-specific septic details for this location.</strong> You do not have to wait for our full guide to get help. The official links below can take you to state and local government resources now. Before starting septic work, confirm permits, site or soil evaluations, setbacks, fees and inspections with the agency that serves your property.</div>
<h2>Get official local help</h2>
<div class="card"><ul>
<li><a href="{state_help}" rel="nofollow">{safe_state} government directory on USA.gov</a> — includes the official state website, agencies and local-government resources.</li>
<li><a href="{LOCAL_GOV}" rel="nofollow">USA.gov state and local government directory</a> — use this to find county, city and local public offices.</li>
<li><a href="{EPA_STATE_CONTACTS}" rel="nofollow">EPA state septic program contacts</a> — find the state-level onsite wastewater program or contact.</li>
<li><a href="{EPA}" rel="nofollow">U.S. EPA septic guidance</a> — homeowner information on septic systems, care and common questions.</li>
</ul></div>
<h2>What to ask the local office</h2>
<p>Ask which agency handles onsite wastewater for the property and confirm whether you need a construction or repair permit, a soil or site evaluation, a licensed designer or installer, minimum setbacks, inspections, operating permits or maintenance agreements, and the current fees.</p>
<h2>While we finish this local guide</h2>
<p>You can also use our <a href="/faq/">septic FAQs</a> and <a href="/guides/">homeowner guides</a> for general septic information. SepticScope will automatically replace this page with a source-checked local guide as soon as the county-specific research is complete.</p>
<p><a href="/counties/{state_slug}/">← Browse all {safe_state} counties</a></p>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    out = counties_root / state_slug / county_slug
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(page, encoding='utf-8')

# State hubs stay indexable and make the distinction between researched guides and
# in-progress help pages clear without treating unfinished counties like dead ends.
state_cards = []
for (state, state_slug), items in sorted(by_state.items()):
    lis = []
    for display, county_slug, status, fips in sorted(items, key=lambda x: x[0]):
        badge = 'Verified guide' if status == 'verified' else 'Official help links'
        badge_style = 'color:#0f5548;font-weight:700' if status == 'verified' else 'color:#5b6672'
        lis.append(
            f'<li data-search="{html.escape((display + " " + state).lower())}">'
            f'<a href="/counties/{state_slug}/{county_slug}/">{html.escape(display)}</a> '
            f'<small style="{badge_style}">— {badge}</small></li>'
        )
    n_verified = sum(1 for x in items if x[2] == 'verified')
    state_cards.append((state, state_slug, len(items), n_verified))
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(state)} Septic Guides & County Help | SepticScope</title>
<meta name="description" content="Browse septic information for every county or county-equivalent in {html.escape(state)}. Source-checked local guides are clearly identified, with official government help links for counties still being researched.">
<link rel="canonical" href="https://septicscope.com/counties/{state_slug}/"><style>{COMMON_STYLE}</style>{ga_tag}{adsense_tag}</head><body>
<header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><p><a href="/counties/">← All states</a></p>
<h1>{html.escape(state)} septic information by county</h1>
<p>Choose your county below. <strong>{n_verified}</strong> currently have source-checked local SepticScope guides. Counties still being researched remain useful: their pages connect you with official government resources so you can get local assistance now.</p>
<div class="note"><strong>How to read the list:</strong> “Verified guide” means we checked authoritative local or state sources for that county. “Official help links” means the county-specific guide is still in progress, but the page provides government directories and septic-program contacts.</div>
<input class="county-filter" type="search" placeholder="Filter {html.escape(state)} counties" aria-label="Filter counties" style="width:100%;padding:14px;border:1px solid #ccd6d3;border-radius:10px;font-size:1rem">
<ul class="grid county-list">{''.join(lis)}</ul></main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a></div></footer>
<script>const q=document.querySelector('.county-filter');q&&q.addEventListener('input',()=>{{const v=q.value.toLowerCase();document.querySelectorAll('[data-search]').forEach(x=>x.style.display=x.dataset.search.includes(v)?'':'none')}});</script></body></html>'''
    d = counties_root / state_slug
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(page, encoding='utf-8')

# National directory: keep the initial DOM small. State cards are immediately useful,
# while county search dynamically renders only the matching results.
state_card_html = ''.join(
    f'<article class="card"><h2 style="margin-top:0"><a href="/counties/{slug}/">{html.escape(state)}</a></h2>'
    f'<p><strong>{verified_count}</strong> verified guides · {total} counties/equivalents</p>'
    f'<p><a href="/counties/{slug}/">Browse {html.escape(state)} →</a></p></article>'
    for state, slug, total, verified_count in state_cards
)
search_json = json.dumps(search_rows, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
count = len(rows)
index = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>U.S. Septic County Lookup & Local Guides | SepticScope</title>
<meta name="description" content="Search all {count:,} U.S. counties and county equivalents for verified septic guides or official government help links while local research is completed.">
<link rel="canonical" href="https://septicscope.com/counties/"><style>{COMMON_STYLE}.state-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}}#county-results{{list-style:none;padding:0}}#county-results li{{padding:12px 0;border-bottom:1px solid var(--line)}}.search-status{{color:var(--muted);font-size:.95rem}}</style>{ga_tag}{adsense_tag}</head><body>
<header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main>
<h1>Find septic information for your county</h1>
<p>SepticScope covers all <strong>{count:,}</strong> U.S. counties and county equivalents. We currently have <strong>{len(verified)}</strong> source-checked local guides, and we keep every other county useful with official government help links while its local septic rules are researched.</p>
<label for="county-search"><strong>Search county and state</strong></label>
<input id="county-search" type="search" placeholder="Example: Denton County Texas" autocomplete="off" style="width:100%;padding:15px;border:1px solid #ccd6d3;border-radius:10px;font-size:1rem;margin-top:8px">
<p id="search-status" class="search-status">Start typing a county or state, or browse by state below.</p><ul id="county-results"></ul>
<h2>Browse by state</h2><div class="state-grid">{state_card_html}</div>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer>
<script>const rows={search_json};const q=document.getElementById('county-search'),out=document.getElementById('county-results'),status=document.getElementById('search-status');function render(){{const v=q.value.trim().toLowerCase();out.innerHTML='';if(v.length<2){{status.textContent='Start typing a county or state, or browse by state below.';return}}const found=rows.filter(x=>(x.n+' '+x.s).toLowerCase().includes(v)).slice(0,50);status.textContent=found.length?(found.length===50?'Showing the first 50 matches':`Showing ${{found.length}} match${{found.length===1?'':'es'}}`):'No matching county found. Try the county name, state name, or browse by state.';for(const x of found){{const li=document.createElement('li'),a=document.createElement('a'),small=document.createElement('small');a.href=x.u;a.textContent=x.n+', '+x.s;small.textContent=x.v?' — Verified guide':' — Official help links';small.style.color=x.v?'#0f5548':'#5b6672';li.append(a,small);out.append(li)}}}}q.addEventListener('input',render);</script></body></html>'''
(counties_root / 'index.html').write_text(index, encoding='utf-8')

# Keep the homepage nationwide CTA accurate without rewriting its established visual design.
home = OUTPUT / 'index.html'
if home.exists():
    t = home.read_text(encoding='utf-8')
    t = t.replace('Local septic rules not yet verified', 'Local guide in progress')
    if 'Search all U.S. counties →' not in t:
        cta = '<p style="margin:24px 0"><a href="/counties/" style="display:inline-block;padding:13px 18px;border-radius:10px;background:#176b5b;color:white;text-decoration:none;font-weight:700">Search all U.S. counties →</a></p>'
        marker = '</header>'
        if marker in t:
            t = t.replace(marker, marker + cta, 1)
    home.write_text(t, encoding='utf-8')

# Search engines should index the national/state directories and researched county guides,
# not thousands of intentionally unfinished help pages. Remove fallback county URLs from
# the sitemap and ensure all indexable county/state pages are present.
sitemap = OUTPUT / 'sitemap.xml'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', NS)
if sitemap.exists():
    tree = ET.parse(sitemap)
    root = tree.getroot()
else:
    root = ET.Element(f'{{{NS}}}urlset')
    tree = ET.ElementTree(root)

existing = {}
for node in list(root):
    loc = node.find(f'{{{NS}}}loc')
    if loc is None or not loc.text:
        continue
    url = loc.text.strip()
    if url in fallback_urls:
        root.remove(node)
    else:
        existing[url] = node

wanted = {'https://septicscope.com/counties/'} | verified_urls
wanted |= {f'https://septicscope.com/counties/{state_slug}/' for state, state_slug in by_state}
for url in sorted(wanted):
    if url in existing:
        continue
    u = ET.SubElement(root, f'{{{NS}}}url')
    ET.SubElement(u, f'{{{NS}}}loc').text = url
    ET.SubElement(u, f'{{{NS}}}lastmod').text = '2026-08-30'

tree.write(sitemap, encoding='utf-8', xml_declaration=True)
print(f'Nationwide lookup complete: {count} counties/equivalents; {fallback_count} friendly noindex help pages; {len(verified)} verified county guides detected')
