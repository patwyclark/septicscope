# SepticScope New York expansion — verified county batch.
# Verified from NYSDOH and official county government sources on 2026-08-30.

NY_APPENDIX = 'https://regs.health.ny.gov/content/appendix-75-a2-regulation-other-agencies'
NY_REGS = 'https://healthweb-back.health.ny.gov/environmental/water/drinking/regulations/'

NY_COUNTIES = [
    {
        'county': 'Suffolk',
        'authority': 'Suffolk County Department of Health Services — Office of Wastewater Management',
        'contact': 'Suffolk County Department of Health Services, Office of Wastewater Management; 631-852-5700. The office reviews and permits sewage disposal and water-supply facilities for new and modified development.',
        'sources': [
            ('Suffolk County — Office of Wastewater Management', 'https://suffolkcountyny.gov/Departments/Health-Services/WWM'),
        ],
        'sections': [
            ('County wastewater approval is required for new homes and businesses', 'Suffolk County states that a new home or business requires a permit from the Department of Health Services Office of Wastewater Management. Modifications to an existing home or business may also require county approval to confirm that the existing or proposed sewage disposal system complies with the Suffolk County Sanitary Code.'),
            ('Applications require signed forms, checklists, and design plans', 'The county’s current wastewater workflow requires a signed application, mandatory checklist, and design or site plans before an application is accepted into formal review. For single-family residential work, Suffolk also identifies the applicable residential application forms, surveys, and floor plans as part of the submission.'),
            ('Approval to construct is followed by inspection and as-built documentation', 'Suffolk County explains that the initial wastewater approval authorizes construction. After construction is complete, an inspection must be requested before use; following a satisfactory field inspection, as-built plans are submitted to the Office of Wastewater Management.'),
            ('Residential and commercial construction approvals are generally valid three years', 'Suffolk County states that residential and commercial wastewater approvals to construct are valid for three years. An extension may be requested, and work beginning outside the approved period requires the applicant to reapply.'),
            ('Cesspool replacement rules are locally significant', 'Suffolk County specifically publishes requirements implementing its sanitary-code amendment eliminating cesspool replacements. Owners replacing a failed or obsolete disposal system should follow the current county replacement standards rather than assuming another cesspool can be installed.'),
            ('Other town, sewer-district, water, or wetland approvals may also apply', 'Suffolk County warns that town planning, zoning or building approvals can be separate from Health Department approval. Properties in sewer or public-water districts, or near regulated wetlands, may require additional county, local, or state approvals.'),
        ],
    },
    {
        'county': 'Broome',
        'authority': 'Broome County Health Department — Division of Environmental Health',
        'contact': 'Broome County Health Department Environmental Health; septic questions and correspondence: BCSewage@broomecountyny.gov or 607-778-2847. The division enforces residential onsite wastewater standards and issues sewage disposal construction permits.',
        'sources': [
            ('Broome County — Wastewater Treatment / Septic Systems', 'https://www.broomecountyny.gov/eh/wastewatertreatment'),
        ],
        'sections': [
            ('Environmental Health enforces Appendix 75-A locally', 'Broome County states that its Environmental Health Division enforces the residential onsite wastewater standards in 10 NYCRR Appendix 75-A. Staff investigate failing systems, assist homeowners, review and approve designs, inspect work, and issue sewage disposal construction permits.'),
            ('A county sewage permit is required for new systems under 1,000 gallons per day', 'Broome County publishes a Sewage Permit Application that it identifies as required for all new septic-system installations with design flow below 1,000 gallons per day.'),
            ('County review relies on a New York licensed engineer for design work', 'Broome County explicitly states that it does not perform percolation tests or design septic systems. Those services are provided by a New York State licensed engineer, whose design is then reviewed through the county Environmental Health process.'),
            ('Enhanced treatment units have a separate county agreement/application path', 'When an enhanced treatment unit is proposed, Broome County publishes a separate ETU agreement/application form in addition to the ordinary sewage permit process.'),
            ('Larger systems move into additional state regulation', 'Broome County states that systems producing more than 1,000 gallons per day require additional regulation under New York State Department of Environmental Conservation SPDES requirements and state standards for intermediate-sized wastewater treatment systems.'),
            ('The county also registers septic installers', 'Broome County maintains a registered-contractor program and provides septic-system installer certification information, adding a local contractor-qualification step beyond the statewide design standard.'),
        ],
    },
    {
        'county': 'Monroe',
        'authority': 'Monroe County Department of Public Health — Bureau of Public Health Engineering, Onsite Wastewater Treatment Systems Program',
        'contact': 'Monroe County Department of Public Health, 111 Westfall Road, Room 844, Rochester, NY 14620; onsite wastewater program 585-753-5060. The county reviews, approves, and inspects new and repaired onsite wastewater treatment systems.',
        'sources': [
            ('Monroe County — Onsite Wastewater Treatment Systems', 'https://www.monroecounty.gov/eh-individualsewagetreatment'),
        ],
        'sections': [
            ('County sanitary code governs local onsite approvals', 'Monroe County states that its program ensures onsite wastewater treatment systems are properly designed and constructed under Article IIA and Article III of the Monroe County Sanitary Code. The county witnesses field testing, reviews plans, issues approvals, inspects construction, and investigates complaints.'),
            ('A design professional must prepare the construction plan', 'Before an onsite wastewater treatment system can be constructed, Monroe County requires a plan prepared by a design professional showing the system placement on the property. Application materials, plans, and reports are submitted to the Department of Public Health for review.'),
            ('County staff witness percolation tests and deep holes', 'Monroe County identifies witnessing field testing, including percolation tests and deep holes, as part of its onsite wastewater program. This gives the county a direct role in validating the site information used for system design.'),
            ('Both new systems and repairs require county construction inspection', 'Monroe County requires a Department of Public Health representative to perform construction inspections for wastewater treatment facilities installed for both new development and repairs.'),
            ('Repair applications are project-specific', 'The county publishes full and partial septic-system repair permit applications and advises that the exact submission requirements for an existing-system repair vary by project. Owners should confirm the required repair package before excavation begins.'),
            ('County standards supplement the statewide minimum', 'Monroe County enforces its own sanitary-code provisions and publishes local design and construction standards and a plan-review submission guide. Those county requirements apply in addition to the New York statewide minimum standards.'),
        ],
    },
]

