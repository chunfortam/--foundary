# -*- coding: utf-8 -*-
# Town map (scene 7): the picture carries only the fixed labels (districts, gate, river); every visitable place has its own
# label image, placed on the scene as a tile so the GM can show or hide it as the players learn of it.
#   python3 build/town_labels.py   ->  assets/maps/town.webp  +  assets/maps/town_labels/<key>.webp
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CJK = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
BLACK, RED = (20, 16, 12, 255), (170, 30, 24, 255)
# key, 中文, English, centre x, centre y (map pixels), red, shown at the start of 12 January, district, when the book reveals or changes it
PLACES = [
 ('stalls',   '沿街浮屋', 'Street stalls',          470, 676, 0, 1, 'Front Street 前街', ''),
 ('theatre',  '李家瓦子', 'Li Family Theatre',     1145, 458, 0, 1, 'Front Street 前街', ''),
 ('wangwu',   '王五分茶', "Wang Wu's Restaurant",   880, 528, 0, 1, 'Front Street 前街', 'Closed on the 12th; opens on the 13th'),
 ('pharmacy', '药铺',     'Pharmacy (HO2)',         640, 584, 0, 1, 'Front Street 前街', ''),
 ('lings',    '凌家',     'the Lings',             1008, 636, 0, 0, 'Front Street 前街', 'After the pharmacy event (Ling Xuchun 凌序春)'),
 ('teahouse', '茶楼',     'Teahouse',               415, 478, 0, 1, 'Front Street 前街', ''),
 ('coffin',   '棺材铺',   'Coffin Shop',           1330, 568, 0, 1, 'Front Street 前街', ''),
 ('house',    '某处民宅', "the widow's house",      110, 582, 0, 0, 'Front Street 前街', 'Address learned at the Gaol or the burning house'),
 ('wineshop', '酒肆',     'Wineshop',               180, 478, 0, 0, 'Front Street 前街', 'Address from tea master Song 宋择一 or Ling Xuchun 凌序春'),
 ('guildhall','会馆',     'Guildhall',             1020, 292, 0, 1, 'Back Street 后街', ''),
 ('burning',  '失火民宅', 'the burning house',     1160, 307, 0, 0, 'Back Street 后街', 'Catches fire when the party passes the Guildhall'),
 ('treasures','七宝行',   'Seven Treasures',       1350, 222, 0, 1, 'Back Street 后街', ''),
 ('crossing', '街口',     'Street Crossing',        768, 345, 1, 1, 'Back Street 后街', 'Fixed events at noon on the 12th and the 15th'),
 ('temple',   '寺庙',     'Temple',                1410, 318, 0, 1, 'Back Street 后街', ''),
 ('fan',      '范宅·灵堂', "Fan's residence",        160, 232, 0, 1, 'Magistracy 衙署', ''),
 ('xu',       '许宅',     'Prefect Xu',             470, 144, 0, 1, 'Magistracy 衙署', ''),
 ('niu',      '牛宅',     "Niu's house (Ashu)",     440, 292, 1, 1, 'Magistracy 衙署', 'Entered only for the assassination'),
 ('school',   '官学·藏书阁', 'School & Library',     652, 144, 0, 1, 'Magistracy 衙署', ''),
 ('gaol',     '监牢',     'Gaol',                   870, 154, 0, 1, 'Magistracy 衙署', ''),
 ('huts',     '渔民棚屋', "fishermen's huts",      1195, 737, 0, 1, 'Riverbank 汉江沿岸', ''),
 ('warships', '蒙古战船', 'Mongol warships',        135, 749, 1, 1, 'Riverbank 汉江沿岸', 'Guarded; reachable only during the feast, evening of the 17th'),
 ('pavilion', '解佩亭',   'Pavilion',               498, 767, 0, 1, 'Riverbank 汉江沿岸', ''),
 ('reeds',    '芦苇荡',   'the reeds',              298, 907, 0, 0, 'Riverbank 汉江沿岸', 'When they learn they can cross without killing the monster'),
 ('tower',    '塔楼',     'Watchtower',             377, 742, 0, 1, 'Riverbank 汉江沿岸', ''),
]
# Fixed labels painted into the picture: 中文, English, centre x, centre y, Chinese size, red
FIXED = [('蒙古大营', 'Mongol camp', 768, 40, 22, 1), ('北门', 'North Gate', 768, 120, 20, 0), ('衙署', 'Magistracy quarter', 218, 133, 28, 0),
         ('后街', 'Back Street', 1180, 147, 28, 0), ('前街', 'Front Street', 307, 650, 28, 0), ('汉江', 'the Han River', 1380, 984, 26, 0),
         ('往襄阳 →', 'to Southbright, across the water', 768, 982, 18, 0)]

def label(zh, en, size=20, red=False):
    fz, fe = ImageFont.truetype(CJK, size), ImageFont.truetype(CJK, max(11, int(size * 0.55)))
    pad = 8
    d0 = ImageDraw.Draw(Image.new('RGBA', (4, 4)))
    bz, be = d0.textbbox((0, 0), zh, font=fz), d0.textbbox((0, 0), en, font=fe)
    w = max(bz[2] - bz[0], be[2] - be[0]) + 2 * pad; hz = bz[3] - bz[1]; he = be[3] - be[1]
    h = hz + he + 4 + 2 * pad
    text = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(text); col = RED if red else BLACK
    d.text(((w - (bz[2] - bz[0])) / 2 - bz[0], pad - bz[1]), zh, font=fz, fill=col)
    d.text(((w - (be[2] - be[0])) / 2 - be[0], pad + hz + 4 - be[1]), en, font=fe, fill=col)
    # soft paper-coloured glow behind the letters so they read over rooftops
    a = text.split()[3].filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(2.2)).point(lambda v: min(255, int(v * 1.6)))
    glow = Image.new('RGBA', (w, h), (250, 244, 228, 0)); glow.putalpha(a.point(lambda v: int(v * 0.88)))
    return Image.alpha_composite(glow, text)

if __name__ == '__main__':
    base = Image.open(f'{ROOT}/assets/maps/town_base.webp').convert('RGBA')
    for zh, en, cx, cy, size, red in FIXED:
        im = label(zh, en, size, red); base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
    base.convert('RGB').save(f'{ROOT}/assets/maps/town.webp', quality=88)
    os.makedirs(f'{ROOT}/assets/maps/town_labels', exist_ok=True)
    for key, zh, en, cx, cy, red, shown, group, when in PLACES:
        im = label(zh, en, 24 if key == 'crossing' else 20, red); im.save(f'{ROOT}/assets/maps/town_labels/{key}.webp', lossless=True)
    print('wrote town.webp and', len(PLACES), 'labels')
