"""Build responsive, outlined Pagella biography and independent contact links."""
from pathlib import Path
from html import escape
from base64 import b64encode
import re
import subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
FONTS = {weight: TTFont(subprocess.check_output(['kpsewhich', f'texgyrepagella-{style}.otf'], text=True).strip()) for weight, style in [(400, 'regular'), (700, 'bold')]}
PARAGRAPHS = [
    'Undergraduate at Sun Yat-sen University & Research Intern at SimpleAI',
    'My research focuses on world models, video generation, and embodied intelligence.\nAt SimpleAI’s Simple World Lab, I work on embodied foundation models and frontier research in Physical Intelligence, exploring how generative models connect perception, reasoning, and action.\nI also develop AI-assisted research tools with InkMind.AI.',
    'I am currently applying for PhD positions in Hong Kong.',
]
ALT = ' '.join(' '.join(PARAGRAPHS).split())
BIO_VERSION = 'v10'
HIGHLIGHTS = {0: ['Sun Yat-sen University', 'SimpleAI'], 2: ['applying for PhD positions in Hong Kong']}
PALETTES = {'light': ('#41474e', '#14191f'), 'dark': ('#d0d7de', '#edf2f7')}


def kern(font, left, right):
    if not left or 'GPOS' not in font:
        return 0
    total = 0
    for lookup in font['GPOS'].table.LookupList.Lookup:
        for original in lookup.SubTable:
            table = original.ExtSubTable if lookup.LookupType == 9 and original.ExtensionLookupType == 2 else original
            if lookup.LookupType != 2 and table is original:
                continue
            if left not in table.Coverage.glyphs:
                continue
            value = None
            if table.Format == 1:
                index = table.Coverage.glyphs.index(left)
                value = next((p.Value1 for p in table.PairSet[index].PairValueRecord if p.SecondGlyph == right), None)
            elif table.Format == 2:
                a = table.ClassDef1.classDefs.get(left, 0)
                b = table.ClassDef2.classDefs.get(right, 0)
                value = table.Class1Record[a].Class2Record[b].Value1
            total += getattr(value, 'XAdvance', 0) or 0
    return total


class Type:
    def __init__(self):
        self.defs = {}

    def layout(self, value, size, weight):
        font = FONTS[weight]
        scale = size / font['head'].unitsPerEm
        previous, x, positions = None, 0, []
        cmap = font.getBestCmap()
        for char in value:
            glyph = cmap[ord(char)]
            x += kern(font, previous, glyph) * scale
            positions.append((glyph, x))
            x += font['hmtx'][glyph][0] * scale
            previous = glyph
        return positions, x, scale

    def measure(self, value, size, weight=400):
        return self.layout(value, size, weight)[1]

    def draw(self, value, x, y, size, color, weight=400, optical_weight=False):
        positions, advance, scale = self.layout(value, size, weight)
        glyphs = FONTS[weight].getGlyphSet()
        result = []
        for glyph, offset in positions:
            key = f'g{weight}-{FONTS[weight].getGlyphID(glyph)}'
            if key not in self.defs:
                pen = SVGPathPen(glyphs)
                glyphs[glyph].draw(pen)
                self.defs[key] = f'<path id="{key}" d="{pen.getCommands()}"/>'
            result.append(f'<use href="#{key}" xlink:href="#{key}" transform="translate({x+offset:.3f} {y:.3f}) scale({scale:.6f} {-scale:.6f})"/>')
        # Stroke is in font units, so the added weight scales with each glyph.
        stroke = f' stroke="{color}" stroke-width="14" stroke-linejoin="round" paint-order="stroke fill"' if optical_weight else ''
        return f'<g fill="{color}"{stroke}>{"".join(result)}</g>', advance

    def svg(self, width, height, title, content):
        return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{escape(title)}</title><defs>{"".join(self.defs.values())}</defs>{content}</svg>\n'


