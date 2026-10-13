"""Confirm every quoted fragment in data/evidence.csv appears in the saved source text (whitespace-insensitive)."""
import csv, re, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
TXT = {'CSTA': 'curricula/csta_2026_standards.txt', 'Eurydice (2022)': 'curricula/eurydice_informatics_2022.txt',
       'Eurydice (2026)': 'eurydice/report.txt', 'RAND': 'surveys/rand_RRA4180-1.txt', 'Stanford': 'evidence/stanford_scale_2026.txt',
       'AI Leap': 'estonia/ai_leap.txt', 'State of Computer Science 2018': 'codeorg/stateofcs2018.txt',
       'State of Computer Science 2019': 'codeorg/stateofcs2019.txt', 'State of Computer Science 2024': 'codeorg/stateofcs2024.txt'}
norm = lambda s: re.sub(r'[\s\-–]+', '', s).lower()
bad = 0
for r in csv.DictReader(open(ROOT / 'data/evidence.csv')):
    if r['check'] != 'quote': continue
    path = next((v for k, v in TXT.items() if k in r['source']), None)
    text = norm((ROOT / 'sources' / path).read_text(errors='ignore'))
    for q in re.findall(r'"([^"]+)"', r['quote']):
        for frag in q.split('…'):
            ok = norm(frag) in text
            bad += not ok
            print('OK ' if ok else 'MISSING', r['id'], '|', frag.strip()[:70])
sys.exit(bad)
