# SepticScope Florida expansion wrapper.
# Preserve the original verified Florida batch, then apply the current additional batch.
exec((ROOT / 'florida_expansion_base.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'florida_second_expansion.py').read_text(encoding='utf-8'), globals())

# Run the latest North Carolina supplemental county after the accumulated NC batches
# and before the nationwide fallback layer so the verified page and state hub persist.
exec((ROOT / 'north_carolina_sixth_expansion.py').read_text(encoding='utf-8'), globals())
