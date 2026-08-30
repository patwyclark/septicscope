# SepticScope North Carolina expansion — verified production batch.
# Verified from NCDHHS and official county government sources on 2026-08-30.

NC_STATE = 'https://www.dph.ncdhhs.gov/programs/environmental-health/site-water-protection-branch/site-wastewater-program'
NC_BRANCH = 'https://www.dph.ncdhhs.gov/programs/environmental-health/site-water-protection-branch'

NC_COUNTIES = [
    {
        'county': 'Buncombe',
        'authority': 'Buncombe County Health and Human Services — Environmental Health, Septic & Sewage Program',
        'contact': 'Buncombe County Environmental Health administers septic permitting for property in the county that is not served by public sewer.',
        'sources': [
            ('Buncombe County — Environmental Health / Septic & Sewage', 'https://www.buncombecounty.org/governing/depts/health/environmentalhealth.aspx'),
        ],
        'sections': [
            ('Septic authorization comes before the building permit', 'Buncombe County states that a residence, place of business, or place of public assembly not served by public sewer must have an approved wastewater system. For new development, the county will not issue the building permit until an Authorization to Construct has been issued for the septic system.'),
            ('Application includes a plat and site preparation', 'To obtain an Authorization to Construct, Buncombe County requires an application to Environmental Health with a plat of the property and applicable fees. Property lines and the proposed house site must be clearly marked so the Environmental Health Specialist can evaluate the proposed development area.'),
            ('County Environmental Health evaluates site suitability', 'After the application is complete, an Environmental Health Specialist performs the onsite evaluation to determine whether the proposed site is suitable for a septic system. Applicants are given a preparation checklist and coordinate the evaluation with the assigned specialist.'),
            ('Improvement Permits can be obtained before development', 'When public sewer is unavailable, Buncombe County allows an Improvement Permit to be obtained for property that may be developed later. The permit identifies the proposed facility, wastewater system and location, design wastewater flow, required site modifications, and other site-specific conditions.'),
            ('Improvement Permit duration depends on the supporting plan', 'Buncombe County states that an Improvement Permit is valid for at least five years. When the application includes an engineered plat showing the exact structure and septic-system locations together with the required detailed site plan, the county states that an Improvement Permit with no expiration date may be issued.'),
        ],
    },
    {
        'county': 'Henderson',
        'authority': 'Henderson County Department of Public Health — Environmental Health, On-Site Wastewater Program',
        'contact': 'Henderson County Environmental Health, 1200 Spartanburg Highway, Suite 100, Hendersonville, NC 28792; 828-694-6060.',
        'sources': [
            ('Henderson County — Applications for Sewage Disposal System Permits', 'https://www.hendersoncountync.gov/health/page/applications-permits-sewage-disposal-systems-and-wells'),
            ('Henderson County — Environmental Health', 'https://www.hendersoncountync.gov/health/page/environmental-health'),
            ('Henderson County — Septic and Well Permit Search', 'https://www.hendersoncountync.gov/health/page/search-septic-well-permits'),
            ('Henderson County — Environmental Health Forms and Fee Schedule', 'https://www.hendersoncountync.gov/health/page/environmental-health-forms-fee-schedule'),
        ],
        'sections': [
            ('Lot evaluation is the first local permitting step', 'Henderson County accepts applications for a lot evaluation for a subsurface sewage disposal permit through the county Permit Center. The county requires the applicable application fee and a property plat before Environmental Health evaluates the proposed septic site.'),
            ('The county evaluates specific soil and site conditions', 'Henderson County identifies topography and landscape position, soil characteristics, soil wetness, soil depth, restrictive horizons, and available space as factors used by the Environmental Health Specialist during the lot evaluation.'),
            ('Approval leads to an Authorization to Construct', 'After the lot has been evaluated and approved, Henderson County issues an Authorization to Construct for the subsurface sewage disposal system. The county states that this septic authorization is also used in obtaining the building permit from County Inspections.'),
            ('Final inspection is required before the Operations Permit', 'Once the septic system is installed, Henderson County performs another inspection. If the installation is approved, Environmental Health issues an Operations Permit to the property owner.'),
            ('Existing-system approvals and revisions are separate services', 'Henderson County’s current Environmental Health fee schedule distinguishes new Improvement Permit / Construction Authorization work from Existing System Approval and wastewater permit revisions, so additions or projects relying on an existing system should use the applicable county review path.'),
            ('County records include a modern search and legacy archive', 'Henderson County provides an online permit search for modern septic and well records from 2004 forward and a separate legacy archive for records from 1968 through 2004. The county cautions that some older septic records are missing.'),
        ],
    },
    {
        'county': 'Mecklenburg',
        'authority': 'Mecklenburg County Environmental Health — Groundwater and Wastewater Services',
        'contact': 'Mecklenburg County Environmental Health, 3205 Freedom Drive, Suite 8000, Charlotte, NC 28208; 980-314-1620. The county lists 980-314-1680 for septic soil-test and general septic questions.',
        'sources': [
            ('Mecklenburg County — Environmental Health', 'https://eh.mecknc.gov/'),
            ('Mecklenburg County — Septic System Fee Schedule and Permitting Sequence', 'https://eh.mecknc.gov/environmental-health/groundwater-and-wastewater-services/septic-system-fee-schedule'),
            ('Mecklenburg County — Basic Steps for a New Septic System', 'https://eh.mecknc.gov/news/basic-steps-new-septic-system'),
        ],
        'sections': [
            ('Groundwater and Wastewater Services handles septic review', 'Mecklenburg County identifies Groundwater and Wastewater Services as the Environmental Health program that performs plan review, permitting, and evaluation of onsite wastewater systems and private wells.'),
            ('New systems begin with application and soil evaluation', 'Mecklenburg County’s published workflow begins with a septic application and soil evaluation. The applicant must identify the proposed building location and clearly mark property lines before the soil evaluation is conducted.'),
            ('Improvement Permit and Construction Authorization are distinct approvals', 'After soil and site review, the Environmental Health Specialist determines the system type and layout and the county issues or denies the Improvement Permit. Construction Authorization is a later approval in the county’s published permitting sequence.'),
            ('The installer coordinates with Environmental Health before installation', 'Mecklenburg County states that the septic contractor must contact the Environmental Health Specialist before installing the system. The specialist issues Installation Approval at the site to the septic contractor.'),
            ('Final inspection occurs before the system is covered', 'The septic contractor must contact the Environmental Health Specialist to schedule a final inspection before covering the system. After final approval, an Operation Permit is issued; the county ties that approval to obtaining the Certificate of Occupancy.'),
            ('Repairs, alterations, plot-plan changes, and existing-system use require county permits', 'Mecklenburg County’s current schedule identifies permits for residential or commercial septic repairs, septic-system alterations, plot-plan modifications, and use of an existing septic system or well. These projects therefore should not be treated as permit-free simply because no completely new system is being installed.'),
        ],
    },
]

