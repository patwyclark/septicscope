# Collision-safe wrapper around the established nationwide county lookup generator.
# Several Census county-equivalents share a base name with a county in the same state.
# The preserved core generator is patched at runtime so every FIPS entity receives a
# unique route while the long-standing county URL remains unchanged.
from pathlib import Path

_core = Path(__file__).with_name("nationwide_county_lookup_core.py")
_source = _core.read_text(encoding="utf-8")
_needle = """if len(rows) != 3144 or len({r[3] for r in rows}) != 3144:
    raise RuntimeError(f'Nationwide county dataset integrity failure: {len(rows)} rows')
"""
_injection = _needle + """
# Give same-name county-equivalents distinct source names before slug generation.
# Example: Fairfax County keeps /fairfax/ while Fairfax City uses /fairfax-city/.
_collision_counts = {}
for _abbr, _name, _lsad, _fips in rows:
    _key = (_abbr, slugify(_name))
    _collision_counts[_key] = _collision_counts.get(_key, 0) + 1
_collision_safe_rows = []
for _abbr, _name, _lsad, _fips in rows:
    _key = (_abbr, slugify(_name))
    if _collision_counts[_key] > 1 and str(_lsad).lower() != 'county':
        _label = 'Census Area' if _lsad == 'CA' else _lsad
        if str(_label).lower() not in _name.lower():
            _name = f'{_name} {_label}'
    _collision_safe_rows.append([_abbr, _name, _lsad, _fips])
rows = _collision_safe_rows
"""
if _source.count(_needle) != 1:
    raise RuntimeError("Nationwide lookup compatibility patch no longer matches the preserved core generator")
_source = _source.replace(_needle, _injection, 1)
exec(compile(_source, str(_core), "exec"), globals())