def profile_art(type, width, height, mobile, mode):
    scale = width / (600 if mobile else 1200)
    hero = (250 if mobile else 300) * scale
    margin = (34 if mobile else 52) * scale
    photo_width = (900 if mobile else 1200) * scale
    photo_height = photo_width * 3679 / 5517
    photo_y = (hero - photo_height) / 2
    fade_end = min(height, photo_y + photo_height)
    def data(name, mime):
        return f'data:{mime};base64,' + b64encode((OUT / name).read_bytes()).decode()
    # One photograph and one fade cover the masthead and biography continuously.
    type.defs['scene'] = f'''<linearGradient id="shade"><stop offset="0" stop-color="#dceffc" stop-opacity=".79"/><stop offset=".48" stop-color="#dceffc" stop-opacity=".66"/><stop offset=".76" stop-color="#dceffc" stop-opacity=".26"/><stop offset="1" stop-color="#dceffc" stop-opacity=".08"/></linearGradient>
<linearGradient id="fade" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{fade_end}"><stop offset="0" stop-color="white"/><stop offset="{hero*.68/fade_end}" stop-color="white"/><stop offset="{hero/fade_end}" stop-color="white" stop-opacity=".26"/><stop offset="{(hero+(fade_end-hero)*.45)/fade_end}" stop-color="white" stop-opacity=".09"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient>
<mask id="scene-fade"><rect width="{width}" height="{height}" fill="url(#fade)"/></mask>
<clipPath id="frame"><rect width="{width}" height="{height}" rx="{8*scale}"/></clipPath>'''
    art = f'''<g clip-path="url(#frame)"><g mask="url(#scene-fade)"><image href="{data('hong-kong-profile.jpg','image/jpeg')}" x="{width-photo_width}" y="{photo_y}" width="{photo_width}" height="{photo_height}"/><rect width="{width}" height="{height}" fill="url(#shade)"/><rect width="{width}" height="{height}" fill="#87c5ed" opacity=".10"/></g></g>'''
    for text, x, y, size, color, weight in [
        ('Yongxue Xu', margin-2*scale, (111 if mobile else 137)*scale, (54 if mobile else 68)*scale, '#244e6b', 700),
        ('World models & embodied intelligence', margin, (155 if mobile else 184)*scale, (21 if mobile else 23)*scale, '#305974', 400),
    ]:
        art += type.draw(text,x,y,size,color,weight)[0]
    art += f'''<image x="{margin}" y="{(174 if mobile else 205)*scale}" width="{(58 if mobile else 68)*scale}" height="{(58 if mobile else 68)*scale}" href="{data('sysu-logo.png','image/png')}"/><image x="{margin+(72 if mobile else 82)*scale}" y="{(181 if mobile else 213.5)*scale}" width="{(180 if mobile else 210)*scale}" height="{(44 if mobile else 51)*scale}" href="{data('simpleai-logo.png','image/png')}"/>'''
    return art


def biography(layout, width, size, inset, mode):
    type = Type()
    color, strong = PALETTES[mode]
    mobile = width <= 600
    hero = width * (250 / 600 if mobile else 300 / 1200)
    lift = width * (10 / 600 if mobile else 18 / 1200)
    y, line_height = hero + size * 1.05 + 6 - lift, size * 1.42
    body = []
    for index, paragraph in enumerate(PARAGRAPHS):
        spans = [(m.start(), m.end()) for phrase in HIGHLIGHTS.get(index, []) for m in re.finditer(re.escape(phrase), paragraph)]
        x = inset
        for token in re.finditer(r'Physical Intelligence\S*|\n|\S+', paragraph):
            if token.group() == '\n':
                x = inset
                y += line_height
                continue
            weight = 700 if any(a <= token.start() < b for a, b in spans) else 400
            word = token.group()
            word_width = type.measure(word, size, weight)
            gap = type.measure(' ', size) if x > inset else 0
            if x + gap + word_width > width - inset:
                x = inset
                gap = 0
                y += line_height
            assert word_width < width - 2 * inset
            rendered, _ = type.draw(word, x + gap, y, size, strong if weight == 700 else color, weight, optical_weight=weight == 400)
            body.append(rendered)
            x += gap + word_width
        y += line_height + size * .36
    height = round(y - line_height + size * .1)
    (OUT / f'research-bio-{layout}-{mode}-{BIO_VERSION}.svg').write_text(type.svg(width, height, 'Yongxue Xu. ' + ALT, profile_art(type, width, height, mobile, mode) + ''.join(body)))