nc_urls=[]
for d in NC_COUNTIES:
    sources=[
        ('North Carolina Division of Public Health — On-Site Wastewater Program', NC_STATE),
        ('North Carolina Division of Public Health — On-Site Water Protection Branch', NC_BRANCH),
    ] + d['sources']
    sections=[
        ('North Carolina combines statewide oversight with local permitting', 'The North Carolina Division of Public Health On-Site Water Protection Branch provides statewide regulatory oversight and technical guidance for subsurface onsite wastewater treatment and dispersal systems. The state describes the program as a joint effort with local health departments, which carry out much of the property-level permitting and inspection work.')
    ] + d['sections']
    nc_urls.append(write_county_page('North Carolina','north-carolina',d['county'],d['authority'],d['contact'],sections,sources,verified='August 30, 2026'))

links=''.join(f'<li><a href="/counties/north-carolina/{slugify(d["county"])}/">{html.escape(d["county"])} County</a></li>' for d in sorted(NC_COUNTIES,key=lambda x:x['county']))
hub=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>North Carolina Septic Permit Guides by County | SepticScope</title><meta name="description" content="Official-source North Carolina septic permit guides by county."><link rel="canonical" href="https://septicscope.com/counties/north-carolina/"><style>{COMMON_STYLE}</style>{ga_tag}{adsense_tag}</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><p><a href="/counties/">← All county guides</a></p><h1>North Carolina septic permits by county</h1><p>North Carolina provides statewide onsite wastewater oversight through the Division of Public Health while local health departments perform much of the ordinary site evaluation, permitting, and inspection work. SepticScope promotes counties only when useful local procedures are supported by official sources.</p><div class="note">This first verified North Carolina production batch covers Buncombe, Henderson, and Mecklenburg counties. Other North Carolina counties remain on the nationwide lookup layer until their local process is individually validated.</div><h2>Choose a county</h2><ul class="grid">{links}</ul></main><footer><div>© 2026 SepticScope</div></footer></body></html>'''
hubdir=OUTPUT/'counties'/'north-carolina'; hubdir.mkdir(parents=True,exist_ok=True); (hubdir/'index.html').write_text(hub,encoding='utf-8')

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    if '/counties/north-carolina/' not in text:
        promo='<section><h2>North Carolina</h2><p><a href="/counties/north-carolina/">Browse the first 3 verified North Carolina county septic guides →</a></p></section>'
        text=text.replace('</main>',promo+'</main>',1) if '</main>' in text else text.replace('</body>',promo+'</body>',1)
        county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
new_urls=['https://septicscope.com/counties/north-carolina/']+nc_urls
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
    entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in new_urls if u not in sm)
    if entries:
        sitemap.write_text(sm.replace('</urlset>',entries+'</urlset>'),encoding='utf-8')

for d in NC_COUNTIES:
    p=OUTPUT/'counties'/'north-carolina'/slugify(d['county'])/'index.html'
    t=p.read_text(encoding='utf-8')
    if 'Local septic rules not yet verified' in t or 'VERIFIED' not in t.upper() or 'Official sources' not in t:
        raise RuntimeError(f'North Carolina verified page failed: {d["county"]}')

print(f'North Carolina production expansion complete: +{len(nc_urls)} verified county guides')
