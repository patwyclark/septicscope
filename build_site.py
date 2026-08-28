from pathlib import Path
import base64, hashlib, html, io, os, re, shutil, subprocess, sys, zipfile

ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / 'bundle'
WORK = ROOT / '.septicscope-build'
OUTPUT = ROOT / 'site'
PARTS = [f'national{i:02d}.txt' for i in range(16)]
GA_MEASUREMENT_ID = 'G-F6RB8YERCM'
ADSENSE_CLIENT = 'ca-pub-8782868222380999'
ADSENSE_PUBLISHER_ID = 'pub-8782868222380999'

payload = ''.join((BUNDLE / name).read_text(encoding='utf-8').strip() for name in PARTS)
archive = base64.b64decode(payload, validate=True)
actual = hashlib.sha256(archive).hexdigest()

if WORK.exists():
    shutil.rmtree(WORK)
if OUTPUT.exists():
    shutil.rmtree(OUTPUT)
WORK.mkdir()

with zipfile.ZipFile(io.BytesIO(archive)) as z:
    bad_member = z.testzip()
    if bad_member:
        raise RuntimeError(f'Deploy bundle failed ZIP integrity check at {bad_member}')
    z.extractall(WORK)

# The custom .com is the permanent production URL. Allow an explicit
# Cloudflare environment variable to override this later if needed.
env = os.environ.copy()
env.setdefault('SITE_BASE_URL', 'https://septicscope.com')
subprocess.run([sys.executable, 'build_site.py'], cwd=WORK, check=True, env=env)
shutil.copytree(WORK / 'site', OUTPUT)

# Inject analytics and AdSense verification into every generated HTML page.
ga_tag = f'''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_MEASUREMENT_ID}');
</script>
'''
adsense_tag = f'''<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
'''
for html_file in OUTPUT.rglob('*.html'):
    text = html_file.read_text(encoding='utf-8')
    inject = ''
    if GA_MEASUREMENT_ID not in text:
        inject += ga_tag
    if ADSENSE_CLIENT not in text:
        inject += adsense_tag
    if inject and '</head>' in text:
        html_file.write_text(text.replace('</head>', inject + '</head>', 1), encoding='utf-8')

# Authorized Digital Sellers file for Google AdSense.
(OUTPUT / 'ads.txt').write_text(
    f'google.com, {ADSENSE_PUBLISHER_ID}, DIRECT, f08c47fec0942fa0\n',
    encoding='utf-8'
)

# ---------------------------------------------------------------------------
# Tennessee expansion: 86 non-contract counties validated against current
# Tennessee Department of Environment & Conservation (TDEC) sources.
# Contract counties are intentionally excluded because their local processes
# must be documented separately: Blount, Davidson, Hamilton, Jefferson, Knox,
# Madison, Sevier, Shelby and Williamson.
# Verified 2026-08-28.
# ---------------------------------------------------------------------------
TN_STATE_SOURCES = {
    'construction': 'https://www.tn.gov/environment/permits/water/septic-systems-permits/ssp/permit-water-septic-system-construction-permit.html',
    'application': 'https://www.tn.gov/environment/permits/water/septic-systems-permits/ssp/wr-sds-online-application-for-ground-water-protection-services.html',
    'installers': 'https://www.tn.gov/environment/permits/water/septic-systems-permits/ssp/wr-sds-active-installers-pumpers.html',
    'third_party': 'https://www.tn.gov/environment/permits/water/septic-systems-permits/ssp/permit-water-3rdparty-ssds.html',
}

