# -*- coding: utf-8 -*-
"""Build a single self-contained copy of the 24-page design book.

Hero-Storybook-24.html loads its photos and fonts from design-book/assets/, which is what
the app links to and what GitHub Pages serves. This script inlines every asset as a data
URI so the book also opens correctly as ONE file (e.g. when emailed to family).

    python design-book/make_selfcontained.py

Output: design-book/Hero-Storybook-24-FIXED.html (~8.7 MB, gitignored — regenerate it).
"""
import re, os, base64, mimetypes

DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(DIR, 'Hero-Storybook-24.html')
OUT = os.path.join(DIR, 'Hero-Storybook-24-FIXED.html')

MIME = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
        '.webp': 'image/webp', '.svg': 'image/svg+xml',
        '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf'}

src = open(SRC, encoding='utf-8').read()
cache = {}

def datauri(rel):
    if rel not in cache:
        path = os.path.join(DIR, rel)
        ext = os.path.splitext(rel)[1].lower()
        mime = MIME.get(ext) or mimetypes.guess_type(path)[0] or 'application/octet-stream'
        with open(path, 'rb') as fh:
            cache[rel] = f'data:{mime};base64,' + base64.b64encode(fh.read()).decode()
    return cache[rel]

refs = sorted(set(re.findall(r'assets/[A-Za-z0-9_.-]+', src)))
missing = [r for r in refs if not os.path.exists(os.path.join(DIR, r))]
if missing:
    raise SystemExit('missing assets: ' + ', '.join(missing))

for rel in refs:
    src = src.replace(rel, datauri(rel))

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(src)

print(f'inlined {len(refs)} assets')
print('wrote', OUT, f'{os.path.getsize(OUT) / 1048576:.1f} MB')
assert '"assets/' not in src, 'some relative refs survived'
