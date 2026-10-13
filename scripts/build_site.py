"""Build site/index.html from site/template.html + validated data/*.csv. Prints the headline numbers it computes."""
import json, statistics as st, pandas as pd
REF = dict(cs2023_intro=1, cs2023_bok=3, csta2026=4, astrachan1997=5, slashdot2000=6, slashdot2008=7, edsurge2016=8,
           apcentral_csa=9, wiki_apcs=10, eurydice2022=11, eurydice2026=12, govuk_computing=13, car2025=14,
           wirth1971=15, stroustrup=16, java1995=17, pythondocs=18)
ev = pd.read_csv('data/cs_curriculum_events.csv')
EV = json.loads(ev.where(ev.notna(), None).to_json(orient='records'))
lag = pd.read_csv('data/cs_curriculum_lags.csv')
lag = lag[lag['case'] != 'CSTA 2026 standards']          # development time, not decision-to-classroom
LAG = json.loads(lag.where(lag.notna(), None).to_json(orient='records'))
def gaps(years, labels, c, open_end=None):
    g = [dict(v=round(b - a, 1), t=f'{la} {a} → {lb} {b}: {round(b - a, 1)} yrs') for a, b, la, lb in zip(years, years[1:], labels, labels[1:])]
    if open_end: g.append(dict(v=round(open_end[0] - years[-1], 1), t=open_end[1], open=True))
    return g
GAPS = [
  dict(name='University CS (ACM/IEEE)', c='var(--us)', gaps=gaps([1968, 1979, 1991, 2001, 2008, 2013, 2023], ["C'68", "C'78", 'CC1991', 'CC2001', 'CS2008', 'CS2013', 'CS2023'], 'us')),
  dict(name='US K-12 standards (ACM/CSTA)', c='var(--us)', gaps=gaps([2003, 2006, 2011, 2017, 2026], ['ACM model', 'ACM rev.', 'CSTA', 'CSTA', 'CSTA'], 'us')),
  dict(name='AP CS exam language', c='var(--us)', gaps=gaps([1984, 1999, 2004], ['Pascal', 'C++', 'Java'], 'us', open_end=(2026, 'Java since the 2004 exam: 22 years and counting'))),
  dict(name='England national curriculum', c='var(--eu)', gaps=gaps([2014, 2028], ['Computing', 'new curriculum (planned)'], 'eu')),
]
std = pd.read_csv('data/us_states_cs_standards.csv')
STD = [dict(year=int(r.year), n=None if pd.isna(r.states_with_k12_cs_standards) else int(r.states_with_k12_cs_standards), src=r.source) for r in std.itertuples()]
hist = pd.read_csv('data/history_series.csv')
CS = [[int(y), float(x)] for y, x in hist[hist.series == 'US high schools offering foundational CS'][['year', 'value']].values]
ka = pd.read_csv('data/cs2023_core_hours.csv')
KA = [dict(name=r.knowledge_area, a=int(r.cs2013_tier1 + r.cs2013_tier2), b=None if pd.isna(r.cs2023_cs_core) else int(r.cs2023_cs_core)) for r in ka.itertuples()]
nces = pd.read_csv('data/nces_spp_ai_dec2024.csv')
seg = nces[(nces['var'] == 'AI5_y') & (nces.category == 'Yes')][['subgroup', 'pct', 'se']]
SEG = [dict(g=g, pct=float(p), se=float(s)) for g, p, s in seg.itertuples(index=False)]
subj = pd.read_csv('data/subject_revisions.csv')
SUBJ = json.loads(subj[['level', 'subject', 'year', 'document']].to_json(orient='records'))
# Europe: year each country's new computing curriculum reached all classes (end of implementation window, or edition year)
EUPTS = [('EN', 'England (UK)', 2014, 'Computing replaces ICT, taught from 2014/15'), ('FR', 'France', 2019, 'Lycée reform: informatics subjects from 2019'),
         ('IE', 'Ireland', 2021, 'Junior-cycle coding course fully phased in by 2021'), ('BG', 'Bulgaria', 2021, 'New subject from 2021/22'),
         ('LU', 'Luxembourg', 2022, 'Digital sciences national from 2022/23'), ('CY', 'Cyprus', 2022, 'Python replaces Pascal, 2022/23'),
         ('MT', 'Malta', 2023, 'ICT C3 reaches final grade 2022/23'), ('LV', 'Latvia', 2023, 'New computing syllabus complete 2022/23'),
         ('LT', 'Lithuania', 2023, 'New informatics curriculum mandatory 2023'), ('CZ', 'Czechia', 2024, 'New informatics in all lower-secondary 2024'),
         ('ES', 'Spain', 2024, 'LOMLOE curriculum fully in place 2023/24'), ('SK', 'Slovakia', 2027, 'Planned: full roll-out 2026/27 (includes AI)')]
