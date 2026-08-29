# Oregon expansion wrapper. Preserve the validated Oregon batch, then run North Carolina and the additional Alabama batch.
exec((ROOT / 'oregon_expansion_base.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'north_carolina_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'alabama_additional_expansion.py').read_text(encoding='utf-8'), globals())
