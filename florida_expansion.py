# SepticScope Florida expansion wrapper.
# Preserve the original verified Florida batch, then apply the current additional batch.
exec((ROOT / 'florida_expansion_base.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'florida_second_expansion.py').read_text(encoding='utf-8'), globals())

# Run the latest supplemental county batches before the nationwide fallback layer so
# verified local pages survive the final national county-directory generation.
exec((ROOT / 'texas_fourth_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'texas_fifth_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'north_carolina_sixth_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'north_carolina_seventh_expansion.py').read_text(encoding='utf-8'), globals())