TN_OFFICES = {
    'Chattanooga': {
        'phone': '(423) 634-5745',
        'address': '1301 Riverfront Parkway, Suite 206, Chattanooga, TN 37402',
        'source': 'https://www.tn.gov/environment/contacts/field-offices/chattanooga.html',
        'counties': ['Bledsoe','Bradley','Grundy','Marion','McMinn','Meigs','Polk','Rhea','Sequatchie'],
    },
    'Columbia': {
        'phone': '(931) 380-3371',
        'address': '1421 Hampshire Pike, Suite 100, Columbia, TN 38401',
        'source': 'https://www.tn.gov/content/tn/environment/contacts/field-offices/columbia.html',
        'counties': ['Bedford','Coffee','Franklin','Giles','Hickman','Lawrence','Lewis','Lincoln','Marshall','Maury','Moore','Perry','Wayne'],
    },
    'Cookeville': {
        'phone': '(931) 520-6688',
        'septic_phone': '931-206-6329',
        'address': '1844 Foreman Dr, Suite 101, Cookeville, TN 38501',
        'source': 'https://www.tn.gov/content/tn/environment/contacts/field-offices/cookeville.html',
        'counties': ['Cannon','Clay','Cumberland','Dekalb','Fentress','Jackson','Macon','Overton','Pickett','Putnam','Smith','Van Buren','Warren','White','Trousdale'],
    },
    'Jackson': {
        'phone': '(731) 512-1300',
        'address': '1625 Hollywood Drive, Jackson, TN 38305',
        'source': 'https://www.tn.gov/content/tn/environment/contacts/field-offices/jackson.html',
        'counties': ['Benton','Carroll','Chester','Crockett','Decatur','Dyer','Gibson','Hardeman','Hardin','Haywood','Henderson','Henry','Lake','Lauderdale','McNairy','Obion','Weakley'],
    },
    'Johnson City': {
        'phone': '(423) 854-5400',
        'records_phone': '(423) 854-5392',
        'records_email': 'TDEC.Johnsoncity.EFO@tn.gov',
        'address': '2305 Silverdale Drive, Johnson City, TN 37601-2162',
        'source': 'https://www.tn.gov/content/tn/environment/contacts/field-offices/johnson.html',
        'counties': ['Carter','Greene','Hancock','Hawkins','Johnson','Sullivan','Unicoi','Washington'],
    },
    'Knoxville': {
        'phone': '(865) 594-6035',
        'address': '3711 Middlebrook Pike, Suite 101, Knoxville, TN 37921',
        'source': 'https://www.tn.gov/content/tn/environment/contacts/field-offices/knoxville.html',
        'counties': ['Anderson','Campbell','Claiborne','Cocke','Grainger','Hamblen','Loudon','Monroe','Morgan','Roane','Scott','Union'],
    },
    'Memphis': {
        'phone': '(901) 371-3000',
        'address': '8383 Wolf Lake Drive, Bartlett, TN 38133-4119',
        'source': 'https://www.tn.gov/environment/contacts/field-offices/memphis.html',
        'counties': ['Fayette','Tipton'],
    },
    'Nashville': {
        'phone': '(615) 687-7000',
        'address': '711 R.S. Gass Blvd, Nashville, TN 37216',
        'source': 'https://www.tn.gov/environment/contacts/field-offices/nashville.html',
        'counties': ['Cheatham','Dickson','Houston','Humphreys','Montgomery','Robertson','Rutherford','Stewart','Sumner','Wilson'],
    },
}


def slugify(value):
    value = value.lower().replace('&', ' and ')
    return re.sub(r'[^a-z0-9]+', '-', value).strip('-')


def tn_page(county, office_name, office):
    county_e = html.escape(county)
    office_e = html.escape(office_name)
    phone = html.escape(office['phone'])
    address = html.escape(office['address'])
    extra_contact = ''
    if office.get('septic_phone'):
        extra_contact += f'<li><strong>Dedicated septic inquiry line:</strong> {html.escape(office["septic_phone"])}</li>'
    if office.get('records_phone'):
        extra_contact += f'<li><strong>Existing septic layout / records assistance:</strong> {html.escape(office["records_phone"])}</li>'
    if office.get('records_email'):
        extra_contact += f'<li><strong>Septic layout requests:</strong> <a href="mailto:{html.escape(office["records_email"])}">{html.escape(office["records_email"])}</a></li>'
    canonical = f'https://septicscope.com/counties/tennessee/{slugify(county)}/'
    title = f'{county_e} County TN Septic Permits & Requirements | SepticScope'
    description = f'Official-source guide to septic permits, repairs, records and contacts for {county_e} County, Tennessee. TDEC permitting authority and field office details verified August 2026.'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{description}"><link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{description}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="article">
