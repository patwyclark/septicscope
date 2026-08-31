"""Last-mile AdSense, trust, privacy, and feedback hardening for SepticScope.

This module is registered by the expansion chain as an atexit callback. It runs after
normal page generation so it can apply deterministic site-wide safeguards without
changing county research data.
"""
from __future__ import annotations

from pathlib import Path
import re
import xml.etree.ElementTree as ET

DOMAIN = "https://septicscope.com"
FEEDBACK_EMAIL = "feedback@septicscope.com"
ADSENSE_CLIENT = "ca-pub-8782868222380999"
GA_ID = "G-F6RB8YERCM"
LASTMOD = "2026-08-31"

STYLE = r''':root{--ink:#17212b;--muted:#5b6672;--line:#dce3e8;--panel:#f7fafb;--accent:#176b5b;--soft:#eaf5f1}*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.68}header{border-bottom:1px solid var(--line)}.nav,main,footer div{max-width:1000px;margin:auto;padding:20px 24px}.brand{font-weight:800;color:var(--ink);text-decoration:none}main{padding-top:42px;padding-bottom:70px}.crumb{font-size:.92rem;color:var(--muted)}h1{font-size:clamp(2rem,5vw,3.2rem);line-height:1.08}h2{margin-top:1.9em}a{color:var(--accent)}.card,.note{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin:22px 0}.note{background:var(--soft)}label{font-weight:700;display:block;margin-top:16px}input,select,textarea{width:100%;padding:12px 13px;margin-top:6px;border:1px solid #bdc9ce;border-radius:9px;font:inherit;color:var(--ink);background:#fff}textarea{min-height:180px;resize:vertical}button{margin-top:18px;padding:12px 17px;border:0;border-radius:9px;background:var(--accent);color:#fff;font:700 1rem/1.2 inherit;cursor:pointer}button:hover,button:focus{filter:brightness(.92)}small,.muted{color:var(--muted)}footer{border-top:1px solid var(--line);color:var(--muted)}'''

ADSENSE_SCRIPT_RE = re.compile(
    r'<script\b[^>]*pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^>]*>\s*</script>',
    flags=re.IGNORECASE,
)


def _write_privacy(site: Path) -> None:
    out = site / "privacy"
    out.mkdir(parents=True, exist_ok=True)
    canonical = f"{DOMAIN}/privacy/"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Privacy Policy | SepticScope</title><meta name="description" content="SepticScope privacy policy covering Google Analytics, Google AdSense, advertising cookies, personalized ads, feedback submissions and external government links."><link rel="canonical" href="{canonical}"><style>{STYLE}</style></head><body>
