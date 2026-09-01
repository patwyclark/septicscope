#!/usr/bin/env python3
"""Load the checksum-verified hourly provider discovery implementation."""
from __future__ import annotations

import base64
import gzip
import hashlib
from pathlib import Path

PARTS = Path(__file__).with_name("provider_discovery_parts")
PART_COUNT = 4
SOURCE_SHA256 = "24ec64a4855709036d1f78cf8ac4a0e46f46697595c48ad1ee0e4fb74f89e098"

encoded = "".join(
    (PARTS / f"part{index:02d}.txt").read_text(encoding="utf-8").strip()
    for index in range(PART_COUNT)
)
source_bytes = gzip.decompress(base64.b64decode(encoded, validate=True))
actual = hashlib.sha256(source_bytes).hexdigest()
if actual != SOURCE_SHA256:
    raise RuntimeError(f"Provider discovery source checksum mismatch: {actual}")

exec(compile(source_bytes, str(Path(__file__).with_name("provider_discovery_impl.py")), "exec"), globals())
