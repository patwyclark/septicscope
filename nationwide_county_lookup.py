# Nationwide county/county-equivalent lookup layer.
# Detailed septic facts are never inferred: unresearched locations become clearly labeled lookup pages.
import base64, gzip, json

DATA_DIR=ROOT/'nationwide_data'
payload=''.join((DATA_DIR/f'part{i:02d}.txt').read_text(encoding='utf-8').strip() for i in range(8))
rows=json.loads(gzip.decompress(base64.b64decode(payload,validate=True)).decode('utf-8'))
if len(rows)!=3144 or len({r[3] for r in rows})!=3144:
    raise RuntimeError(f'Nationwide county dataset integrity failure: {len(rows)} rows')

STATE_NAMES={'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado','CT':'Connecticut','DE':'Delaware','DC':'District of Columbia','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':'Idaho','IL':'Illinois','IN':'Indiana','IA':'Iowa','KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan','MN':'Minnesota','MS':'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina','ND':'North Dakota','OH':'Ohio','OK':'Oklahoma','OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont','VA':'Virginia','WA':'Washington','WV':'West Virginia','WI':'Wisconsin','WY':'Wyoming'}
CENSUS_SOURCE='https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.2025.html'
LOCAL_GOV='https://www.usa.gov/state-local-governments'
EPA='https://www.epa.gov/septic'

def display_name(name,lsad):
    if not lsad: return name
    if lsad=='CA': lsad='Census Area'
    return name if lsad.lower() in name.lower() else f'{name} {lsad}'

def county_slug_name(name,lsad):
    return slugify(name)

counties_root=OUTPUT/'counties'; counties_root.mkdir(parents=True,exist_ok=True)
verified=set()
for state_dir in counties_root.iterdir():
    if state_dir.is_dir():
        for county_dir in state_dir.iterdir():
            if county_dir.is_dir() and (county_dir/'index.html').exists():
                verified.add((state_dir.name,county_dir.name))

by_state={}; fallback_count=0
for abbr,name,lsad,fips in rows:
    state=STATE_NAMES[abbr]; state_slug=slugify(state); county_slug=county_slug_name(name,lsad)
    display=display_name(name,lsad)
    status='verified' if (state_slug,county_slug) in verified else 'lookup'
    by_state.setdefault((state,state_slug),[]).append((display,county_slug,status,fips))
    if status=='verified': continue
    fallback_count+=1
    canonical=f'https://septicscope.com/counties/{state_slug}/{county_slug}/'
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(display)} {html.escape(state)} Septic Information | SepticScope</title><meta name="description" content="County lookup page for {html.escape(display)}, {html.escape(state)} with official-government starting points while SepticScope verifies local septic permitting requirements."><link rel="canonical" href="{canonical}"><style>{COMMON_STYLE}</style>{ga_tag}{adsense_tag}</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><div class="crumb"><a href="/">Home</a> / <a href="/counties/">Counties</a> / <a href="/counties/{state_slug}/">{html.escape(state)}</a> / {html.escape(display)}</div><p><span class="verified" style="background:#fff5df;color:#765400">Local septic rules not yet verified</span></p><h1>{html.escape(display)}, {html.escape(state)} septic information</h1><div class="note"><strong>This is a lookup page, not a verified permit guide.</strong> SepticScope has not yet independently confirmed the local permitting authority or county-specific septic requirements for this location. Do not rely on this page as permit instructions.</div><h2>Official government starting points</h2><ul><li><a href="{LOCAL_GOV}" rel="nofollow">USA.gov — find state and local government offices</a></li><li><a href="{CENSUS_SOURCE}" rel="nofollow">U.S. Census Bureau — county and county-equivalent geography</a></li><li><a href="{EPA}" rel="nofollow">U.S. EPA — septic system information</a></li></ul><h2>What to verify locally</h2><p>Use the official local-government directory to identify the county, parish, borough, planning-region, city, or health/environmental office responsible for onsite wastewater. Confirm permit requirements, site or soil evaluation rules, installer licensing, setbacks, repair permits, inspections, fees, and any operating or maintenance requirements directly with that agency.</p><p>SepticScope will replace this lookup page with a sourced local guide after the permitting authority and county-specific requirements are verified.</p></main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    out=counties_root/state_slug/county_slug; out.mkdir(parents=True,exist_ok=True); (out/'index.html').write_text(page,encoding='utf-8')