<header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><div class="crumb"><a href="/">Home</a> / Privacy Policy</div><h1>Privacy Policy</h1><p class="muted">Last updated August 31, 2026</p>
<p>SepticScope is an informational website that helps visitors find septic-system permitting information, official government sources and homeowner guidance. This policy explains the information that may be processed when you use the site.</p>
<h2>Analytics</h2><p>SepticScope uses Google Analytics to understand aggregate site usage, such as pages viewed, approximate traffic sources, device or browser information and interaction patterns. Google Analytics may use cookies or similar technologies. We use this information to improve navigation, find broken or unhelpful pages and understand which guides visitors use.</p>
<h2>Advertising, Google AdSense and cookies</h2><p>SepticScope uses Google AdSense to support the site with advertising. <strong>Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites.</strong> Google's advertising cookies enable Google and its partners to serve ads based on visits to SepticScope and/or other sites on the Internet.</p>
<p>Users may opt out of personalized advertising through <a href="https://adssettings.google.com/" rel="nofollow">Google Ads Settings</a>. You can also learn more about how Google uses information for advertising at <a href="https://policies.google.com/technologies/ads" rel="nofollow">Google's advertising technologies page</a>. If additional third-party advertising vendors or networks are added, this policy will be updated with the relevant disclosures and opt-out information.</p>
<h2>Consent choices</h2><p>Where privacy law or Google's advertising requirements call for a consent choice, the site or Google's consent tools may ask you to manage advertising or cookie preferences. Your available choices can vary by region and by the services active on the site.</p>
<h2>Feedback and contact information</h2><p>If you contact SepticScope or submit feedback, the information you choose to provide may include your name, email address, the page you are reporting and the contents of your message. We use that information to respond, investigate corrections, repair broken links and improve the site. Do not submit passwords, financial account details, medical information or other sensitive personal information through the feedback form.</p>
<h2>External government and third-party links</h2><p>County guides intentionally link to state, county, municipal, public-health, environmental-health and other official websites. SepticScope does not control those sites. Their privacy policies, cookies and data practices apply when you visit them.</p>
<h2>Children</h2><p>SepticScope is a general informational resource for property owners, homebuyers and professionals and is not directed to children under 13.</p>
<h2>Policy changes</h2><p>This policy may be updated when site features, analytics, advertising providers or applicable requirements change. The latest revision date is shown above.</p>
<h2>Contact</h2><p>For privacy questions, corrections or site feedback, use the <a href="/contact/">Contact &amp; Feedback page</a> or email <a href="mailto:{FEEDBACK_EMAIL}">{FEEDBACK_EMAIL}</a>.</p>
</main><footer><div>© 2026 SepticScope · <a href="/about/">About</a> · <a href="/contact/">Contact &amp; Feedback</a></div></footer></body></html>'''
    (out / "index.html").write_text(page, encoding="utf-8")


def _write_contact(site: Path) -> None:
    out = site / "contact"
    out.mkdir(parents=True, exist_ok=True)
    canonical = f"{DOMAIN}/contact/"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Contact &amp; Feedback | SepticScope</title><meta name="description" content="Send SepticScope feedback, report an outdated county septic requirement, submit a corrected official source, or report a broken local government link."><link rel="canonical" href="{canonical}"><style>{STYLE}</style></head><body>
<header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><div class="crumb"><a href="/">Home</a> / Contact &amp; Feedback</div><h1>Contact &amp; Feedback</h1>
<p>Use this page to report outdated septic information, a broken government link, a missing county resource or general feedback about SepticScope. County corrections are especially useful when you can include the current official agency page.</p>
<div class="note"><strong>Permit or septic emergency?</strong> SepticScope does not issue permits and cannot provide emergency field service. Contact the health, environmental or permitting authority shown in the applicable county guide.</div>
<form id="feedback-form">
<label for="kind">Feedback type</label><select id="kind" required><option value="County information correction">County information correction</option><option value="Broken official link">Broken official link</option><option value="Missing county/local source">Missing county/local source</option><option value="General website feedback">General website feedback</option><option value="Other">Other</option></select>
<label for="page">Page or county URL</label><input id="page" type="url" inputmode="url" placeholder="https://septicscope.com/counties/..."><label for="name">Your name <span class="muted">(optional)</span></label><input id="name" autocomplete="name"><label for="reply">Your email <span class="muted">(optional, for a reply)</span></label><input id="reply" type="email" autocomplete="email"><label for="message">Feedback</label><textarea id="message" required placeholder="Tell us what should be corrected or improved. For county information, include the official local source if you have it."></textarea><button type="submit">Prepare feedback email</button><p class="muted"><small>The form opens your email app with the information filled in. Nothing is transmitted by this webpage until you send the email.</small></p></form>
<div class="card"><strong>Prefer email?</strong><p>Email <a href="mailto:{FEEDBACK_EMAIL}">{FEEDBACK_EMAIL}</a>. For a county correction, include the SepticScope page URL and the official county, health-department or permitting-agency source that supports the change.</p></div>
</main><footer><div>© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a></div></footer>
<script>(function(){{const f=document.getElementById('feedback-form'),page=document.getElementById('page');if(!page.value&&document.referrer&&document.referrer.indexOf(location.origin)===0)page.value=document.referrer;f.addEventListener('submit',function(e){{e.preventDefault();const kind=document.getElementById('kind').value,name=document.getElementById('name').value.trim(),reply=document.getElementById('reply').value.trim(),msg=document.getElementById('message').value.trim(),url=page.value.trim();const subject='SepticScope feedback: '+kind;const body=['Feedback type: '+kind,'Page: '+(url||'Not provided'),'Name: '+(name||'Not provided'),'Reply email: '+(reply||'Not provided'),'','Feedback:',''+msg].join('\n');location.href='mailto:{FEEDBACK_EMAIL}?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);}});}})();</script></body></html>'''
    (out / "index.html").write_text(page, encoding="utf-8")


