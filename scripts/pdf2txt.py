import sys
from pypdf import PdfReader
r = PdfReader(sys.argv[1])
open(sys.argv[2], 'w').write('\n'.join(f'<<PAGE {i+1}>>\n' + (p.extract_text() or '') for i, p in enumerate(r.pages)))
print(len(r.pages), 'pages')
