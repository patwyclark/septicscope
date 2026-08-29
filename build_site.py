from pathlib import Path
import base64, html, io, os, re, shutil, subprocess, sys, zipfile

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
if WORK.exists(): shutil.rmtree(WORK)
if OUTPUT.exists(): shutil.rmtree(OUTPUT)
WORK.mkdir()
with zipfile.ZipFile(io.BytesIO(archive)) as z:
    bad_member = z.testzip()
    if bad_member: raise RuntimeError(f'Deploy bundle failed ZIP integrity check at {bad_member}')
    z.extractall(WORK)

env = os.environ.copy()
env.setdefault('SITE_BASE_URL', 'https://septicscope.com')
subprocess.run([sys.executable, 'build_site.py'], cwd=WORK, check=True, env=env)
shutil.copytree(WORK / 'site', OUTPUT)

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
    if GA_MEASUREMENT_ID not in text: inject += ga_tag
    if ADSENSE_CLIENT not in text: inject += adsense_tag
    if inject and '</head>' in text:
        html_file.write_text(text.replace('</head>', inject + '</head>', 1), encoding='utf-8')
(OUTPUT / 'ads.txt').write_text(f'google.com, {ADSENSE_PUBLISHER_ID}, DIRECT, f08c47fec0942fa0\n', encoding='utf-8')

def slugify(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower().replace('&', ' and ')).strip('-')

COMMON_STYLE = ''':root{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b}*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.65}header{border-bottom:1px solid var(--line)}.nav,main,footer div{max-width:1000px;margin:auto;padding:20px 24px}.brand{font-weight:800;color:var(--ink);text-decoration:none}main{padding-top:42px;padding-bottom:70px}.crumb{font-size:.92rem;color:var(--muted)}h1{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}h2{margin-top:1.8em}a{color:var(--accent)}.card,.note{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}.verified{display:inline-block;background:#eaf5f1;color:#0f5548;font-weight:700;padding:6px 10px;border-radius:999px;font-size:.83rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:8px 28px}footer{border-top:1px solid var(--line);color:var(--muted)}'''

def write_county_page(state, state_slug, county, authority, contact, body_sections, sources, verified='August 28, 2026'):
    c = html.escape(county)
    canonical = f'https://septicscope.com/counties/{state_slug}/{slugify(county)}/'
    title = f'{c} County {state} Septic Permits & Requirements | SepticScope'
    source_html = ''.join(f'<li><a href="{html.escape(url)}" rel="nofollow">{html.escape(label)}</a></li>' for label, url in sources)
    sections = ''.join(f'<h2>{html.escape(h)}</h2><p>{p}</p>' for h,p in body_sections)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="Official-source guide to septic permits, site evaluation, installation and contacts for {c} County, {state}."><link rel="canonical" href="{canonical}">