def _strip_adsense(text: str) -> str:
    return ADSENSE_SCRIPT_RE.sub("", text)


def _is_verified_county(path: Path, site: Path, text: str) -> bool:
    try:
        parts = path.relative_to(site).parts
    except ValueError:
        return False
    if len(parts) != 4 or parts[0] != "counties" or parts[-1] != "index.html":
        return False
    lower = text.lower()
    return "noindex" not in lower and "official sources" in lower and "permitting authority" in lower


def _harden_existing_pages(site: Path) -> tuple[int, int, int]:
    footer_updates = 0
    county_updates = 0
    ad_suppressed = 0
    for html_file in site.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8", errors="replace")
        original = text
        rel = html_file.relative_to(site).as_posix()
        lower = text.lower()

        # Do not allow Auto ads on intentionally unfinished/noindex utility pages or
        # policy/contact pages. These pages exist for navigation, trust or assistance,
        # not as monetized content destinations.
        if "local guide in progress" in lower or "name=\"robots\" content=\"noindex" in lower or rel in {"privacy/index.html", "contact/index.html", "404.html"}:
            stripped = _strip_adsense(text)
            if stripped != text:
                ad_suppressed += 1
                text = stripped

        # Add the public feedback route to the fixed menu created by site_ui_fix.py.
        menu_anchor = '<a href="/about/">About</a>'
        menu_contact = '<a href="/contact/">Contact &amp; Feedback</a>'
        if "septicscope-fixed-menu" in text and menu_contact not in text and menu_anchor in text:
            text = text.replace(menu_anchor, menu_anchor + menu_contact, 1)

        # Make Contact & Feedback discoverable from every page that already has a footer.
        if "</footer>" in text and 'href="/contact/"' not in text[text.rfind("<footer"):]:
            text = text.replace("</footer>", '<p style="max-width:1000px;margin:0 auto;padding:0 24px 18px"><a href="/contact/">Contact &amp; Feedback</a></p></footer>', 1)
            footer_updates += 1

        if _is_verified_county(html_file, site, text) and "Report outdated county information" not in text:
            feedback = '<div class="note"><strong>Report outdated county information</strong><p>Septic rules, forms and agency pages can change. If you find a broken official link or a county requirement that has changed, <a href="/contact/">send SepticScope feedback</a> and include the current local government source.</p></div>'
            if "</main>" in text:
                text = text.replace("</main>", feedback + "</main>", 1)
                county_updates += 1

        if text != original:
            html_file.write_text(text, encoding="utf-8")

    return footer_updates, county_updates, ad_suppressed


def _ensure_sitemap(site: Path) -> None:
    sitemap = site / "sitemap.xml"
    if not sitemap.exists():
        return
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    tree = ET.parse(sitemap)
    root = tree.getroot()
    existing = {((node.find(f"{{{ns}}}loc").text or "").strip()) for node in root.findall(f"{{{ns}}}url") if node.find(f"{{{ns}}}loc") is not None}
    for slug in ("privacy", "about", "contact"):
        url = f"{DOMAIN}/{slug}/"
        if url in existing:
            continue
        node = ET.SubElement(root, f"{{{ns}}}url")
        ET.SubElement(node, f"{{{ns}}}loc").text = url
        ET.SubElement(node, f"{{{ns}}}lastmod").text = LASTMOD
    tree.write(sitemap, encoding="utf-8", xml_declaration=True)


def finalize(root: Path | str | None = None) -> None:
    repo = Path(root) if root is not None else Path(__file__).resolve().parent
    site = repo / "site"
    if not site.is_dir():
        return
    _write_privacy(site)
    _write_contact(site)
    footer_updates, county_updates, ad_suppressed = _harden_existing_pages(site)
    # Re-write policy/contact pages after the global pass so they stay deliberately ad-free.
    _write_privacy(site)
    _write_contact(site)
    _ensure_sitemap(site)
    print(
        "AdSense hardening complete: "
        f"feedback links on {footer_updates} pages; "
        f"county feedback prompts on {county_updates} verified guides; "
        f"AdSense suppressed on {ad_suppressed} non-content/noindex pages"
    )