ny_urls=[]
for d in NY_COUNTIES:
    sources=[
        ('New York State Department of Health — Residential Sanitation Regulations', NY_REGS),
        ('10 NYCRR Appendix 75-A.2 — Regulation by other agencies', NY_APPENDIX),
    ] + d['sources']
    sections=[
        ('New York sets statewide minimum standards but allows stricter local rules', 'New York State Department of Health Appendix 75-A establishes statewide minimum standards for residential onsite wastewater treatment systems. Appendix 75-A.2 expressly allows local health departments and other agencies to impose more stringent standards, and where stricter local standards apply, the stricter standard controls. That makes county-level permitting and design guidance important in jurisdictions with active local health programs.')
    ] + d['sections']
    ny_urls.append(write_county_page('New York','new-york',d['county'],d['authority'],d['contact'],sections,sources,verified='August 30, 2026'))

links=''.join(f'<li><a href="/counties/new-york/{slugify(d["county"])}/">{html.escape(d["county"])} County</a></li>' for d in sorted(NY_COUNTIES,key=lambda x:x['county']))
hub=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>New York Septic Permit Guides by County | SepticScope</title><meta name="description" content="Official-source New York septic permit guides by county."><link rel="canonical" href="https://septicscope.com/counties/new-york/"><style>{COMMON_STYLE}</style>{ga_tag}{adsense_tag}</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><p><a href="/counties/">← All county guides</a></p><h1>New York septic permits by county</h1><p>New York establishes statewide residential onsite wastewater minimum standards in Appendix 75-A, but local health departments may impose stricter requirements. SepticScope promotes counties only when the local authority and substantive county procedures are supported by official sources.</p><div class="note">This first verified New York batch covers Suffolk, Broome, and Monroe counties. Other New York counties remain on the nationwide lookup layer until their local process is individually validated.</div><h2>Choose a county</h2><ul class="grid">{links}</ul></main><footer><div>© 2026 SepticScope</div></footer></body></html>'''
hubdir=OUTPUT/'counties'/'new-york'; hubdir.mkdir(parents=True,exist_ok=True); (hubdir/'index.html').write_text(hub,encoding='utf-8')

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    if '/counties/new-york/' not in text:
        promo='<section><h2>New York</h2><p><a href="/counties/new-york/">Browse the first 3 verified New York county septic guides →</a></p></section>'
        text=text.replace('</main>',promo+'</main>',1) if '</main>' in text else text.replace('</body>',promo+'</body>',1)
        county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
new_urls=['https://septicscope.com/counties/new-york/']+ny_urls
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
    entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in new_urls if u not in sm)
    if entries:
        sitemap.write_text(sm.replace('</urlset>',entries+'</urlset>'),encoding='utf-8')

for d in NY_COUNTIES:
    p=OUTPUT/'counties'/'new-york'/slugify(d['county'])/'index.html'
    t=p.read_text(encoding='utf-8')
    if 'Local septic rules not yet verified' in t or 'VERIFIED' not in t.upper() or 'Official sources' not in t:
        raise RuntimeError(f'New York verified page failed: {d["county"]}')

print(f'New York expansion complete: +{len(ny_urls)} verified county guides')
