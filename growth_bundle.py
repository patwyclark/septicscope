"""Materialize SepticScope growth sources from deterministic compressed parts."""
from __future__ import annotations
import base64, hashlib, io, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "growth_bundle_parts"
EXPECTED = {
    "growth_layer.py",
    "data/providers.json",
    "functions/api/location.js",
    "growth_audit.py",
    "search_console_prioritizer.py",
    "SEARCH_CONSOLE.md",
}
PART_COUNT = 17
PAYLOAD_SHA256 = 'd7f19709d14af447f8f9dedc971452d760278f9ad550da06ac95bc56efd0e692'

def materialize() -> None:
    encoded = "".join((PARTS / f"part{i:02d}.txt").read_text(encoding="utf-8").strip() for i in range(PART_COUNT))
    archive = base64.b64decode(encoded, validate=True)
    actual = hashlib.sha256(archive).hexdigest()
    if actual != PAYLOAD_SHA256:
        raise RuntimeError(f"Growth bundle checksum mismatch: {actual}")
    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        names = set(bundle.namelist())
        if names != EXPECTED:
            raise RuntimeError(f"Growth bundle file manifest mismatch: {sorted(names)}")
        bad = bundle.testzip()
        if bad:
            raise RuntimeError(f"Growth bundle failed ZIP integrity check at {bad}")
        for name in sorted(EXPECTED):
            target = ROOT / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(bundle.read(name))
    print("SepticScope growth source bundle materialized and verified")

if __name__ == "__main__":
    materialize()
