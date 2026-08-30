# SepticScope Nevada expansion chain wrapper.
# Keep Nevada implementation isolated so verified state batches can be chained without rewriting it.
exec((ROOT / 'nevada_expansion_impl.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'kansas_expansion.py').read_text(encoding='utf-8'), globals())
