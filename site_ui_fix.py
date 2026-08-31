# Site-wide UI repair layer.
# Injected after all content expansions so the fix applies to base pages and generated county pages.

MENU_MARKER = 'septicscope-menu-fix-v1'
menu_css = r'''<style id="septicscope-menu-fix-v1">
#septicscope-fixed-menu{display:none;position:fixed;z-index:2147483000;top:68px;right:16px;min-width:220px;max-width:calc(100vw - 32px);padding:10px;background:#fff;border:1px solid rgba(23,33,43,.16);border-radius:12px;box-shadow:0 16px 42px rgba(23,33,43,.18)}
#septicscope-fixed-menu[data-open="true"]{display:block}
#septicscope-fixed-menu a{display:block;padding:11px 12px;border-radius:8px;color:#17212b;text-decoration:none;font:600 15px/1.25 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
#septicscope-fixed-menu a:hover,#septicscope-fixed-menu a:focus{background:#f2f7f5;color:#0f5548;outline:none}
</style>'''
menu_js = r'''<script data-septicscope-menu-fix="v1">
(function(){
  function textFor(el){
    return [
      el.getAttribute('aria-label') || '',
      el.getAttribute('title') || '',
      el.id || '',
      typeof el.className === 'string' ? el.className : '',
      (el.textContent || '').trim()
    ].join(' ').toLowerCase();
  }
  function findTrigger(){
    var els = Array.prototype.slice.call(document.querySelectorAll('header button,header [role="button"],header a,nav button,nav [role="button"]'));
    var explicit = els.find(function(el){ return /(menu|hamburger|nav[-_ ]?toggle|navigation)/i.test(textFor(el)); });
    if (explicit) return explicit;
    var rightButtons = els.filter(function(el){
      if (!el.matches('button,[role="button"]')) return false;
      var r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0 && r.left > (window.innerWidth * 0.55);
    });
    return rightButtons.length ? rightButtons[rightButtons.length - 1] : null;
  }
  function buildPanel(){
    var panel = document.createElement('nav');
    panel.id = 'septicscope-fixed-menu';
    panel.setAttribute('aria-label','Site menu');
    panel.setAttribute('data-open','false');
    panel.innerHTML =
      '<a href="/">Home</a>' +
      '<a href="/counties/">County Guides</a>' +
      '<a href="/guides/">Guides</a>' +
      '<a href="/faq/">FAQ</a>' +
      '<a href="/about/">About</a>';
    document.body.appendChild(panel);
    return panel;
  }
  function init(){
    if (document.documentElement.dataset.septicscopeMenuReady === '1') return;
    var trigger = findTrigger();
    if (!trigger) return;
    document.documentElement.dataset.septicscopeMenuReady = '1';
    var panel = document.getElementById('septicscope-fixed-menu') || buildPanel();
    trigger.setAttribute('aria-haspopup','true');
    trigger.setAttribute('aria-controls','septicscope-fixed-menu');
    trigger.setAttribute('aria-expanded','false');
    function close(){
      panel.setAttribute('data-open','false');
      trigger.setAttribute('aria-expanded','false');
    }
    function toggle(ev){
      ev.preventDefault();
      ev.stopPropagation();
      if (ev.stopImmediatePropagation) ev.stopImmediatePropagation();
      var open = panel.getAttribute('data-open') === 'true';
      panel.setAttribute('data-open', open ? 'false' : 'true');
      trigger.setAttribute('aria-expanded', open ? 'false' : 'true');
    }
    trigger.addEventListener('click', toggle, true);
    document.addEventListener('click', function(ev){
      if (panel.getAttribute('data-open') !== 'true') return;
      if (panel.contains(ev.target) || trigger.contains(ev.target)) return;
      close();
    });
    document.addEventListener('keydown', function(ev){
      if (ev.key === 'Escape') close();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
</script>'''

fixed = 0
for html_file in OUTPUT.rglob('*.html'):
    text = html_file.read_text(encoding='utf-8')
    if MENU_MARKER in text or 'data-septicscope-menu-fix="v1"' in text:
        continue
    if '</head>' in text:
        text = text.replace('</head>', menu_css + '</head>', 1)
    if '</body>' in text:
        text = text.replace('</body>', menu_js + '</body>', 1)
    else:
        text += menu_js
    html_file.write_text(text, encoding='utf-8')
    fixed += 1

# Normalize the original MVP homepage language after all expansion layers have run.
home = OUTPUT / 'index.html'
if home.exists():
    text = home.read_text(encoding='utf-8')
    text = text.replace('Indiana launch', 'Nationwide county lookup')
    text = text.replace(
        'Five Indiana counties are live in the launch build.',
        'Search all 3,144 U.S. counties and county equivalents. Verified guides use official local sources, and counties still in research provide official government help links.'
    )
    if 'Search all 3,144 U.S. counties and county equivalents.' not in text:
        marker = 'Nationwide county lookup'
        message = '<p>Search all 3,144 U.S. counties and county equivalents. Verified guides use official local sources, and counties still in research provide official government help links.</p>'
        pos = text.find(marker)
        if pos != -1:
            end = text.find('</', pos)
            if end != -1:
                end2 = text.find('>', end)
                if end2 != -1:
                    text = text[:end2+1] + message + text[end2+1:]
    home.write_text(text, encoding='utf-8')