LAYOUTS = [('narrow', 480, 31, 27.2), ('mobile', 600, 31, 34), ('compact', 800, 27, 800 * 52 / 1200), ('medium', 960, 26, 960 * 52 / 1200), ('desktop', 1200, 24, 52)]
for layout, width, size, inset in LAYOUTS:
    for mode in PALETTES:
        biography(layout, width, size, inset, mode)

CONTACTS = [
    ('home', 'Homepage', 'https://jerrysnow.me/'),
    ('playground', 'Playground', 'https://jerrysnow.me/blog/'),
    ('scholar', 'Google Scholar', 'https://scholar.google.com/citations?user=8PtwUrkAAAAJ&hl=en'),
    ('linkedin', 'LinkedIn', 'https://www.linkedin.com/in/%E6%B0%B8%E9%9B%AA-%E5%BE%90-6340a4415/'),
    ('email', 'Email', 'mailto:xuyx85@mail2.sysu.edu.cn'),
    ('x', 'Twitter', 'https://x.com/JerryXuri'),
    ('rednote', 'Rednote', 'https://xhslink.cn/o/60IapESrKEh'),
]

BRAND_COLORS = {'home': '#3779cf', 'playground': '#11998e', 'scholar': '#4285f4', 'linkedin': '#0a66c2', 'email': '#d95c4b', 'x': '#171717', 'rednote': '#ff2442'}

for name, label, _ in CONTACTS:
    version = 'v5' if name == 'rednote' else 'v4'
    icon = (OUT / 'contact' / f'blog-{name}.svg').read_text().split('viewBox="0 0 24 24">', 1)[1].strip().removesuffix('</svg>')
    for mode in (['light', 'dark'] if name == 'x' else ['brand']):
        color = '#648eaa'
        icon_color = '#f0f3f6' if name == 'x' and mode == 'dark' else BRAND_COLORS[name]
        type = Type()
        label_x = 51 if name == 'rednote' else 30
        content, advance = type.draw(label, label_x, 21, 16, color)
        width = round(advance + label_x + 7)
        transform = 'translate(0 -6.6) scale(1.8)' if name == 'rednote' else 'translate(0 4) scale(.916667)'
        content = f'<g transform="{transform}">{icon.replace("#648eaa", icon_color)}</g>' + content
        (OUT / 'contact' / f'blog-label-{name}-{mode}-{version}.svg').write_text(type.svg(width, 32, label, content))

readme = '<!-- The masthead and biography share one continuous skyline. -->\n'
readme += '\n<div>\n'
conditions = [('narrow', '(max-width: 360px)'), ('mobile', '(max-width: 480px)'), ('compact', '(max-width: 1000px)'), ('medium', '(max-width: 1199px)')]
for mode in PALETTES:
    fragment = f'#gh-{mode}-mode-only'
    readme += f'<a href="assets/research-bio-desktop-{mode}-{BIO_VERSION}.svg{fragment}"><picture>\n'
    for layout, condition in conditions:
        readme += f'  <source media="{condition}" srcset="assets/research-bio-{layout}-{mode}-{BIO_VERSION}.svg{fragment}">\n'
    readme += f'  <img src="assets/research-bio-desktop-{mode}-{BIO_VERSION}.svg{fragment}" width="100%" alt="{escape(ALT, quote=True)}">\n</picture></a>\n'
readme += '</div>\n\n<p align="center">\n'
for name, label, href in CONTACTS:
    version = 'v5' if name == 'rednote' else 'v4'
    for mode in (['light', 'dark'] if name == 'x' else ['brand']):
        fragment = f'#gh-{mode}-mode-only' if name == 'x' else ''
        readme += f'  <a href="{escape(href + fragment, quote=True)}">'
        readme += f'<img src="assets/contact/blog-label-{name}-{mode}-{version}.svg" height="32" alt="{label}">'
        readme += '</a>'
    readme += '&nbsp;\n'
readme += '</p>\n'
(ROOT / 'README.md').write_text(readme)
print('Built 10 responsive biography images and 7 Blog-style contact labels.')
