from pathlib import Path
import base64, hashlib, io, shutil, subprocess, sys, zipfile

ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / 'bundle'
WORK = ROOT / '.septicscope-build'
OUTPUT = ROOT / 'site'
EXPECTED_SHA256 = 'f46d80d1b8f3a928253457e117192ba425a7f7298d474f58511fa53d7ca4394f'
PARTS = ['part00a.txt','part00b.txt','part01.txt','part02.txt','part03.txt','part04.txt','part05.txt','part06.txt','part07.txt','part08.txt']

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

subprocess.run([sys.executable, 'build_site.py'], cwd=WORK, check=True)
shutil.copytree(WORK / 'site', OUTPUT)
shutil.rmtree(WORK)
print(f'SepticScope build complete: {OUTPUT}')
