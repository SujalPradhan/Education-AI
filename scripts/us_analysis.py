"""US state tiers for AI-in-school policy (as of Oct 2026) and tests vs politics, size, spending.
Tier 1 'Instruction required/standardised': AI emphasised in state CS standards (CodeAI 2025) OR enacted law putting AI literacy into
        standards / required coursework (verified: AL HB329 2026, MD SB720 2026, ID SB1227 2026, UT HB218 2026 [optional course standards], CA AB2876 2024 ['consider']).
Tier 2 'Guidance only': official SEA K-12 AI guidance (AI for Education tracker, updated 2026-08-21) but no Tier-1 measure.
Tier 3 'Neither'."""
import re, pandas as pd, numpy as np, openpyxl
from scipy import stats
cs = pd.read_csv('data/codeorg_ai_policy_2025.csv').set_index('state')
GUIDANCE = ['Alabama','Alaska','Arizona','California','Colorado','Connecticut','Delaware','Georgia','Hawaii','Indiana','Illinois','Kentucky','Louisiana',
            'Maine','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nevada','New Mexico','North Carolina','North Dakota','Ohio',
            'Oklahoma','Oregon','Rhode Island','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
assert len(GUIDANCE) == 35
LAWS = {'Alabama': 'HB329 (2026): CS course incl. AI required for graduation, class of 2032 [FutureEd; single-source]',
        'Maryland': 'SB720 (2026): AI literacy into state standards by Jun 2027; PD [FutureEd + ExcelinEd]',
        'Idaho': 'SB1227 (2026): state GenAI framework incl. AI literacy standards [FutureEd + MultiState]',
        'Utah': 'HB218 (2026): standards for an LEA-optional gr7/8 digital skills course incl. AI literacy [enrolled-text summaries]',
        'California': 'AB2876 (2024): IQC must *consider* AI literacy in math/science/HSS frameworks [chaptered]'}
df = cs[['ai_cs_standards', 'ai_cs_pd_funding', 'ai_cs_guidance', 'cs_grad_req']].copy()
df['sea_ai_guidance'] = df.index.isin(GUIDANCE)
df['ai_law'] = [LAWS.get(s, '') for s in df.index]
t1 = (df.ai_cs_standards == 'met') | (df.ai_law != '')
df['tier'] = np.select([t1, df.sea_ai_guidance], ['1 AI in standards or law', '2 Guidance only'], '3 Neither')
# covariates
mit = pd.read_csv('sources/us_covariates/mit_president_1976_2024.csv')
m = mit[mit.year == 2024]
tot = m.groupby('state').totalvotes.first()
rep = m[m.party_simplified == 'REPUBLICAN'].groupby('state').candidatevotes.sum()
dem = m[m.party_simplified == 'DEMOCRAT'].groupby('state').candidatevotes.sum()
margin = ((rep - dem) / tot * 100).rename(lambda s: s.title())
df['gop_margin_2024'] = margin.reindex(df.index).values
wb = openpyxl.load_workbook('sources/us_covariates/census_elsec23.xlsx', read_only=True)
def census(sheet, col):
    out = {}
    for r in wb[sheet].iter_rows(values_only=True):
        if r[0] and isinstance(r[col], (int, float)): out[re.sub(r'\.+$', '', str(r[0]).strip())] = r[col]
    return pd.Series(out)
df['enrollment_2023'] = census('19', 4).reindex(df.index).values
df['per_pupil_spend_fy23'] = census('8', 2).reindex(df.index).values
assert df[['gop_margin_2024', 'enrollment_2023', 'per_pupil_spend_fy23']].notna().all().all(), df[df.isna().any(axis=1)]
df.to_csv('data/us_state_tiers.csv')
print(df.tier.value_counts().sort_index().to_string())
for t, g in df.groupby('tier'): print(f'\n{t} ({len(g)}):', ', '.join(g.index))
print('\nMedians by tier:'); print(df.groupby('tier')[['gop_margin_2024', 'enrollment_2023', 'per_pupil_spend_fy23']].median().round(1).to_string())
print('\nTrump-won states by tier:', df.assign(red=df.gop_margin_2024 > 0).groupby('tier').red.agg(['sum', 'count']).to_string())
print('\nKruskal-Wallis across 3 tiers:')
for v in ['gop_margin_2024', 'enrollment_2023', 'per_pupil_spend_fy23']:
    print(v, 'p=%.2f' % stats.kruskal(*[g[v] for _, g in df.groupby('tier')]).pvalue)
any_policy = df.tier != '3 Neither'
print('\nAny policy vs none: Trump states', pd.crosstab(df.gop_margin_2024 > 0, any_policy).to_string(), 'Fisher p=%.2f' % stats.fisher_exact(pd.crosstab(df.gop_margin_2024 > 0, any_policy).values)[1])
print('CS grad requirement vs tier1:', pd.crosstab(df.cs_grad_req, t1).to_string())
print('Enrollment share covered by tier1: %.0f%%; tier1+2: %.0f%%' % (df.loc[t1, 'enrollment_2023'].sum() / df.enrollment_2023.sum() * 100, df.loc[df.tier != '3 Neither', 'enrollment_2023'].sum() / df.enrollment_2023.sum() * 100))
