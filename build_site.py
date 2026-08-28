from pathlib import Path
import base64, hashlib, io, os, shutil, subprocess, sys, zipfile

ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / 'bundle'
WORK = ROOT / '.septicscope-build'
OUTPUT = ROOT / 'site'
EXPECTED_SHA256 = 'f46d80d1b8f3a928253457e117192ba425a7f7298d474f58511fa53d7ca4394f'
PARTS = ['part00a.txt','part00b.txt','part01.txt','part02.txt','part03.txt','part04.txt','part05.txt','part06.txt','part07.txt','part08.txt']
GA_MEASUREMENT_ID = 'G-F6RB8YERCM'
ADSENSE_CLIENT = 'ca-pub-8782868222380999'
ADSENSE_PUBLISHER_ID = 'pub-8782868222380999'

payload = ''.join((BUNDLE / name).read_text(encoding='utf-8').strip() for name in PARTS)
archive = base64.b64decode(payload, validate=True)
actual = hashlib.sha256(archive).hexdigest()
if actual != EXPECTED_SHA256:
    raise RuntimeError(f'Deploy bundle checksum mismatch: {actual}')

if WORK.exists():
    shutil.rmtree(WORK)
if OUTPUT.exists():
    shutil.rmtree(OUTPUT)
WORK.mkdir()

with zipfile.ZipFile(io.BytesIO(archive)) as z:
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

shutil.rmtree(WORK)
print(f'SepticScope build complete: {OUTPUT}')
