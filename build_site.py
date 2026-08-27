from pathlib import Path
import shutil, subprocess, sys, zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / 'septicscope-source.zip'
WORK = ROOT / '.septicscope-build'
OUTPUT = ROOT / 'site'

if WORK.exists():
    shutil.rmtree(WORK)
if OUTPUT.exists():
    shutil.rmtree(OUTPUT)
WORK.mkdir()

with zipfile.ZipFile(ARCHIVE) as z:
    z.extractall(WORK)

subprocess.run([sys.executable, 'build_site.py'], cwd=WORK, check=True)
shutil.copytree(WORK / 'site', OUTPUT)
shutil.rmtree(WORK)
print(f'SepticScope build complete: {OUTPUT}')
