# Additional Iowa county guides verified from Iowa DNR and official county sources on 2026-08-30.
IA2_DNR='https://www.iowadnr.gov/environmental-protection/water-quality/private-sewage-disposal-and-septage'
IA2_TOT='https://www.iowadnr.gov/environmental-protection/water-quality/private-sewage-disposal-and-septage/time-transfer'

IA2_COUNTIES=[
{
'county':'Pottawattamie',
'authority':'Pottawattamie County Public Health — Environmental Health / Board of Health',
'contact':'Pottawattamie County Public Health, 227 S 6th St., Council Bluffs, IA 51501; 712-328-5600.',
'sources':[('Pottawattamie County — Septic Systems','https://www.pottcounty-ia.gov/public_health/septic_systems/'),('Pottawattamie County — County Code / Chapter 5.50','https://www.pottcounty-ia.gov/about/county_code/'),('Pottawattamie County — Chapter 5.50 Onsite Wastewater Ordinance','https://www.pottcounty-ia.gov/files/county_code/septic_code_72660.pdf')],
'sections':[
('County Board of Health regulates onsite systems','Pottawattamie County states that onsite wastewater sewage-disposal systems are regulated by the Board of Health under Iowa Administrative Code Chapter 69 and county Chapter 5.50.'),
('Permit, site evaluation, design approval, and final inspection','Permits are required for new septic installations and repairs. Environmental Health inspectors perform site evaluations and approve designs before permit issuance, inspect the completed system before it is covered, and issue a certificate of completion.'),
('New lots must preserve replacement area','The county specifically states that new lots are required to have room for a replacement septic system. Older lots without adequate replacement area may need additional measures such as pretreatment or a Board of Health variance.'),
('Failed or illegal systems must be corrected','Pottawattamie County states that septic systems must be replaced when they have failed, discharge effluent to the ground surface, or are illegal systems such as cesspools.'),
('Time of Transfer review','The county reviews Time of Transfer reports. Iowa law generally requires a certified septic inspection before sale or deed transfer of a septic-served building, subject to state exceptions and binding-agreement procedures.')]
},
{
'county':'Warren',
'authority':'Warren County Environmental Health / Warren County Board of Health',
'contact':'Warren County Environmental Health, 301 N Buxton St., Indianola, IA 50125; 515-690-9190; envhealth@warrencountyia.org.',
'sources':[('Warren County — Septic Systems','https://www.warrencountyia.gov/how-do-i/apply-for/septic/'),('Warren County — County Ordinances','https://www.warrencountyia.gov/government/public-safety/county-ordinances/')],
'sections':[
('Environmental Health handles permits and inspections','Warren County identifies Environmental Health as the primary contact for septic permitting and inspections and states that permits are required for new installations and repairs.'),
('Certified installers are required','The county requires septic contractors to hold the Certified Installer of Onsite Wastewater Treatment Systems (CIOWTS) credential or be approved by the Warren County Board of Health.'),
('Primary and secondary treatment are required','Warren County states that systems must use a septic tank as primary treatment followed by a secondary treatment system complying with Iowa Administrative Code 567 Chapter 69 and Warren County Ordinance Chapter 31.'),
('Local ordinance supplements state standards','Warren County separately codifies Chapter 31, On-Site Wastewater Treatment and Disposal Systems. Applicants should check current county instructions in addition to the state minimum standards.'),
('County publishes professional-resource lists','Warren County publishes resources for certified contractors, maintenance providers, certified pumper inspectors, Time of Transfer inspectors, and soil-analysis professionals.')]
},
{
'county':'Cedar',
'authority':'Cedar County Environmental Health',
'contact':'Cedar County Environmental Health, 400 Cedar St., Basement Level, Tipton, IA 52772; 563-886-2248; ehs@cedarcounty.iowa.gov.',
'sources':[('Cedar County — Septic','https://cedarcounty.iowa.gov/environmental_health/septic/'),('Cedar County — Environmental Health Ordinances','https://cedarcounty.iowa.gov/environmental_health/ordinances/')],
'sections':[
('Environmental Health permits and inspects private sewage systems','Cedar County states that Environmental Health is responsible for inspection and permitting of all private sewage disposal systems in the county and administers local Ordinance No. 28 for onsite wastewater treatment and disposal.'),
('Soil evaluation or perc testing comes before the permit','A soil evaluation and/or percolation test, including a six-foot soil boring, is required before a private sewage disposal permit can be issued. Cedar County states that the testing must be performed by a licensed engineer or approved septic-system contractor.'),
('Inspection is required before covering','No portion of the system may be covered before inspection. Cedar County currently requires inspection requests at least seven and one-half hours in advance and keeps a detailed final drawing of the installed system on file.'),
('Septic approval precedes a new-dwelling building permit','When a system will serve a new dwelling, Cedar County requires the private sewage disposal system permit to be issued before the building permit.'),
('Public sewer availability blocks private septic permitting','Cedar County states that private sewage disposal permits will not be issued to properties that have access to a community or public sewage disposal system.'),
('Time of Transfer inspection applies to sales','The county directs sellers of septic-served homes to complete the required Time of Transfer inspection, consistent with Iowa’s statewide transfer-inspection law.')]
}
]

