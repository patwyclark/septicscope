# Refresh Washington navigation after the fourth verified county batch.
existing_wa = {county: authority for county, authority in wa_links}
for d in WA4_COUNTIES:
    existing_wa[d['county']] = d['authority']
wa_links[:] = sorted(existing_wa.items())
write_hub(
    'Washington', 'washington', wa_links,
    'Washington delegates onsite sewage system permitting and management to local health jurisdictions. SepticScope adds counties only after the responsible local agency and meaningful local requirements are validated from government sources.',
    'This Washington set now includes 18 verified counties. Local design, installer, inspection, repair, operating-permit, maintenance, and building-clearance requirements are documented county-by-county rather than inferred statewide.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    text = text.replace('Browse 15 verified Washington county septic guides →', 'Browse 18 verified Washington county septic guides →')
    county_index.write_text(text, encoding='utf-8')

hub_text = (OUTPUT / 'counties' / 'washington' / 'index.html').read_text(encoding='utf-8')
for county in ('Kitsap', 'Skagit', 'Jefferson'):
    if f'/counties/washington/{slugify(county)}/' not in hub_text:
        raise RuntimeError(f'Washington hub missing fourth-batch county: {county}')
if '18 verified counties' not in hub_text:
    raise RuntimeError('Washington hub verified-county count was not refreshed')

print('Washington hub refreshed for 18 verified county guides')
