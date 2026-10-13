"""Extract NCES School Pulse Panel AI items (AI5 taught-to-students, AI4a policy, AI1a training) by school level."""
import sys, openpyxl, pandas as pd
wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
keep = ('AI5_1', 'AI5_2', 'AI5_3', 'AI5_4', 'AI5_y', 'AI4a', 'AI1a_1', 'AI3', 'DL1')
recs = []
for sheet in ['All Schools', 'School Level', 'Poverty', 'Locale']:
    rows = list(wb[sheet].iter_rows(values_only=True))
    hdr = rows[0]
    for r in rows[1:]:
        if r[2] in keep:
            recs.append(dict(sheet=sheet, month=str(r[0])[:7], subgroup=r[1], var=r[2], desc=r[5], category=r[6], pct=r[7], se=r[8]))
df = pd.DataFrame(recs); df.to_csv(sys.argv[2], index=False)
pd.set_option('display.width', 200)
print(df[df['var'].str.startswith('AI5')].pivot_table(index=['var', 'category'], columns='subgroup', values='pct', aggfunc='first').to_string())
print(df[df['var'].isin(['AI4a','AI1a_1','AI3'])].pivot_table(index=['var','category'], columns='subgroup', values='pct', aggfunc='first').to_string())
print(df.month.unique())