ia2_urls=[]
for d in IA2_COUNTIES:
    sources=[('Iowa DNR — Private Sewage Disposal and Septage',IA2_DNR),('Iowa DNR — Time of Transfer',IA2_TOT)]+d['sources']
    sections=[('Iowa state and county framework','Iowa DNR states that local boards of health have primary responsibility for private sewage disposal systems serving four homes or fewer or fewer than 15 people. Counties must meet state Chapter 69 minimum standards and may enforce additional local requirements.')]+d['sections']
    ia2_urls.append(write_county_page('Iowa','iowa',d['county'],d['authority'],d['contact'],sections,sources,verified='August 30, 2026'))

# Rebuild the curated Iowa hub with the original four plus this additional validated batch.
all_ia=['Polk','Linn','Story','Johnson']+[d['county'] for d in IA2_COUNTIES]
items=''.join(f'<li><a href="/counties/iowa/{slugify(c)}/">{html.escape(c)} County</a></li>' for c in sorted(all_ia))
hub=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Iowa Septic Permit Guides by County | SepticScope</title><meta name="description" content="Official-source Iowa septic permit guides by county."><link rel="canonical" href="https://septicscope.com/counties/iowa/"><style>{COMMON_STYLE}</style>{ga_tag}{adsense_tag}</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><p><a href="/counties/">← All county guides</a></p><h1>Iowa septic permits by county</h1><p>Iowa DNR establishes minimum private sewage disposal standards while local boards of health have primary responsibility for ordinary private systems. These guides include only counties where current official sources support the local authority and substantive procedures or requirements.</p><div class="note">Seven Iowa county guides are currently locally verified. Additional counties are added only after their local permitting and inspection procedures can be supported from government sources.</div><h2>Verified county guides</h2><ul class="grid">{items}</ul></main><footer><div>© 2026 SepticScope</div></footer></body></html>'''
(OUTPUT/'counties'/'iowa'/'index.html').write_text(hub,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
    entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in ia2_urls if u not in sm)
    if entries: sitemap.write_text(sm.replace('</urlset>',entries+'</urlset>'),encoding='utf-8')

for d in IA2_COUNTIES:
    p=OUTPUT/'counties'/'iowa'/slugify(d['county'])/'index.html'
    t=p.read_text(encoding='utf-8')
    if 'Local septic rules not yet verified' in t or 'VERIFIED' not in t.upper():
        raise RuntimeError(f'Iowa additional verified page failed: {d["county"]}')

print(f'Iowa additional expansion complete: +{len(ia2_urls)} verified county guides; 7 verified Iowa counties total')