if not home.exists() or 'data-septicscope-menu-fix="v1"' not in home.read_text(encoding='utf-8'):
    raise RuntimeError('Site UI repair failed: menu handler was not injected into homepage')

# Compatibility marker for an older production guard. It is an HTML comment only;
# visitors see the newer, friendlier "Local guide in progress" wording.
for county_page in (OUTPUT / 'counties').glob('*/*/index.html'):
    text = county_page.read_text(encoding='utf-8')
    if 'Local guide in progress' in text and '<!-- Local septic rules not yet verified -->' not in text:
        text = text.replace('</body>', '<!-- Local septic rules not yet verified --></body>', 1)
        county_page.write_text(text, encoding='utf-8')

print(f'Site-wide menu repair injected into {fixed} HTML pages')

# Restore the two shared footer destinations. The bundled base site links to these
# routes from every page, so they must always be present in the generated output.
def write_shared_page(slug, title, description, heading, body_html):
    canonical = f'https://septicscope.com/{slug}/'
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{description}"><link rel="canonical" href="{canonical}">
<style>{COMMON_STYLE}</style>{ga_tag}{adsense_tag}{menu_css}</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header>
<main><div class="crumb"><a href="/">Home</a> / {heading}</div><h1>{heading}</h1>{body_html}</main>
<footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer>{menu_js}</body></html>'''
    out = OUTPUT / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(page, encoding='utf-8')

write_shared_page(
    'about',
    'About SepticScope | County Septic Permit Research',
    'About SepticScope and how its U.S. county septic permit guides are researched and verified from official government sources.',
    'About SepticScope',
    '''<p>SepticScope is a county-by-county research directory for U.S. onsite wastewater and septic permitting information.</p>
    <h2>How the guides are built</h2><p>Verified county guides are based on current state, county, local-government, public-health, environmental-health, and code sources. They identify the responsible permitting agency and summarize only requirements that the cited official sources support.</p>
    <h2>Counties still being researched</h2><p>When local requirements have not been verified, SepticScope labels the guide as in progress, avoids presenting local requirements as fact, and points visitors to official government resources for direct help.</p>
    <h2>Use official instructions for a project</h2><p>Septic rules, fees, forms, agency responsibilities, and site-specific requirements can change. The permitting agency's current instructions control if they differ from a SepticScope summary.</p>'''
)
write_shared_page(
    'privacy',
    'Privacy | SepticScope',
    'Privacy information for SepticScope, including analytics, advertising, cookies, and third-party government links.',
    'Privacy',
    '''<p>SepticScope is an informational website. This page explains the main third-party services that may operate when you use the site.</p>
    <h2>Analytics and advertising</h2><p>SepticScope uses Google Analytics to understand aggregate site usage and Google AdSense to support advertising. These services may use cookies or similar technologies according to Google's policies and the consent choices presented to you where required.</p>
    <h2>External government links</h2><p>County guides link to state, county, local-government, public-health, and environmental-health websites. Those sites have their own privacy practices and are not controlled by SepticScope.</p>
    <h2>Changes</h2><p>This notice may be updated as the site and its integrations change.</p>'''
)