<style>
:root{{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b;--accent2:#0f5548}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.65;background:#fff}}header{{border-bottom:1px solid var(--line);background:#fff}}.nav{{max-width:1080px;margin:auto;padding:18px 24px;display:flex;align-items:center;justify-content:space-between;gap:20px}}.brand{{font-size:1.25rem;font-weight:800;text-decoration:none;color:var(--ink)}}nav a{{color:var(--muted);text-decoration:none;margin-left:18px}}main{{max-width:900px;margin:auto;padding:42px 24px 70px}}.crumb{{font-size:.92rem;color:var(--muted);margin-bottom:18px}}.crumb a{{color:var(--accent)}}h1{{font-size:clamp(2rem,5vw,3.25rem);line-height:1.08;margin:.15em 0 .35em}}h2{{margin-top:2em;line-height:1.2}}.lede{{font-size:1.16rem;color:#3e4a55;max-width:780px}}.verified{{display:inline-block;background:#eaf5f1;color:var(--accent2);font-weight:700;padding:6px 10px;border-radius:999px;font-size:.83rem}}.card{{border:1px solid var(--line);border-radius:14px;background:var(--panel);padding:22px;margin:24px 0}}.card h2{{margin-top:0}}ul,ol{{padding-left:1.35rem}}a{{color:var(--accent)}}.notice{{border-left:4px solid #d59b21;padding:12px 16px;background:#fff9eb}}.sources li{{margin:.55rem 0}}footer{{border-top:1px solid var(--line);padding:28px 24px;color:var(--muted);font-size:.9rem}}footer div{{max-width:900px;margin:auto}}
</style>
{ga_tag}{adsense_tag}
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{county_e} County, Tennessee Septic Permit Guide","dateModified":"2026-08-28","publisher":{{"@type":"Organization","name":"SepticScope"}},"mainEntityOfPage":"{canonical}"}}</script>
</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a><nav><a href="/counties/">County Guides</a><a href="/guides/">Guides</a><a href="/faq/">FAQ</a></nav></div></header>
<main><div class="crumb"><a href="/">Home</a> / <a href="/counties/">Counties</a> / <a href="/counties/tennessee/">Tennessee</a> / {county_e} County</div>
<span class="verified">Official sources checked August 28, 2026</span><h1>{county_e} County, Tennessee septic permits and requirements</h1>
<p class="lede">For properties in {county_e} County, the Tennessee Department of Environment and Conservation (TDEC), Division of Water Resources, is the septic permitting authority identified by the official state materials reviewed for this guide. {county_e} County is not one of Tennessee's nine contract counties, so the state's Subsurface Sewage Disposal System (SSDS) process applies rather than a separate contract-county permitting program.</p>
<div class="card"><h2>Who to contact in {county_e} County</h2><p><strong>TDEC {office_e} Environmental Field Office</strong></p><ul><li><strong>Phone:</strong> {phone}</li><li><strong>Office:</strong> {address}</li>{extra_contact}</ul><p>The official TDEC field-office page lists {county_e} County in the {office_e} office's service area. For a site-specific question, call the office and ask for Division of Water Resources / septic assistance.</p></div>
<h2>When a septic permit is required</h2><p>TDEC states that a Septic System Construction Permit is required when a property owner wants to install a subsurface sewage disposal system or repair an existing faulty system. For a conventional system, the state says the permit should be obtained before dirt work, the building pad, or construction begins. A separate repair permit is required before work is performed on a failing septic system.</p>
<h2>What the application can require</h2><p>State application materials identify information such as the landowner and site address, lot size, expected occupancy or bedroom count, water use, basement information, the proposed installer if known, and a rough site sketch showing items such as property lines, the house site, wells or springs, driveway and utilities. Depending on the site or system, a soils map prepared by a qualified soil scientist and engineered system design may also be required.</p>
<h2>Licensed installers and pumpers</h2><p>Tennessee requires septic system installers and septage pumpers to hold valid state permits. TDEC's installer permits are generally valid statewide. The state DataViewer can be used to locate active installers and pumpers and narrow results by county. Before hiring anyone, verify the person's current status in the state system rather than relying only on advertising or an old license number.</p>
<h2>Third-party permit option</h2><p>Since October 1, 2024, Tennessee law allows certain permit packages and final inspections to be prepared by a registered third-party water resources engineer. TDEC also states that, for non-contract counties such as {county_e}, third-party permit packages and certificate-of-completion packages are submitted to the department. The state describes a ten-business-day review framework after receipt of a qualifying package, although a specific project can still require corrections or additional information.</p>
<h2>Existing septic records</h2><p>For an existing home, ask the {office_e} Environmental Field Office about available septic layouts, permits, final inspections or public records before paying for a new design. Records can help identify the original disposal area and permitted bedroom count, but field conditions and later unrecorded work may still require an on-site inspection.</p>
<div class="notice"><strong>County-specific note:</strong> The official sources reviewed did not identify a separate {county_e} County contract-county septic program. This page therefore reports the verified TDEC statewide process and the field office that serves the county. Parcel constraints, subdivision restrictions, floodplain rules, wells, soils, repair conditions and local building requirements can change what is allowed on a specific property.</div>
<h2>Practical order of operations</h2><ol><li>Confirm that the parcel is not served by a public sewer or subject to a mandatory sewer-connection rule.</li><li>Contact the TDEC {office_e} Environmental Field Office for the current septic service path.</li><li>Gather the site plan, bedroom/occupancy information, water-supply locations and any existing septic records.</li><li>Complete any required soils evaluation or engineering before committing to a house location.</li><li>Obtain the construction or repair permit before beginning regulated septic work.</li><li>Use a properly permitted installer and complete the required inspection / certificate-of-completion process.</li></ol>
<h2>Official sources</h2><ul class="sources"><li><a href="{html.escape(office['source'])}" rel="nofollow">TDEC {office_e} Environmental Field Office — counties served and contact information</a></li><li><a href="{TN_STATE_SOURCES['construction']}" rel="nofollow">TDEC — Septic System Construction Permit</a></li><li><a href="{TN_STATE_SOURCES['application']}" rel="nofollow">TDEC — Online Application for Septic Related Services</a></li><li><a href="{TN_STATE_SOURCES['installers']}" rel="nofollow">TDEC — Licensed Septic System Installers & Septic Tank Pumpers</a></li><li><a href="{TN_STATE_SOURCES['third_party']}" rel="nofollow">TDEC — Third-Party Permits & Final Inspections</a></li></ul>
<p><em>Verified August 28, 2026. SepticScope summarizes public agency information for planning purposes; the permitting agency controls if its current instructions differ.</em></p></main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''


# Generate Tennessee hub and all validated non-contract county pages.
tn_rows = []
for office_name, office in TN_OFFICES.items():
    for county in office['counties']:
        tn_rows.append((county, office_name, office))
        out_dir = OUTPUT / 'counties' / 'tennessee' / slugify(county)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / 'index.html').write_text(tn_page(county, office_name, office), encoding='utf-8')

tn_rows.sort(key=lambda row: row[0])
county_links = '\n'.join(
    f'<li><a href="/counties/tennessee/{slugify(county)}/">{html.escape(county)} County</a> <span>— TDEC {html.escape(office_name)} Environmental Field Office</span></li>'
    for county, office_name, _ in tn_rows
)
tn_hub = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tennessee Septic Permit Guide by County | SepticScope</title><meta name="description" content="Tennessee septic permit and contact guides for 86 non-contract counties, verified from TDEC sources in August 2026."><link rel="canonical" href="https://septicscope.com/counties/tennessee/"><style>body{{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:0;color:#17212b;line-height:1.6}}header{{border-bottom:1px solid #dce3e8}}.nav,main,footer div{{max-width:1000px;margin:auto;padding:20px 24px}}.brand{{font-weight:800;color:#17212b;text-decoration:none}}main{{padding-top:42px;padding-bottom:70px}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}}a{{color:#176b5b}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px 28px;padding-left:1.3rem}}.grid span{{color:#5b6672;font-size:.9rem}}.note{{background:#f7fafb;border:1px solid #dce3e8;padding:18px;border-radius:12px}}footer{{border-top:1px solid #dce3e8;color:#5b6672}}</style>{ga_tag}{adsense_tag}</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><p><a href="/counties/">← All county guides</a></p><h1>Tennessee septic permits by county</h1><p>These guides cover all 86 Tennessee counties where TDEC's statewide Subsurface Sewage Disposal System process applies. The nine contract counties—Blount, Davidson, Hamilton, Jefferson, Knox, Madison, Sevier, Shelby and Williamson—are being researched separately because their local septic programs can use different application steps or additional permits.</p><div class="note"><strong>Verified August 28, 2026:</strong> county-to-field-office assignments and statewide permit requirements are sourced to the Tennessee Department of Environment and Conservation.</div><h2>Choose a county</h2><ul class="grid">{county_links}</ul><h2>Statewide basics</h2><p>TDEC requires a construction permit for new septic systems and a repair permit before work on a failing system. Application materials can require property and bedroom information, a site sketch, and—when applicable—soil-scientist or engineering documentation. Always confirm the current process with the field office serving the parcel before beginning site work.</p></main><footer><div>© 2026 SepticScope</div></footer></body></html>'''
tn_hub_dir = OUTPUT / 'counties' / 'tennessee'
tn_hub_dir.mkdir(parents=True, exist_ok=True)
(tn_hub_dir / 'index.html').write_text(tn_hub, encoding='utf-8')

# Add Tennessee to the existing county directory without depending on the
# original bundle's exact markup.
county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    if '/counties/tennessee/' not in text:
        promo = f'''<section style="max-width:1080px;margin:32px auto;padding:22px 24px;border:1px solid #dce3e8;border-radius:14px;background:#f7fafb"><h2 style="margin-top:0">Tennessee county guides</h2><p>New: 86 non-contract Tennessee counties verified from current TDEC permitting and field-office sources.</p><p><a href="/counties/tennessee/">Browse Tennessee septic permit guides →</a></p></section>'''
        text = text.replace('</main>', promo + '</main>', 1) if '</main>' in text else text.replace('</body>', promo + '</body>', 1)
        county_index.write_text(text, encoding='utf-8')

# Add the new URLs to the XML sitemap while retaining the bundle-generated URLs.
sitemap = OUTPUT / 'sitemap.xml'
new_urls = ['https://septicscope.com/counties/tennessee/'] + [
    f'https://septicscope.com/counties/tennessee/{slugify(county)}/' for county, _, _ in tn_rows
]
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    entries = ''.join(f'<url><loc>{url}</loc><lastmod>2026-08-28</lastmod></url>' for url in new_urls if url not in sm)
    if entries:
        sm = sm.replace('</urlset>', entries + '</urlset>')
        sitemap.write_text(sm, encoding='utf-8')
else:
    entries = ''.join(f'<url><loc>{url}</loc><lastmod>2026-08-28</lastmod></url>' for url in new_urls)
    sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + entries + '</urlset>', encoding='utf-8')

shutil.rmtree(WORK)
print(f'SepticScope build complete: {OUTPUT} (bundle sha256 {actual}; +{len(tn_rows)} Tennessee counties)')
