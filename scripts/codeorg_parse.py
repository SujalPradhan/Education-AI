"""Infer each state's AI+CS policy status from CodeAI 2025 state pages.
A policy counts as MET when it is absent from the state's 'can expand its commitment ... by' sentence.
Validated against report totals: standards 4, guidance 17, PD funding 5, grad req 0."""
import re, sys, pandas as pd
txt = open(sys.argv[1]).read()
pages = re.split(r'<<PAGE \d+>>', txt)
STATES = ["ALABAMA","ALASKA","ARIZONA","ARKANSAS","CALIFORNIA","COLORADO","CONNECTICUT","DELAWARE","FLORIDA","GEORGIA","HAWAI","IDAHO","ILLINOIS","INDIANA","IOWA","KANSAS","KENTUCKY","LOUISIANA","MAINE","MARYLAND","MASSACHUSETTS","MICHIGAN","MINNESOTA","MISSISSIPPI","MISSOURI","MONTANA","NEBRASKA","NEVADA","NEW HAMPSHIRE","NEW JERSEY","NEW MEXICO","NEW YORK","NORTH CAROLINA","NORTH DAKOTA","OHIO","OKLAHOMA","OREGON","PENNSYLVANIA","RHODE ISLAND","SOUTH CAROLINA","SOUTH DAKOTA","TENNESSEE","TEXAS","UTAH","VERMONT","VIRGINIA","WASHINGTON","WEST VIRGINIA","WISCONSIN","WYOMING"]
rows = []
for p in pages:
    m = re.search(r'can (?:further )?expand its commitment to AI \+ CS education by(.*?)\.\s*\n?(?:[A-Z]|$)', p.replace('\n', ' '), re.S)
    st = [s for s in STATES if re.search(r'\b' + s + r'(?:’I|\'I|I)?\b', p) and re.search(r'(?m)^' + s, p)]
    if not st: continue
    flat = p.replace('\n', ' ')
    m = re.search(r'expand its commitment to AI \+ CS education by (.*?)\.(?: |$)', flat)
    gap = m.group(1).lower() if m else ''
    rows.append(dict(state=st[0].title(), gap_sentence=gap,
        ai_standards=('standards' not in gap) if m else None,
        ai_grad_req=('graduation' not in gap) if m else None,
        ai_pd_funding=('professional development' not in gap) if m else None,
        ai_cs_guidance=not any(k in gap for k in ['guidance', 'fundamental role', 'clarif']) if m else None))
df = pd.DataFrame(rows).drop_duplicates('state')
print(len(df), 'states parsed;', df.gap_sentence.eq('').sum(), 'without gap sentence')
print(df[['ai_standards','ai_grad_req','ai_pd_funding','ai_cs_guidance']].sum())
df.to_csv(sys.argv[2], index=False)
