# Education-AI

Computer science and AI in schools: US vs Europe. A single-page answer to four questions — how often the CS curriculum changes, whether schools must teach CS, whether AI is being taught, and whether teaching AI works.

- **Live page:** https://sujalpradhan.github.io/Education-AI/
- `site/template.html` — page source; `scripts/build_site.py` injects the data and writes `site/index.html` and `docs/index.html`
- `data/evidence.csv`: one row per number on the page, with the source quote, page and check type; `scripts/check_quotes.py` confirms each quote word-for-word against the saved source.
- `data/` — validated, source-annotated CSVs behind every number
- `scripts/` — extraction and analysis code
- `validation/` — independent re-derivation of headline figures

Raw source documents are not redistributed; every figure links to its original in the page's Sources list.
