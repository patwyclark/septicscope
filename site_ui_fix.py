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

home = OUTPUT / 'index.html'
if not home.exists() or 'data-septicscope-menu-fix="v1"' not in home.read_text(encoding='utf-8'):
    raise RuntimeError('Site UI repair failed: menu handler was not injected into homepage')

print(f'Site-wide menu repair injected into {fixed} HTML pages')
