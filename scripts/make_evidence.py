"""Write data/evidence.csv: one row per number on the page, with the source's own words.

check: quote = figure appears verbatim in the source; count = we counted it from the source's table/data;
       chart = read off a published chart; date = publication year confirmed from the source; calc = our arithmetic.
Quotes were matched against the saved copies in sources/ (page = PDF page).
"""
import csv, pathlib
CSTA = ('CSTA (2026), PK–12 CS Standards', 'https://csteachers.org/wp-content/uploads/2026/07/2026-CSTA-PK%E2%80%9312-Computer-Science-Standards.pdf')
EU22 = ('Eurydice (2022), Informatics education at school in Europe', 'https://eurydice.indire.it/wp-content/uploads/2022/09/Informatics-education_Report.pdf')
EU26 = ('Eurydice (2026), Digital education at school in Europe', 'https://eurydice.eacea.ec.europa.eu/sites/default/files/2026-09/z_Digital_ed_OpenData_2026_without_links.xlsx')
NCES = ('NCES School Pulse Panel, Dec 2024', 'https://nces.ed.gov/surveys/spp/docs/release/Technology.xlsx')
RAND = ('RAND (2025), RR-A4180-1', 'https://www.rand.org/pubs/research_reports/RRA4180-1.html')
SCALE = ('Stanford SCALE (2026), The Evidence Base on AI in K-12', 'https://scale.stanford.edu/sites/default/files/The%20Evidence%20Base%20on%20AI%20in%20K-12%20Report.pdf')
LEAP = ('AI Leap Foundation (2026), First Annual Review 2025/26', 'https://tihupe.ee/wp-content/uploads/2026/08/AI-Leap-First-Annual-Review-202526.pdf')
CODE = lambda y: (f'Code.org, State of Computer Science {y}', 'https://advocacy.code.org/stateofcs/')
rows = [
 # card 1
 ('cs_versions', 1, 'US school CS standards: 5 versions since 2003', '2003 · 2006 · 2011 · 2017 · 2026', 'quote',
  '"in 2003 (Tucker, 2003) and revised in 2006 (Tucker et al., 2006), laying the groundwork for the first comprehensive CSTA K–12 Computer Science Standards released in 2011 … A revised set of Standards was published in 2017"', *CSTA, 'p.10'),
 ('maths_versions', 1, 'US school maths standards: 3 versions', '1989 · 2000 · 2010', 'date',
  'NCTM Curriculum and Evaluation Standards (1989); Principles and Standards for School Mathematics (2000); Common Core (2010).', 'NCTM; AMS Notices (2000); Education Week (2010)', 'https://www.ams.org/journals/notices/200008/comm-ferrini.pdf', ''),
 ('science_versions', 1, 'US school science standards: 2 versions', '1996 · 2013', 'date',
  'National Science Education Standards (NRC, 1996); Next Generation Science Standards (2013).', 'National Research Council; NGSS', 'https://doi.org/10.17226/4962', ''),
 ('english_versions', 1, 'US school English standards: 2 versions', '1996 · 2010', 'date',
  'NCTE/IRA Standards for the English Language Arts (1996); Common Core ELA (2010).', 'Education Week (1996, 2010)', 'https://www.edweek.org/teaching-learning/standards-for-language-arts-are-unveiled/1996/03', ''),
 ('social_versions', 1, 'US school social studies standards: 2 versions', '1994 · 2010', 'date',
  'NCSS Expectations of Excellence (1994); National Curriculum Standards for Social Studies (2010).', 'Education Week (1994); NCSS library record (2010)', 'https://www.edweek.org/education/social-studies-council-issues-standards-for-k-12-curriculum/1994/09', ''),
 ('rate', 1, 'US: CS standards rewritten 3–5× as often', '1.7 vs 0.3–0.5 per decade', 'calc',
  'Rewrites per decade = (versions − 1) ÷ (2026 − first year) × 10. CS: 4 ÷ 23 × 10 = 1.7. Maths 0.5, science 0.3, English 0.3, social studies 0.3.', 'Standards dates: see table below', '#sources', ''),
 ('eu_impl', 1, 'Europe: 17 systems rolling out an informatics reform', '17 of 39', 'quote',
  '"As shown in Figure 1.5, 17 education systems were in the process of implementing curricular reforms on informatics education."', *EU22, 'p.36'),
 ('eu_dev', 1, 'Europe: 11 more drafting one', '11 of 39', 'quote',
  '"In 11 other education systems, the education authorities are planning the development of curricular reforms on informatics education."', *EU22, 'p.39'),
 ('eu_share', 1, 'Europe: systems reforming informatics', '28 of 39', 'quote',
  '"More than two thirds of the education systems are implementing or developing reforms that envisage the introduction of an informatics subject or the provision or updating of related learning outcomes"', *EU22, 'p.12'),
 # card 2
 ('std_2017', 2, 'US states with K-12 CS standards, 2017', '6', 'quote', '"In 2017, only six states had K–12 computer science standards."', *CODE(2024), 'p.10'),
 ('std_2018', 2, 'US states with K-12 CS standards, 2018', '22', 'quote', '"the number of states that have K-12 computer science standards has increased from 6 to 22"', *CODE(2018), 'p.17'),
 ('std_2019', 2, 'US states with K-12 CS standards, 2019', '34', 'quote', '"now 34 states have K–12 computer science standards, up from 6 in 2017."', *CODE(2019), 'p.16'),
 ('std_2020', 2, 'US states with K-12 CS standards, 2020', '37', 'chart', 'Read off the standards-over-time chart in the 2021 report.', *CODE(2021), 'p.29'),
 ('std_2021', 2, 'US states with K-12 CS standards, 2021', '39', 'chart', 'Read off the standards-over-time chart in the 2021 report.', *CODE(2021), 'p.29'),
 ('std_2023', 2, 'US states with K-12 CS standards, 2023', '42', 'count', 'Counted "Yes" rows in the Appendix 1 policy table (one row split across lines in the PDF). The 2022 report gives no single count.', *CODE(2023), 'Appendix 1'),
 ('std_2024', 2, 'US states with K-12 CS standards, 2024', '43', 'quote', '"Now, in 2024, 43 states have standards."', *CODE(2024), 'p.10'),
 ('std_2025', 2, 'US states with K-12 CS standards, 2025', '44', 'count', 'Counted the "standards" policy marked as met on each state page (one partial excluded).', 'CodeAI, State of AI + Computer Science 2025', 'https://advocacy.code.org/stateofcs/', 'state pages'),
 ('eu_lower', 2, 'Europe: informatics taught at ages 11–14', '35 of 39', 'quote',
  '"In general lower secondary education, informatics is taught as a distinct discipline in 35 education systems."', *EU22, 'p.11'),
 ('eu_primary', 2, 'Europe: informatics taught in primary', '23 of 39', 'quote',
  '"In primary education, informatics is taught as a distinct discipline in 23 education systems."', *EU22, 'p.11'),
 # card 3
 ('us_any', 3, 'US high schools teaching any AI topic to some students', '72%', 'count',
  'Survey item AI5: "Are any of the topics regarding AI listed taught to any students at your school?" High/secondary schools: Yes 72% (s.e. 2.0).', *NCES, 'AI5_y'),
 ('us_all', 3, 'US high schools teaching AI to all students', '16–25%', 'count',
  'Survey item AI5, "All students": ethical/appropriate uses of AI 25% (s.e. 2.0); technical knowledge 16% (s.e. 2.0). High/secondary schools.', *NCES, 'AI5_1, AI5_2'),
 ('us_rand', 3, 'US high-school students given AI guidance by teachers', '21%', 'quote',
  '"Smaller percentages of middle school students (14 percent) reported that they received guidance compared with high school students (21 percent)."', *RAND, 'p.8'),
 ('eu_ai', 3, 'Europe: AI in the lower-secondary curriculum', '12 of 38', 'quote',
  '"the national curricula of around one third of the education systems include AI-related competences." Count of "Yes" in Figure 4.4 / open-data Table 4.3: 12 of 38.', *EU26, 'report p.25, p.127'),
 # card 4
 ('ev_818', 4, 'Studies of AI in K-12 education → rigorous ones', '818 → 20', 'quote',
  '"We include the 818 papers in the Research Repository as of October 2025. 20 papers had strong enough causal evidence on educators and students to contribute to the key findings."', *SCALE, 'p.7'),
 ('ev_0', 4, 'Rigorous studies on teaching AI literacy', 'none', 'quote',
  '"there exists no high-quality causal research on the timely topic of developing student and teacher AI literacy."', *SCALE, 'p.29'),
 ('estonia', 4, 'Estonia\'s 9,000-student study has not reported', 'analysis from summer 2026', 'quote',
  '"The first student assessment took place in March, and the second at the end of May 2026. Data analysis will begin during the summer of 2026."', *LEAP, 'p.11'),
]
out = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'evidence.csv'
with out.open('w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['id', 'card', 'claim', 'value', 'check', 'quote', 'source', 'url', 'locator'])
    w.writerows(rows)
print(len(rows), 'rows ->', out)
