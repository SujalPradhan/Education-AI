"""Read CodeAI 2025 'Introducing Policies to Make AI Foundational' toggle colors from each state page.
Knob colour: green = policy met, red = not met, other (yellow/orange) = partial/in progress."""
import re, sys, numpy as np, pandas as pd, pypdfium2 as pdfium
pdf, txtf, out = sys.argv[1:4]
pages = re.split(r'<<PAGE (\d+)>>', open(txtf).read())
STATES = ["ALABAMA","ALASKA","ARIZONA","ARKANSAS","CALIFORNIA","COLORADO","CONNECTICUT","DELAWARE","FLORIDA","GEORGIA","HAWAI","IDAHO","ILLINOIS","INDIANA","IOWA","KANSAS","KENTUCKY","LOUISIANA","MAINE","MARYLAND","MASSACHUSETTS","MICHIGAN","MINNESOTA","MISSISSIPPI","MISSOURI","MONTANA","NEBRASKA","NEVADA","NEW HAMPSHIRE","NEW JERSEY","NEW MEXICO","NEW YORK","NORTH CAROLINA","NORTH DAKOTA","OHIO","OKLAHOMA","OREGON","PENNSYLVANIA","RHODE ISLAND","SOUTH CAROLINA","SOUTH DAKOTA","TENNESSEE","TEXAS","UTAH","VERMONT","VIRGINIA","WASHINGTON","WEST VIRGINIA","WISCONSIN","WYOMING"]
pagestate = {}
for k in range(1, len(pages), 2):
    num, body = int(pages[k]), pages[k+1]
    hits = [s for s in STATES if re.search(r'(?m)^\s*' + s + r'\S*\s*$', body)]
    if hits: pagestate[num] = max(hits, key=len)
doc = pdfium.PdfDocument(pdf)
def classify(px):
    r, g, b = px[..., 0].astype(int), px[..., 1].astype(int), px[..., 2].astype(int)
    green = ((g > 150) & (r < 110) & (b < 110)).sum()
    red = ((r > 180) & (g < 70) & (b < 70)).sum()
    yellow = ((r > 200) & (g > 140) & (b < 80)).sum()
    c = {'met': green, 'not_met': red, 'partial': yellow}
    return max(c, key=c.get) if max(c.values()) > 30 else None
rows = []
for num, st in sorted(pagestate.items()):
    img = np.array(doc[num-1].render(scale=1.3).to_pil().convert('RGB'))
    H, W, _ = img.shape
    band = img[int(H*0.13):int(H*0.21)]           # AI toggle row (~y=180/1030)
    xs = [(65, 215), (237, 387), (409, 559), (581, 731)]
    sc = W / 796
    vals = [classify(band[:, int(a*sc):int(b*sc)]) for a, b in xs]
    # CS graduation requirement toggle (bottom-right of 'Ten Policies' panel)
    gband = img[int(H*0.73):int(H*0.77), int(581*sc):int(731*sc)]
    rows.append(dict(page=num, state=st.title().replace('Hawai', 'Hawaii'), ai_cs_standards=vals[0], ai_cs_grad_req=vals[1],
                     ai_cs_pd_funding=vals[2], ai_cs_guidance=vals[3], cs_grad_req=classify(gband)))
df = pd.DataFrame(rows)
df.to_csv(out, index=False)
print(len(df), 'states')
for c in df.columns[2:]: print(c, df[c].value_counts(dropna=False).to_dict())
