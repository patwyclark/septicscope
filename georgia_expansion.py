# SepticScope Georgia expansion — official-source county pages
# Executed by the root build_site.py after the national bundle and prior expansions are built.
import atexit
import adsense_hardening
import trust_routes

# Register these during the build chain so the compatibility pass runs first at process
# exit, followed by the final AdSense/trust hardening pass.
atexit.register(adsense_hardening.finalize, ROOT)
atexit.register(trust_routes.finalize, ROOT)

GA_STATE = 'https://dph.georgia.gov/environmental-health/onsite-sewage'
GA_CONTACT = 'https://dph.georgia.gov/environmental-health/make-complaint-contact-your-county'
GA_DISTRICT = 'https://www.district4health.org/'
GA_APPLICATION = 'https://www.district4health.org/wp-content/uploads/2024/09/D4-Residential-New-Septic-Permit-Application-20240812.pdf'

GA_COUNTIES = {
    'Butts': ('770-504-2230 ext. 3', '463 Ernest Biles Drive, Suite A, Jackson, GA 30233', 'https://www.district4health.org/locations/butts-county/'),
    'Carroll': ('770-836-6781', '423 College Street, Carrollton, GA 30117', 'https://www.district4health.org/locations/carroll-county/'),
    'Coweta': ('770-683-7345', '22 E. Broad Street, Newnan, GA 30263', 'https://www.district4health.org/locations/coweta-county/'),
    'Fayette': ('943-209-8057', '245 Booker Avenue, Suite E, Fayetteville, GA 30215', 'https://www.district4health.org/locations/fayette-county/'),
    'Heard': ('706-675-3456', '1191 Franklin Parkway, Franklin, GA 30217', 'https://www.district4health.org/locations/heard-county/'),
    'Henry': ('470-661-0044', '137 Henry Parkway, McDonough, GA 30253', 'https://www.district4health.org/locations/henry-county/'),
    'Meriwether': ('706-672-4974', '51 Gay Connector, Greenville, GA 30222', 'https://www.district4health.org/locations/meriwether-county/'),
    'Spalding': ('770-467-4230', '1007 Memorial Drive, Griffin, GA 30224', 'https://www.district4health.org/locations/spalding-county/'),
}

ga_urls = []
ga_links = []
for county, (phone, address, county_url) in GA_COUNTIES.items():
    contact = (
        f'{html.escape(county)} County Environmental Health Office, District 4 Public Health — '
        f'{html.escape(phone)}; {html.escape(address)}. The county office lists wastewater management and '
        'residential septic permit/repair applications among its Environmental Health services.'
    )
    sections = [
        ('County Environmental Health handles the local process',
         'Georgia Department of Public Health directs locally related onsite-sewage questions, records, services and inspections to the County Environmental Health Office. District 4 identifies the county office above as the Environmental Health contact for wastewater management and residential septic permitting.'),
        ('Apply before constructing the septic system',
         'District 4’s residential septic application is an application for a construction permit to install or construct an on-site wastewater management system under Georgia DPH Chapter 511-3-1. Do not treat the application itself as permission to begin work; follow the county office’s review and permit instructions.'),
        ('The site sketch must be detailed',
         'District 4’s application requires a lot sketch showing lot dimensions, the proposed building location and dimensions, building and side-line distances, road name, well locations where applicable, driveway or paved areas, underground utilities, plumbing stub-out, proposed drainfield location, easements and floodplain information, plus detached structures.'),
        ('Final inspection is required before cover',
         'The District 4 application states that final inspection is required and that the County Environmental Health Department must be notified after construction is completed and before final cover is placed over the system.'),
        ('Permit duration',
         'District 4’s current residential application states that the construction permit expires 12 months from its issue date. Confirm any extension or reapplication procedure directly with the county office before relying on an expired permit.'),
        ('Use certified septic professionals',
         'Georgia DPH maintains statewide certified installer and pumper lists through its Onsite Sewage program. Verify that the contractor you plan to use is appropriately certified for the work being performed.')
    ]
    sources = [
        (f'{county} County Environmental Health — District 4 Public Health', county_url),
        ('District 4 residential new septic permit application', GA_APPLICATION),
        ('Georgia DPH — Onsite Sewage', GA_STATE),
        ('Georgia DPH — contact your County Environmental Health Office', GA_CONTACT),
        ('District 4 Public Health — service area', GA_DISTRICT),
    ]
    url = write_county_page(
        'Georgia', 'georgia', county,
        f'{county} County Environmental Health Office, District 4 Public Health',
        contact, sections, sources, verified='August 28, 2026'
    )
    ga_urls.append(url)
    ga_links.append(county)

write_hub(
    'Georgia', 'georgia',
    [(c, 'District 4 Public Health Environmental Health') for c in sorted(ga_links)],
    'Georgia DPH regulates onsite sewage statewide while locally related permits, inspections and records are handled through County Environmental Health Offices. This batch covers eight District 4 counties whose local Environmental Health contacts and residential septic forms were verified.',
    'Only counties with a verified local Environmental Health page and District 4 septic permitting documentation are included in this batch. Additional Georgia counties will be added as their local authority and contact details are validated.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    if '/counties/georgia/' not in text:
        promo = '<section><h2>Georgia</h2><p><a href="/counties/georgia/">Browse 8 verified Georgia county septic guides →</a></p></section>'
        text = text.replace('</main>', promo + '</main>', 1) if '</main>' in text else text.replace('</body>', promo + '</body>', 1)
        county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
new_urls = ['https://septicscope.com/counties/georgia/'] + ga_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-28</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm = sm.replace('</urlset>', entries + '</urlset>')
    sitemap.write_text(sm, encoding='utf-8')

print(f'Georgia expansion complete: +{len(ga_urls)} verified county guides')
exec((ROOT / 'new_mexico_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'south_carolina_expansion.py').read_text(encoding='utf-8'), globals())