<style>{COMMON_STYLE}</style>{ga_tag}{adsense_tag}</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header>
<main><div class="crumb"><a href="/">Home</a> / <a href="/counties/">Counties</a> / <a href="/counties/{state_slug}/">{state}</a> / {c} County</div>
<p><span class="verified">Official sources checked {verified}</span></p><h1>{c} County, {state} septic permits and requirements</h1>
<div class="card"><h2>Permitting authority</h2><p><strong>{html.escape(authority)}</strong></p><p>{contact}</p></div>{sections}
<h2>Official sources</h2><ul>{source_html}</ul><p><em>SepticScope summarizes public-agency information for planning purposes. The permitting agency's current instructions control if they differ from this guide.</em></p></main>
<footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer></body></html>'''
    out = OUTPUT / 'counties' / state_slug / slugify(county)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(page, encoding='utf-8')
    return canonical

TN_SOURCES = [
('TDEC Septic System Construction Permit','https://www.tn.gov/environment/permits/water/septic-systems-permits/ssp/permit-water-septic-system-construction-permit.html'),
('TDEC online septic-services application','https://www.tn.gov/environment/permits/water/septic-systems-permits/ssp/wr-sds-online-application-for-ground-water-protection-services.html'),
('TDEC licensed installers and pumpers','https://www.tn.gov/environment/permits/water/septic-systems-permits/ssp/wr-sds-active-installers-pumpers.html'),
('TDEC third-party permits and final inspections','https://www.tn.gov/environment/permits/water/septic-systems-permits/ssp/permit-water-3rdparty-ssds.html'),
]
TN_OFFICES = {
'Chattanooga':('423-634-5745','1301 Riverfront Parkway, Suite 206, Chattanooga, TN 37402','https://www.tn.gov/environment/contacts/field-offices/chattanooga.html',['Bledsoe','Bradley','Grundy','Marion','McMinn','Meigs','Polk','Rhea','Sequatchie']),
'Columbia':('931-380-3371','1421 Hampshire Pike, Suite 100, Columbia, TN 38401','https://www.tn.gov/content/tn/environment/contacts/field-offices/columbia.html',['Bedford','Coffee','Franklin','Giles','Hickman','Lawrence','Lewis','Lincoln','Marshall','Maury','Moore','Perry','Wayne']),
'Cookeville':('931-520-6688','1844 Foreman Dr, Suite 101, Cookeville, TN 38501','https://www.tn.gov/content/tn/environment/contacts/field-offices/cookeville.html',['Cannon','Clay','Cumberland','Dekalb','Fentress','Jackson','Macon','Overton','Pickett','Putnam','Smith','Van Buren','Warren','White','Trousdale']),
'Jackson':('731-512-1300','1625 Hollywood Drive, Jackson, TN 38305','https://www.tn.gov/content/tn/environment/contacts/field-offices/jackson.html',['Benton','Carroll','Chester','Crockett','Decatur','Dyer','Gibson','Hardeman','Hardin','Haywood','Henderson','Henry','Lake','Lauderdale','McNairy','Obion','Weakley']),
'Johnson City':('423-854-5400','2305 Silverdale Drive, Johnson City, TN 37601-2162','https://www.tn.gov/content/tn/environment/contacts/field-offices/johnson.html',['Carter','Greene','Hancock','Hawkins','Johnson','Sullivan','Unicoi','Washington']),
'Knoxville':('865-594-6035','3711 Middlebrook Pike, Suite 101, Knoxville, TN 37921','https://www.tn.gov/content/tn/environment/contacts/field-offices/knoxville.html',['Anderson','Campbell','Claiborne','Cocke','Grainger','Hamblen','Loudon','Monroe','Morgan','Roane','Scott','Union']),
'Memphis':('901-371-3000','8383 Wolf Lake Drive, Bartlett, TN 38133-4119','https://www.tn.gov/environment/contacts/field-offices/memphis.html',['Fayette','Tipton']),
'Nashville':('615-687-7000','711 R.S. Gass Blvd, Nashville, TN 37216','https://www.tn.gov/environment/contacts/field-offices/nashville.html',['Cheatham','Dickson','Houston','Humphreys','Montgomery','Robertson','Rutherford','Stewart','Sumner','Wilson']),
}
tn_urls=[]; tn_links=[]
for office,(phone,address,office_url,counties) in TN_OFFICES.items():
    for county in counties:
        contact=f'TDEC {office} Environmental Field Office — {html.escape(phone)}; {html.escape(address)}. TDEC lists {html.escape(county)} County in this office’s service area.'
        sections=[
        ('When a permit is required','TDEC states that a Septic System Construction Permit is required to install a subsurface sewage disposal system or repair an existing faulty system. Obtain the applicable permit before regulated septic work begins.'),
        ('Application and site information','State application materials can require ownership and site information, expected occupancy or bedroom count, water supply information, a site sketch, and—depending on site conditions—soil-scientist or engineered design documentation.'),
        ('Installers and inspections','Tennessee requires septic installers and septage pumpers to hold current state permits. Verify credentials and complete the required inspection or certificate-of-completion process before covering or placing a system in service.')]
        url=write_county_page('Tennessee','tennessee',county,'Tennessee Department of Environment and Conservation (TDEC), Division of Water Resources',contact,sections,[(f'TDEC {office} Environmental Field Office',office_url)]+TN_SOURCES)
        tn_urls.append(url); tn_links.append((county,office))

KY_STATE = 'https://www.chfs.ky.gov/agencies/dph/dphps/emb/Pages/environmentmgmt.aspx'
KY_PERMIT_REG = 'https://apps.legislature.ky.gov/law/kar/titles/902/010/110/'
KY_SYSTEM_REG = 'https://apps.legislature.ky.gov/law/kar/titles/902/010/085/'
KY_DISTRICT = 'https://www.barrenriverhealth.org/services/onsite-sewage'
KY_CONTACT = 'https://www.barrenriverhealth.org/contact'
KY_COUNTIES = {
'Barren':('270-651-8321','200 South Green Street, Glasgow, KY 42142'),
'Butler':('270-526-3221','104 North Warren Street, Morgantown, KY 42261'),
'Edmonson':('270-597-2194','221 Mammoth Cave Road, Brownsville, KY 42210'),
'Hart':('270-524-2511','500 AA Whitman Lane, Munfordville, KY 42765'),
'Logan':('270-726-8341','151 S. Franklin Street, Russellville, KY 42276'),
'Metcalfe':('270-432-3214','615 West Stockton Street, Edmonton, KY 42129'),
'Simpson':('270-586-8261','1131 South College Street, Franklin, KY 42134'),
'Warren':('270-781-2490','1109 State Street, Bowling Green, KY 42101'),
}
ky_urls=[]; ky_links=[]
for county,(phone,address) in KY_COUNTIES.items():
    contact=f'Barren River District Health Department serves {html.escape(county)} County. Local office: {html.escape(phone)}, {html.escape(address)}.'
    sections=[
    ('Site evaluation comes first','Kentucky’s Onsite Sewage Disposal Systems Program is administered through local health departments. Local onsite septic inspectors perform site evaluations and inspections, and the evaluation determines whether site and soil conditions are suitable and what system can be permitted.'),
    ('Permit before construction or alteration','Kentucky regulation 902 KAR 10:110 requires an onsite sewage disposal permit from the local health department before constructing, installing, or altering a regulated onsite sewage disposal system. The permit process includes the state application and applicable local-board fees.'),
    ('District-specific process','Barren River District Health Department states that its onsite sewage team performs soil evaluations, reviews installation drawings before issuing permits, inspects systems after installation, and handles variances under applicable policy.'),
    ('Who may install','Kentucky generally issues construction permits to certified installers. A homeowner may obtain a homeowner permit through the local health department when the regulatory conditions are met.'),
    ('Permit duration and site limits','902 KAR 10:085 states that a permit is issued by a certified inspector and expires one year from issuance unless an extension is granted. Site suitability depends on factors including slope, soil depth, restrictive horizons, groundwater and other conditions evaluated under the regulation.')]
    sources=[('Kentucky CHFS — Onsite Sewage Disposal Systems Program',KY_STATE),('902 KAR 10:110 — permit issuance',KY_PERMIT_REG),('902 KAR 10:085 — system and site-evaluation standards',KY_SYSTEM_REG),('Barren River District Health Department — Onsite Sewage',KY_DISTRICT),('Barren River District Health Department — county offices',KY_CONTACT)]
    url=write_county_page('Kentucky','kentucky',county,'Barren River District Health Department (local health department administering Kentucky’s onsite sewage program)',contact,sections,sources)
    ky_urls.append(url); ky_links.append(county)

AL_STATE = 'https://www.alabamapublichealth.gov/onsite/index.html'
AL_BEFORE = 'https://www.alabamapublichealth.gov/onsite/before-construction.html'
AL_RECORDS = 'https://www.alabamapublichealth.gov/onsite/septic-tanks.html'
AL_COUNTIES = {
'Baldwin':('251-947-3618','22251 Palmer Street, Robertsdale, AL 36567','https://www.alabamapublichealth.gov/baldwin/sewage.html','https://www.alabamapublichealth.gov/baldwin/contact.html'),
'Blount':('205-947-1076','1001 Lincoln Avenue, Oneonta, AL 35121','https://www.alabamapublichealth.gov/Blount/environmental-services.html','https://www.alabamapublichealth.gov/Blount/contact.html'),
'Chambers':('334-756-0758','5 North Medical Park Drive, Valley, AL 36854',None,'https://www.alabamapublichealth.gov/chambers/contact.html'),
'Cherokee':('256-927-7322','833 Cedar Bluff Road, Centre, AL 35960','https://www.alabamapublichealth.gov/cherokee/environmental-services.html','https://www.alabamapublichealth.gov/cherokee/contact.html'),
'DeKalb':('256-845-7031','2401 Calvin Drive SW, Fort Payne, AL 35967',None,'https://www.alabamapublichealth.gov/Dekalb/contact.html'),
'Houston':('334-678-2815','1781 East Cottonwood Road, Dothan, AL 36301','https://www.alabamapublichealth.gov/houston/sewage.html','https://www.alabamapublichealth.gov/houston/contact.html'),
'Montgomery':('334-293-6452','3060 Mobile Highway, Montgomery, AL 36108','https://www.alabamapublichealth.gov/montgomery/sewage.html','https://www.alabamapublichealth.gov/about/locations.html'),
}
al_urls=[]; al_links=[]
for county,(phone,address,sewage_url,contact_url) in AL_COUNTIES.items():
    contact=f'{html.escape(county)} County Health Department Environmental Office — {html.escape(phone)}; {html.escape(address)}.'
    sections=[
    ('Permit before installation or repair','Alabama requires a permit from the local county health department before installing a new onsite sewage disposal system or repairing an existing system. The county environmental office is the local point of contact for the permit and inspection process.'),
    ('Site and soil evaluation','ADPH directs property owners to have the site evaluated by an appropriate registered professional. Depending on site conditions and system type, this can involve a professional soils classifier, land surveyor, geologist, or engineer; engineered design is required for certain restricted sites or designed systems.'),
    ('What goes into the application','State guidance identifies soils information, property or legal-description information, a plot plan and vicinity information among the materials used for permit review. The local health department reviews the application and site information before a Permit to Install is issued.'),
    ('Installation and inspection','Do not begin construction until the Permit to Install has been issued. ADPH says system installers must be properly licensed, and county inspection or approval is required before the system is covered or placed into use.'),
    ('Finding existing septic records','ADPH says property owners or their agents can contact the local health department for existing septic-system information. A completed permit or Approval for Use may include a diagram showing the installed tank and field-line layout.')]
    sources=[('ADPH Soil and Onsite Sewage Branch',AL_STATE),('ADPH — before construction',AL_BEFORE),('ADPH — septic tank records and maintenance',AL_RECORDS),('County environmental/contact information',contact_url)]
    if sewage_url:
        sources.insert(0,(f'{county} County onsite/environmental sewage guidance',sewage_url))
    if county == 'Cherokee':
        sections.append(('Weiss Lake holding-tank rule','Cherokee County has a separate local rule for temporary sewage holding tanks within Alabama Power Company’s flood easement around Weiss Lake where sewer service is unavailable. That process requires a county application, a contract with a permitted pumper, county inspection and a permit before installation or use; it should not be treated as the ordinary septic-system process.'))
        sources.append(('Cherokee County — sewage holding tanks','https://www.alabamapublichealth.gov/cherokee/sewage-holding-tanks.html'))
    url=write_county_page('Alabama','alabama',county,f'{county} County Health Department, Environmental Office (Alabama Department of Public Health)',contact,sections,sources)
    al_urls.append(url); al_links.append(county)

def write_hub(state,state_slug,links,intro,note):
    items=''.join(f'<li><a href="/counties/{state_slug}/{slugify(c)}/">{html.escape(c)} County</a>{(" — "+html.escape(extra)) if extra else ""}</li>' for c,extra in links)
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{state} Septic Permit Guides by County | SepticScope</title><meta name="description" content="Official-source {state} septic permit guides by county."><link rel="canonical" href="https://septicscope.com/counties/{state_slug}/"><style>{COMMON_STYLE}</style>{ga_tag}{adsense_tag}</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><p><a href="/counties/">← All county guides</a></p><h1>{state} septic permits by county</h1><p>{intro}</p><div class="note">{note}</div><h2>Choose a county</h2><ul class="grid">{items}</ul></main><footer><div>© 2026 SepticScope</div></footer></body></html>'''
    d=OUTPUT/'counties'/state_slug; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(page,encoding='utf-8')