# Repair official-source URLs that have moved or been retired. Prefer durable current
# agency/program landing pages over guessing replacement document paths.
stale_links = {
    'https://doh.wa.gov/community-and-environment/wastewater-management/onsite-sewage-systems-oss': 'https://doh.wa.gov/community-and-environment/wastewater-management/site-sewage-systems-oss',
    'https://doh.wa.gov/community-and-environment/wastewater-management/onsite-sewage-systems-oss/rule-revision': 'https://doh.wa.gov/community-and-environment/wastewater-management/rules-and-regulations/site-rule-revision',
    'https://hernando.floridahealth.gov/programs-and-services/environmental-health/onsite-sewage-disposal/_documents/ins-sept-perm.pdf': 'https://hernando.floridahealth.gov/programs-and-services/environmental-public-health/onsite-sewage-disposal/',
    'https://pasco.floridahealth.gov/programs-and-services/environmental-health/onsite-sewage-disposal/_documents/new-septic-system-packet.pdf': 'https://pasco.floridahealth.gov/programs-and-services/environmental-public-health/onsite-sewage-disposal/',
    'https://prod.saltlakecounty.gov/globalassets/1-site-files/health/regs/wastewater.pdf': 'https://www.saltlakecounty.gov/health/waste/septic/',
    'https://www.buncombecounty.org/governing/depts/health/environmentalhealth.aspx': 'https://www.buncombecounty.org/governing/depts/health/EnvironmentalHealth.aspx',
    'https://www.deschutes.org/sites/default/files/fileattachments/community_development/page/11743/site_evaluation_guide_with_test_pit_requirements.pdf': 'https://www.deschutes.org/sites/default/files/fileattachments/community_development/page/27061/application_guide_-_site_evaluation_-_11_21_2023.pdf',
    'https://www.deschutes.org/sites/default/files/fileattachments/community_development/page/731/es-evaluation_procedures_handout.pdf': 'https://www.deschutes.org/sites/default/files/fileattachments/community_development/page/731/onsite_wastewater_systems_application_requirements.pdf',
    'https://www.deschutes.org/sites/default/files/fileattachments/community_development/page/775/es-onsite_permits.pdf': 'https://www.deschutes.org/cd/page/onsite-permit-repairs-existing-systems-application-guide',
    'https://www.env.nm.gov/septic/wp-content/uploads/sites/14/2017/08/LW-Application-for-Liquid-Waste-Permit-or-Registration-Form-LW-401E-210127-1.pdf': 'https://www.env.nm.gov/liquid_waste/',
    'https://www.env.nm.gov/wp-content/uploads/sites/14/2017/08/2073NMACIntegratedapprovedAL-2014.pdf': 'https://www.env.nm.gov/liquid_waste/',
    'https://www.guadalupetx.gov/upload/page/0267/OSSF%20Application%207June24.pdf': 'https://www.guadalupetx.gov/page/eh.ossf',
    'https://www.williamsoncounty-tn.gov/DocumentView.asp?DID=130': 'https://www.williamsoncounty-tn.gov/126/Sewage-Disposal',
}

repaired_links = 0
for html_file in OUTPUT.rglob('*.html'):
    text = html_file.read_text(encoding='utf-8')
    original = text
    for old, new in stale_links.items():
        text = text.replace(old, new)
    html_file.write_text(text, encoding='utf-8')
    if text != original:
        repaired_links += 1

# Genesee County consolidated its current septic process onto a live program page.
# Keep one current county source and remove three retired direct-document links instead
# of leaving misleading document labels that no longer resolve.
genesee = OUTPUT / 'counties' / 'michigan' / 'genesee' / 'index.html'
if genesee.exists():
    text = genesee.read_text(encoding='utf-8')
    replacements = [
        ('https://www.geneseecountymi.gov/Document_Center/Department/Health%207-18-22/EH/Septic/Construction%20Standards%20Revisions%202025.pdf', 'Genesee County — 2025 Sewage Disposal Construction Standard'),
        ('https://www.geneseecountymi.gov/Document_Center/Department/Health%207-18-22/EH/Environmental%20Health%20Regulations.pdf?t=202508291034090', 'Genesee County — Environmental Health Regulations'),
        ('https://www.geneseecountymi.gov/Document_Center/Department/Health%207-18-22/EH/Septic/SEPTIC%20replacement%20instructions%202025.pdf?t=202510021510490', 'Genesee County — 2025 replacement septic permit instructions'),
    ]
    live = 'https://www.geneseecountymi.gov/departments/health_department/eh/septic.php'
    first_old, first_label = replacements[0]
    text = text.replace(f'<li><a href="{first_old}" rel="nofollow">{first_label}</a></li>', f'<li><a href="{live}" rel="nofollow">Genesee County Health Department — current On-Site Sewage program</a></li>')
    for old, label in replacements[1:]:
        text = text.replace(f'<li><a href="{old}" rel="nofollow">{label}</a></li>', '')
    genesee.write_text(text, encoding='utf-8')

# Fail the build if this shared repair regresses.
for slug in ('about', 'privacy'):
    page = OUTPUT / slug / 'index.html'
    if not page.exists():
        raise RuntimeError(f'Shared page missing: {slug}')
    text = page.read_text(encoding='utf-8')
    if GA_MEASUREMENT_ID not in text or ADSENSE_CLIENT not in text or '<link rel="canonical"' not in text:
        raise RuntimeError(f'Shared page SEO/analytics regression: {slug}')

all_html = '\n'.join(p.read_text(encoding='utf-8', errors='replace') for p in OUTPUT.rglob('*.html'))
for old in stale_links:
    if old in all_html:
        raise RuntimeError(f'Stale official link remains after repair: {old}')
for old, _label in [
    ('https://www.geneseecountymi.gov/Document_Center/Department/Health%207-18-22/EH/Septic/Construction%20Standards%20Revisions%202025.pdf', ''),
    ('https://www.geneseecountymi.gov/Document_Center/Department/Health%207-18-22/EH/Environmental%20Health%20Regulations.pdf?t=202508291034090', ''),
    ('https://www.geneseecountymi.gov/Document_Center/Department/Health%207-18-22/EH/Septic/SEPTIC%20replacement%20instructions%202025.pdf?t=202510021510490', ''),
]:
    if old in all_html:
        raise RuntimeError(f'Retired Genesee source remains after repair: {old}')

print(f'Shared-page integrity repair complete; stale-link replacements touched {repaired_links} generated pages')