EU = [dict(c=c, n=n, y=y, t=f'{n}, {y}: {t}', planned=y > 2026) for c, n, y, t in EUPTS]
eut = pd.read_csv('data/europe_tiers.csv')
cur = eut.ai_curriculum.str.startswith('AI related competences are included')
EUAI = dict(total=len(eut), yes=int(cur.sum()), pipeline=int((~cur & eut.curriculum_in_pipeline).sum()))
EUAI['none'] = EUAI['total'] - EUAI['yes'] - EUAI['pipeline']
# Eurydice (2022) Informatics education at school in Europe, Main findings p.9-10 and s.1.5 (reference year 2020/21, 39 systems)
EUINF = dict(total=39, primary=23, lower_secondary=35, reform_implementing=17, reform_developing=11)
# Evidence register: the source's own words for every number on the page (data/evidence.csv, checked by scripts/check_quotes.py)
evd = pd.read_csv('data/evidence.csv').fillna('')
EVID = evd.to_dict(orient='records')
val = dict(zip(evd.id, evd.value))
for p in STD:   # chart values must match the register
    if p['n'] is not None: assert val[f"std_{p['year']}"] == str(p['n']), p
assert val['eu_impl'] == f"{EUINF['reform_implementing']} of {EUINF['total']}" and val['eu_dev'] == f"{EUINF['reform_developing']} of {EUINF['total']}"
assert val['eu_lower'] == f"{EUINF['lower_secondary']} of {EUINF['total']}" and val['eu_primary'] == f"{EUINF['primary']} of {EUINF['total']}"
assert val['eu_ai'] == f"{EUAI['yes']} of {EUAI['total']}", (val['eu_ai'], EUAI)
hs = nces[(nces.subgroup == 'High/Secondary')].set_index(['var', 'category']).pct
assert val['us_any'] == f"{hs[('AI5_y', 'Yes')]}%" and val['us_all'] == f"{hs[('AI5_1', 'All students')]}–{hs[('AI5_2', 'All students')]}%"
data = dict(REF=REF, LAG=LAG, STD=STD, SUBJ=SUBJ, EU=EU, EUAI=EUAI, EUINF=EUINF, EVID=EVID)
print('EUAI', EUAI, 'EUINF', EUINF)
tpl = open('site/template.html').read()
html = tpl.replace('/*__DATA__*/', 'const DATA = ' + json.dumps(data, ensure_ascii=False) + ';')
open('site/index.html', 'w').write(html)
import os; os.makedirs('docs', exist_ok=True); open('docs/index.html', 'w').write(html)   # GitHub Pages serves /docs
# headline checks
for g in GAPS: print(f"{g['name']}: gaps {[x['v'] for x in g['gaps']]} median(closed) {st.median([x['v'] for x in g['gaps'] if not x.get('open')])}")
d2c = lag[lag.kind == 'decision_to_classroom'].lag_years
print('decision->classroom: n', len(d2c), 'median', d2c.median(), 'range', d2c.min(), d2c.max())
print('AP language lags:', lag[lag['case'].str.contains('AP CS') & (lag.kind == 'tech_to_curriculum')][['case', 'lag_years']].values.tolist())
print('missing refs:', sorted({k for s in ev.source_key.tolist() + lag.source_keys.tolist() for k in s.split(';')} - set(REF)))
