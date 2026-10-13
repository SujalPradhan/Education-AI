"""Europe: tier classification of 38 Eurydice systems + test of the 'Western & Southern' pattern and correlates.
Inputs: data/eurydice_ai.csv, Eurostat JSONs. Output: data/europe_tiers.csv + printed stats."""
import json, sys, pandas as pd, numpy as np
from scipy import stats
E = 'sources/eurostat/'
def es(f, filt=None):
    d = json.load(open(E + f)); dims = d['id']; sizes = d['size']
    labels = {k: d['dimension'][k]['category'] for k in dims}
    out = {}
    for flat, v in d['value'].items():
        i, idx = int(flat), {}
        for k, s in zip(reversed(dims), reversed(sizes)):
            idx[k] = i % s; i //= s
        keys = {k: list(labels[k]['index'].keys())[list(labels[k]['index'].values()).index(idx[k])] for k in dims}
        if filt and any(keys[a] != b for a, b in filt.items()): continue
        out[labels['geo']['label'][keys['geo']]] = v
    return pd.Series(out)
dig = es('digital_skills_2023.json'); pisa = es('pisa_low_2022.json', {'field': 'EF461'}); gdp = es('gdp_pps_2024.json')
df = pd.read_csv('data/eurydice_ai.csv', index_col=0)
geo = {s: ('Belgium' if s.startswith('Belgium') else s) for s in df.index}
geo.update({'Türkiye': 'Türkiye', 'Bosnia and Herzegovina': 'Bosnia and Herzegovina', 'North Macedonia': 'North Macedonia'})
for name, ser in [('basic_digital_skills_2023', dig), ('pisa_math_low_achievers_2022', pisa), ('gdp_pps_2024', gdp)]:
    df[name] = [ser.get(geo[s], np.nan) for s in df.index]
# UN M49 sub-regions (Türkiye is Western Asia in M49 -> kept separate)
M49 = {'Western': ['Belgium', 'Germany', 'France', 'Luxembourg', 'Netherlands', 'Austria', 'Switzerland', 'Liechtenstein'],
       'Southern': ['Greece', 'Spain', 'Croatia', 'Italy', 'Malta', 'Portugal', 'Slovenia', 'Bosnia and Herzegovina', 'Montenegro', 'North Macedonia', 'Serbia'],
       'Northern': ['Denmark', 'Estonia', 'Ireland', 'Latvia', 'Lithuania', 'Finland', 'Sweden', 'Iceland', 'Norway'],
       'Eastern': ['Bulgaria', 'Czechia', 'Hungary', 'Poland', 'Romania', 'Slovakia'],
       'Western Asia (M49)': ['Cyprus', 'Türkiye']}
reg = {c: r for r, cs in M49.items() for c in cs}
df['m49_region'] = [reg[geo[s]] for s in df.index]
cur = df.ai_curriculum.str.startswith('AI related competences are included')
fw = df.ai_framework != 'No top-level framework reported'
# Curriculum reform adopted but not yet in force in 2024/25 (report text pp.127): CZ (2028-32), SK (full by 2026/27), IE (Sept 2026), HR (pilot elective 2025/26)
pipeline = df.index.isin(['Czechia', 'Slovakia', 'Ireland', 'Croatia'])
df['tier'] = np.select([cur, fw | pipeline], ['1 AI in national curriculum', '2 Framework/guidance or curriculum in pipeline'], '3 No top-level AI framework or curriculum')
df['curriculum_in_pipeline'] = pipeline
df.to_csv('data/europe_tiers.csv')
print(df.tier.value_counts().sort_index().to_string(), '\n')
for t, g in df.groupby('tier'): print(t, ':', ', '.join(g.index))
print('\nAI curriculum share by M49 region:')
print(df.groupby('m49_region').apply(lambda g: f"{(g.ai_curriculum.str.startswith('AI related competences are included')).sum()}/{len(g)}").to_string())
ws = df.m49_region.isin(['Western', 'Southern'])
tab = pd.crosstab(ws, cur); print('\nW+S vs rest crosstab (rows: W+S; cols: AI curriculum)\n', tab)
print('Fisher exact p =', round(stats.fisher_exact(tab.values)[1], 3))
print('\nCorrelates (AI curriculum yes vs no): medians, Mann-Whitney p, n')
for v in ['basic_digital_skills_2023', 'pisa_math_low_achievers_2022', 'gdp_pps_2024']:
    a, b = df.loc[cur, v].dropna(), df.loc[~cur, v].dropna()
    print(f'{v}: yes {a.median():.1f} (n={len(a)}) vs no {b.median():.1f} (n={len(b)}); p={stats.mannwhitneyu(a, b).pvalue:.2f}')
print('\nFramework yes vs no:')
for v in ['basic_digital_skills_2023', 'pisa_math_low_achievers_2022', 'gdp_pps_2024']:
    a, b = df.loc[fw, v].dropna(), df.loc[~fw, v].dropna()
    print(f'{v}: yes {a.median():.1f} (n={len(a)}) vs no {b.median():.1f} (n={len(b)}); p={stats.mannwhitneyu(a, b).pvalue:.2f}')
print('\nDedicated digital subject (compulsory) vs AI curriculum:')
ded = df.digital_competence_approach.fillna('').str.contains('compulsory')
print(pd.crosstab(ded, cur), 'Fisher p=', round(stats.fisher_exact(pd.crosstab(ded, cur).values)[1], 3))
print('\nmissing correlates:', df[df[['basic_digital_skills_2023','pisa_math_low_achievers_2022','gdp_pps_2024']].isna().any(axis=1)].index.tolist())