for (state,state_slug),items in sorted(by_state.items()):
    lis=[]
    for display,county_slug,status,fips in sorted(items,key=lambda x:x[0]):
        badge='Verified guide' if status=='verified' else 'Lookup page'
        lis.append(f'<li data-search="{html.escape((display+" "+state).lower())}"><a href="/counties/{state_slug}/{county_slug}/">{html.escape(display)}</a> <small>— {badge}</small></li>')
    n_verified=sum(1 for x in items if x[2]=='verified')
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(state)} Septic County Lookup | SepticScope</title><meta name="description" content="Browse every Census county or county-equivalent in {html.escape(state)}. Verified SepticScope guides are distinguished from unverified lookup pages."><link rel="canonical" href="https://septicscope.com/counties/{state_slug}/"><style>{COMMON_STYLE}</style>{ga_tag}{adsense_tag}</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><p><a href="/counties/">← All states</a></p><h1>{html.escape(state)} septic county lookup</h1><p>Every U.S. Census county or county-equivalent in {html.escape(state)} is listed below. <strong>{n_verified}</strong> currently have locally verified SepticScope septic guides; remaining locations have lookup pages with official-government starting points while local rules are researched.</p><input class="county-filter" type="search" placeholder="Filter counties" aria-label="Filter counties" style="width:100%;padding:14px;border:1px solid #ccd6d3;border-radius:10px;font-size:1rem"><ul class="grid county-list">{''.join(lis)}</ul></main><footer><div>© 2026 SepticScope</div></footer><script>const q=document.querySelector('.county-filter');q&&q.addEventListener('input',()=>{{const v=q.value.toLowerCase();document.querySelectorAll('[data-search]').forEach(x=>x.style.display=x.dataset.search.includes(v)?'':'none')}});</script></body></html>'''
    d=counties_root/state_slug; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(page,encoding='utf-8')

all_lis=[]
for (state,state_slug),items in sorted(by_state.items()):
    for display,county_slug,status,fips in sorted(items,key=lambda x:x[0]):
        badge='Verified' if status=='verified' else 'Lookup'
        all_lis.append(f'<li data-search="{html.escape((display+" "+state).lower())}"><a href="/counties/{state_slug}/{county_slug}/">{html.escape(display)}, {html.escape(state)}</a> <small>— {badge}</small></li>')
count=len(rows)
index=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>U.S. Septic County Lookup | SepticScope</title><meta name="description" content="Search all {count:,} U.S. counties and county equivalents. Verified septic guides use official local sources; other locations provide government lookup links while local rules are researched."><link rel="canonical" href="https://septicscope.com/counties/"><style>{COMMON_STYLE}</style>{ga_tag}{adsense_tag}</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><h1>Nationwide septic county lookup</h1><p>Search all <strong>{count:,}</strong> counties and county equivalents in the 50 states and District of Columbia. Detailed pages are marked <strong>Verified</strong> only after SepticScope checks authoritative local/state sources. All other locations remain searchable as clearly labeled lookup pages without speculative permit claims.</p><input class="county-filter" type="search" placeholder="Search county and state" aria-label="Search county and state" style="width:100%;padding:14px;border:1px solid #ccd6d3;border-radius:10px;font-size:1rem"><p><strong>{len(verified)}</strong> locally researched county pages are currently in the build; verification continues county by county.</p><ul class="grid county-list">{''.join(all_lis)}</ul></main><footer><div>© 2026 SepticScope</div></footer><script>const q=document.querySelector('.county-filter');q&&q.addEventListener('input',()=>{{const v=q.value.toLowerCase();document.querySelectorAll('[data-search]').forEach(x=>x.style.display=x.dataset.search.includes(v)?'':'none')}});</script></body></html>'''
(counties_root/'index.html').write_text(index,encoding='utf-8')

home=OUTPUT/'index.html'
if home.exists():
    t=home.read_text(encoding='utf-8')
    t=t.replace('Indiana launch','Nationwide county lookup')
    t=t.replace('Five Indiana counties are live in the launch build.',f'Search all {count:,} U.S. counties and county equivalents. Verified guides use official local sources; other counties provide official-government lookup links while we research local septic rules.')
    t=t.replace('Verified county septic guides','Nationwide septic county lookup')
    cta='<p style="margin:24px 0"><a href="/counties/" style="display:inline-block;padding:13px 18px;border-radius:10px;background:#176b5b;color:white;text-decoration:none;font-weight:700">Search all U.S. counties →</a></p>'
    if 'Search all U.S. counties →' not in t:
        marker=f'Search all {count:,} U.S. counties and county equivalents.'; pos=t.find(marker)
        if pos!=-1:
            end=t.find('</p>',pos)
            if end!=-1: t=t[:end+4]+cta+t[end+4:]
    home.write_text(t,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8'); entries=[]
    for (state,state_slug),items in by_state.items():
        u=f'https://septicscope.com/counties/{state_slug}/'
        if u not in sm: entries.append(f'<url><loc>{u}</loc><lastmod>2026-08-29</lastmod></url>')
        for display,county_slug,status,fips in items:
            u=f'https://septicscope.com/counties/{state_slug}/{county_slug}/'
            if u not in sm: entries.append(f'<url><loc>{u}</loc><lastmod>2026-08-29</lastmod></url>')
    if entries: sitemap.write_text(sm.replace('</urlset>',''.join(entries)+'</urlset>'),encoding='utf-8')
print(f'Nationwide lookup complete: {count} counties/equivalents; {fallback_count} fallback lookup pages; {len(verified)} pre-existing verified pages detected')