write_hub('Tennessee','tennessee',[(c,o) for c,o in sorted(tn_links)],'These guides cover Tennessee counties where TDEC’s statewide Subsurface Sewage Disposal System process applies.','The nine Tennessee contract counties—Blount, Davidson, Hamilton, Jefferson, Knox, Madison, Sevier, Shelby and Williamson—remain excluded until their local septic procedures are documented individually.')
write_hub('Kentucky','kentucky',[(c,'Barren River District Health Department') for c in sorted(ky_links)],'Kentucky administers onsite sewage through local health departments. This first Kentucky batch covers the eight counties served by Barren River District Health Department, whose official onsite-sewage program and county office contacts were validated.','Kentucky has 120 counties. SepticScope is adding them district-by-district so each page identifies a verified local permitting authority instead of publishing generic county pages.')
write_hub('Alabama','alabama',[(c,'County Health Department Environmental Office') for c in sorted(al_links)],'Alabama’s Soil and Onsite Sewage Branch coordinates the onsite sewage program through county health departments. These first Alabama guides pair statewide permit rules with verified county environmental-office contacts and county-specific guidance where available.','This batch intentionally covers only counties whose environmental contact information and permitting role were validated from current ADPH pages. Additional Alabama counties will be added as their local information is checked.')

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    promos=''
    if '/counties/tennessee/' not in text: promos += '<section><h2>Tennessee</h2><p><a href="/counties/tennessee/">Browse 86 verified Tennessee county septic guides →</a></p></section>'
    if '/counties/kentucky/' not in text: promos += '<section><h2>Kentucky</h2><p><a href="/counties/kentucky/">Browse the first 8 verified Kentucky county septic guides →</a></p></section>'
    if '/counties/alabama/' not in text: promos += '<section><h2>Alabama</h2><p><a href="/counties/alabama/">Browse the first 7 verified Alabama county septic guides →</a></p></section>'
    if promos:
        text=text.replace('</main>',promos+'</main>',1) if '</main>' in text else text.replace('</body>',promos+'</body>',1)
        county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
new_urls=['https://septicscope.com/counties/tennessee/']+tn_urls+['https://septicscope.com/counties/kentucky/']+ky_urls+['https://septicscope.com/counties/alabama/']+al_urls
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
else:
    sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-28</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm=sm.replace('</urlset>',entries+'</urlset>')
    sitemap.write_text(sm,encoding='utf-8')

shutil.rmtree(WORK)
print(f'SepticScope build complete: {OUTPUT} (+{len(tn_urls)} Tennessee counties, +{len(ky_urls)} Kentucky counties, +{len(al_urls)} Alabama counties)')
