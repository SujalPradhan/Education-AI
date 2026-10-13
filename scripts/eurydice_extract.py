"""Extract Eurydice 2026 open-data AI tables to a tidy CSV (one row per education system)."""
import sys, openpyxl, pandas as pd
src, out = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(src, read_only=True)
def table(name):
    rows = list(wb[name].iter_rows(values_only=True))
    hdr_i = next(i for i, r in enumerate(rows) if r[0] is None and r[1])
    hdr = [h for h in rows[hdr_i][1:] if h]
    recs = {}
    for r in rows[hdr_i+1:]:
        if not r[0] or str(r[0]).startswith(('Explanatory', 'Country', '=')) or r[0] is None: break
        recs[r[0].strip()] = next((hdr[j] for j, v in enumerate(r[1:len(hdr)+1]) if v == 1), None)
    return pd.Series(recs, name=name)
df = pd.concat([table('Table 4.3'), table('Table 1.7'), table('Table 1.8'), table('Table 5.7')], axis=1)
df.columns = ['ai_curriculum', 'ai_framework', 'ai_largescale_initiative', 'leader_cpd_guidance']
dig = {}
rows = list(wb['Table 4.1'].iter_rows(values_only=True))
hi = next(i for i, r in enumerate(rows) if r[0] is None and r[1])
hdr = [h.strip() for h in rows[hi][1:5]]
for r in rows[hi+1:]:
    if not r[0] or str(r[0]).startswith('Explanatory'): break
    dig[r[0].strip()] = '; '.join(hdr[j] for j, v in enumerate(r[1:5]) if v == 1)
df['digital_competence_approach'] = pd.Series(dig)
df.index.name = 'system'
df.to_csv(out)
print(df.shape); print(df.apply(lambda c: c.value_counts()).to_string() if False else '')
for c in df.columns[:4]: print(df[c].value_counts(dropna=False).to_string(), '\n')
