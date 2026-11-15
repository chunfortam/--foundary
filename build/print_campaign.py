# -*- coding: utf-8 -*-
"""Campaign GM pack (A4, English with Chinese on names): the Days 1–6 GM journal, the rules cards, every handout, and the GM who's who.
Usage: python3 build/print_campaign.py -> print/campaign-gm-pack.pdf"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import campaign as CP, content as C
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD_PREFIX = f'modules/{C.MOD}/'
TH = '/tmp/gongruo_thumbs'
def local(html):  # module asset paths -> small local thumbnails for Chrome (keeps the PDF small)
    from PIL import Image
    os.makedirs(TH, exist_ok=True)
    def sub(m):
        rel = m.group(1); src = os.path.join(ROOT, rel); dst = os.path.join(TH, os.path.basename(rel).replace('.webp', '.jpg'))
        if os.path.exists(src) and not os.path.exists(dst): Image.open(src).convert('RGB').resize((112, 112)).save(dst, quality=80)
        return f'src="file://{dst}"'
    return re.sub(r'src="' + re.escape(MOD_PREFIX) + r'([^"]+)"', sub, html)
PAGES = [CP.prep_html(), CP.sandbox_html(), CP.front_html(), CP.back_html(), CP.crossing_html(), CP.temple_html(), CP.magistracy_html(), CP.riverbank_html(),
         CP.finale_html(), CP.optional_html(), CP.endings_html(), CP.npcs_html(), CP.rules_cards_html()]
BODY = ''.join(f'<section>{p}</section>' for p in PAGES)
BODY += '<section>' + CP.H('Handouts', '文书与残页', 1) + '<p>Cut along the rules; hand over or read aloud as found.</p>' + ''.join(f'<div class="handout">{h}</div>' for _, h in CP.HANDOUTS) + '</section>'
BODY += f'<section class="cast">{local(C.cast_html(True))}</section>'
CSS = '''
@page { size: A4; margin: 10mm 11mm; }
body { font-family: "Noto Serif CJK SC", "Noto Serif", serif; font-size: 8.8pt; color: #111; margin: 0; line-height: 1.35; }
section { page-break-after: always; }
h1 { font-size: 15pt; margin: 0 0 6px; border-bottom: 2px solid #000; padding-bottom: 3px; }
h2 { font-size: 10.5pt; margin: 9px 0 3px; border-bottom: 1px solid #000; page-break-after: avoid; }
.zh-tag { font-size: 70%; font-weight: normal; color: #555; margin-left: .4em; }
p { margin: 3px 0; } ul { margin: 2px 0; padding-left: 16px; } li { margin-bottom: 2px; }
blockquote.read { border-left: 3px solid #999; padding: 2px 8px; margin: 4px 0; background: #f4f4f4; font-style: italic; page-break-inside: avoid; }
p.gmnote { font-size: 8pt; color: #333; border-top: 1px dashed #999; padding-top: 3px; }
.roll { font-weight: bold; background: #e8e8e8; padding: 0 3px; border-radius: 2px; white-space: nowrap; }
.card { border: 1px solid #000; border-radius: 3px; padding: 6px 10px; margin: 4px 0 10px; page-break-inside: avoid; }
.handout { border: 1px dashed #888; padding: 4px 10px 6px; margin: 6px 0; page-break-inside: avoid; } .handout h1 { font-size: 11pt; border-bottom: 1px solid #000; margin: 0 0 4px; }
table { border-collapse: collapse; width: 100%; } td, th { border: 1px solid #999; padding: 2px 4px; vertical-align: top; text-align: left; font-size: 8.2pt; }
th { background: #eee; }
table.cast td { border: none; border-bottom: 1px solid #bbb; padding: 4px; } td.cast-pic-cell { width: 60px; } img.cast-pic { width: 56px; height: 56px; border-radius: 50%; }
.gm-secret { color: #a0322d; }
'''
doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{BODY}</body></html>'
out = os.path.join(ROOT, 'print'); os.makedirs(out, exist_ok=True)
hp = os.path.join(out, '_campaign.html'); open(hp, 'w').write(doc)
pdf = os.path.join(out, 'campaign-gm-pack.pdf')
subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--allow-file-access-from-files', f'--print-to-pdf={pdf}', 'file://' + hp], check=True, capture_output=True)
os.remove(hp); print('wrote', pdf)
