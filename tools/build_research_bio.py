"""Build responsive, outlined Pagella biography and independent contact links."""
from pathlib import Path
from html import escape
import re
import subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
FONTS = {weight: TTFont(subprocess.check_output(['kpsewhich', f'texgyrepagella-{style}.otf'], text=True).strip()) for weight, style in [(400, 'regular'), (700, 'bold')]}
PARAGRAPHS = [
    'Undergraduate at Sun Yat-sen University · Research Intern at SimpleAI',
    'My research focuses on world models, video generation, and embodied intelligence. At SimpleAI’s Simple World Lab, I work on embodied foundation models and frontier research in Physical Intelligence. I also develop AI-assisted research tools with InkMind.AI.',
    'I am currently applying for PhD positions in Hong Kong.',
]
ALT = ' '.join(PARAGRAPHS)
HIGHLIGHTS = {0: ['Sun Yat-sen University', 'SimpleAI'], 2: ['applying for PhD positions in Hong Kong']}
PALETTES = {'light': ('#292e33', '#14191f'), 'dark': ('#d0d7de', '#edf2f7')}


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

    def draw(self, value, x, y, size, color, weight=400):
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
        return f'<g fill="{color}">{"".join(result)}</g>', advance

    def svg(self, width, height, title, content):
        return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{escape(title)}</title><defs>{"".join(self.defs.values())}</defs>{content}</svg>\n'


def biography(layout, width, size, inset, mode):
    type = Type()
    color, strong = PALETTES[mode]
    y, line_height = size * 1.05, size * 1.42
    body = []
    for index, paragraph in enumerate(PARAGRAPHS):
        spans = [(m.start(), m.end()) for phrase in HIGHLIGHTS.get(index, []) for m in re.finditer(re.escape(phrase), paragraph)]
        x = inset
        for token in re.finditer(r'\S+', paragraph):
            weight = 700 if any(a <= token.start() < b for a, b in spans) else 400
            word = token.group()
            word_width = type.measure(word, size, weight)
            gap = type.measure(' ', size) if x > inset else 0
            if x + gap + word_width > width - inset:
                x = inset
                gap = 0
                y += line_height
            assert word_width < width - 2 * inset
            rendered, _ = type.draw(word, x + gap, y, size, strong if weight == 700 else color, weight)
            body.append(rendered)
            x += gap + word_width
        y += line_height + size * .36
    height = round(y - line_height + size * .1)
    (OUT / f'research-bio-{layout}-{mode}-v3.svg').write_text(type.svg(width, height, ALT, ''.join(body)))


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
    ('rss', 'RSS', 'https://jerrysnow.me/blog/feed.xml'),
]

BRAND_COLORS = {'home': '#3779cf', 'playground': '#11998e', 'scholar': '#4285f4', 'linkedin': '#0a66c2', 'email': '#d95c4b', 'x': '#171717', 'rss': '#ee802f'}

for name, label, _ in CONTACTS:
    icon = (OUT / 'contact' / f'blog-{name}.svg').read_text().split('viewBox="0 0 24 24">', 1)[1].strip().removesuffix('</svg>')
    for mode in (['light', 'dark'] if name == 'x' else ['brand']):
        color = '#648eaa'
        icon_color = '#f0f3f6' if name == 'x' and mode == 'dark' else BRAND_COLORS[name]
        type = Type()
        content, advance = type.draw(label, 25, 21, 16, color)
        width = round(advance + 32)
        content = f'<g transform="translate(0 6) scale(.75)">{icon.replace("#648eaa", icon_color)}</g>' + content
        (OUT / 'contact' / f'blog-label-{name}-{mode}-v2.svg').write_text(type.svg(width, 32, label, content))

readme = (ROOT / 'README.md').read_text().split('</div>', 1)[0] + '</div>\n'
readme += '\n<div>\n'
conditions = [('narrow', '(max-width: 360px)'), ('mobile', '(max-width: 480px)'), ('compact', '(max-width: 1000px)'), ('medium', '(max-width: 1199px)')]
for mode in PALETTES:
    fragment = f'#gh-{mode}-mode-only'
    readme += f'<a href="assets/research-bio-desktop-{mode}-v3.svg{fragment}"><picture>\n'
    for layout, condition in conditions:
        readme += f'  <source media="{condition}" srcset="assets/research-bio-{layout}-{mode}-v3.svg{fragment}">\n'
    readme += f'  <img src="assets/research-bio-desktop-{mode}-v3.svg{fragment}" width="100%" alt="{escape(ALT, quote=True)}">\n</picture></a>\n'
readme += '</div>\n\n<p align="center">\n'
for name, label, href in CONTACTS:
    for mode in (['light', 'dark'] if name == 'x' else ['brand']):
        fragment = f'#gh-{mode}-mode-only' if name == 'x' else ''
        readme += f'  <a href="{escape(href + fragment, quote=True)}">'
        readme += f'<img src="assets/contact/blog-label-{name}-{mode}-v2.svg" height="32" alt="{label}">'
        readme += '</a>'
    readme += '&nbsp;\n'
readme += '</p>\n'
(ROOT / 'README.md').write_text(readme)
print('Built 10 responsive biography images and 7 Blog-style contact labels.')
