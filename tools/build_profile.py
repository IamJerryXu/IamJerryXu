"""Build original, outlined profile artwork. Optional dependency: fonttools."""
from pathlib import Path
from html import escape
import os
from base64 import b64encode
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
FONT_DIR = Path(os.environ.get('PROFILE_SYSTEM_FONTS', '/System/Library/Fonts/Supplemental'))
COMIC = TTFont(OUT / 'fonts/ComicNeue-Bold.ttf')
REGULAR = TTFont(OUT / 'fonts/ComicNeue-Regular.ttf')
SANS = TTFont(FONT_DIR / 'Trebuchet MS.ttf')
CJK = TTFont(FONT_DIR / 'Songti.ttc', fontNumber=1)

def label(value, x, y, size, color, font=COMIC):
    parts = []
    for char in value:
        chosen = font if ord(char) in font.getBestCmap() else CJK
        cmap, glyphs = chosen.getBestCmap(), chosen.getGlyphSet()
        name = cmap[ord(char)]
        scale = size / chosen['head'].unitsPerEm
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        parts.append(f'<path fill="{color}" d="{pen.getCommands()}" transform="translate({x:.3f} {y}) scale({scale} {-scale})"/>')
        x += chosen['hmtx'][name][0] * scale
    return ''.join(parts)

def save(name, w, h, title, body):
    (OUT / f'{name}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{body}</svg>\n')

def wrapped(value, width, size, font=REGULAR):
    scale=size/font['head'].unitsPerEm
    cmap=font.getBestCmap()
    def measure(s): return sum(font['hmtx'][cmap[ord(c)]][0] for c in s)*scale
    lines=[]
    for word in value.split():
        if not lines or measure(lines[-1]+' '+word)>width: lines.append(word)
        else: lines[-1]+=' '+word
    return lines

def copy_block(name, paragraphs, mobile, mode, p):
    width=450 if mobile else 900
    size=21 if mobile else 23
    y=25
    body=''
    for paragraph in paragraphs:
        for line in wrapped(paragraph,width-12,size):
            body+=label(line,2,y,size,p['ink'],REGULAR)
            y+=30 if mobile else 32
        y+=8
    save(f'{name}-{"mobile" if mobile else "desktop"}-{mode}',width,y-15,' '.join(paragraphs),body)

def snow(x,y,r,c):
    lines = ''.join(f'<path transform="rotate({a} {x} {y})" d="M{x} {y-r}v{2*r}m{-r*.25} {-r*1.7} {r*.25} {r*.25} {r*.25} {-r*.25}"/>' for a in [0,60,120])
    return f'<g fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round">{lines}</g>'

def icon(kind, x, y, scale, p):
    ink, soft, mint = p['ink'], p['soft'], p['mint']
    shapes = {
        'world': f'<ellipse cx="34" cy="32" rx="26" ry="24" fill="{soft}"/><ellipse cx="34" cy="32" rx="12" ry="24"/><path d="M9 31h50M14 19q20 9 40 0M14 45q20-9 40 0"/><path d="m14 55 4 4M54 8l4-4"/>',
        'video': f'<rect x="7" y="10" width="48" height="44" rx="8" fill="{soft}"/><path d="M8 21h46M8 44h46M17 11v9M29 11v9M41 11v9M17 45v8M29 45v8M41 45v8"/><path d="m27 26 12 7-12 7Z" fill="{mint}"/>',
        'draw': f'<rect x="7" y="12" width="46" height="42" rx="6" fill="{soft}"/><path d="m16 44 12-15 10 8"/><path d="m41 13 7-5 6 7-21 26-9 4 2-10Z" fill="{mint}"/><path d="m38 18 9 7M26 35l7 6"/>',
        'paper': f'<path d="M12 7h30l12 12v39H12Z" fill="{soft}"/><path d="M42 7v13h12M22 30h23M22 38h18M22 46h12"/><path d="m4 24 3-1m52 21 3 1"/>',
        'home': f'<path d="m7 29 25-20 25 20M14 24v31h37V24" fill="{soft}"/><path d="M26 54V38h12v16M27 24h10"/>',
        'scholar': f'<path d="m4 26 28-14 28 14-28 14Z" fill="{soft}"/><path d="M16 33v14q16 10 32 0V33M58 28v21"/>',
        'mail': f'<rect x="6" y="15" width="52" height="36" rx="7" fill="{soft}"/><path d="m9 19 23 18 23-18M9 47l15-15M55 47 40 32"/>',
    }
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{ink}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round">{shapes[kind]}</g>'

def world_scene(x,y,scale,p):
    b = f'<path d="M12 150C-3 49 53 4 133 13c84 9 123 73 96 134-22 51-75 55-127 44-48-9-84-11-90-41Z" fill="{p["wash"]}"/>'
    b += f'<ellipse cx="121" cy="106" rx="71" ry="67" fill="{p["soft"]}" stroke="{p["ink"]}" stroke-width="2"/><ellipse cx="121" cy="106" rx="31" ry="67" fill="none" stroke="{p["line"]}" stroke-width="1.5"/>'
    b += f'<path d="M51 106h140M62 73q59 28 118 0M62 139q59-28 118 0" fill="none" stroke="{p["line"]}" stroke-width="1.5"/>'
    b += f'<path d="m90 64 19-12 22 10 10 19-20 10-24-8ZM145 116l20 7 4 21-16 11-14-16Z" fill="{p["mint"]}" stroke="{p["ink"]}" stroke-width="1.5"/>'
    b += f'<g transform="rotate(-11 126 139)"><rect x="24" y="119" width="198" height="48" rx="7" fill="{p["bg"]}" stroke="{p["ink"]}" stroke-width="2"/>'
    for i in range(4):
        xx=33+i*46
        b += f'<rect x="{xx}" y="126" width="38" height="34" rx="3" fill="{p["wash"]}"/><path d="m{xx+4} 150 11-10 8 5 10-14" fill="none" stroke="{p["accent"]}" stroke-width="2"/><circle cx="{xx+11+i*5}" cy="135" r="3" fill="{p["green"]}"/>'
    b += '</g>'
    b += f'<path d="M34 77C-11 124 27 202 94 192m-8-6 8 6-9 3M203 58c33 8 49 29 41 57" fill="none" stroke="{p["accent"]}" stroke-width="2" stroke-linecap="round" stroke-dasharray="3 5"/>'
    b += snow(205,31,10,p['accent'])+snow(27,38,8,p['line'])
    return f'<g transform="translate({x} {y}) scale({scale})">{b}</g>'

PROJECTS = [
    ('track4d', 'LMM-Track4D', 'world', '4D REASONING', 'Multi-view object tracking and trajectory reasoning.', ['Multi-view object tracking', 'and trajectory reasoning.']),
    ('posreasoner', 'POSReasoner', 'video', 'VIDEO UNDERSTANDING', 'Persistent object states for video instance segmentation.', ['Persistent object states for', 'video instance segmentation.']),
    ('astradraw', 'AstraDraw', 'draw', 'RESEARCH TOOLS', 'Editable paper figures, guided by your own visual references.', ['Editable paper figures, guided by', 'your own visual references.']),
    ('ccfa', 'CCFA-Skills', 'paper', 'RESEARCH TOOLS', 'Connected skills for ideas, evidence, writing and review.', ['Connected skills for ideas,', 'evidence, writing and review.']),
]

def build():
    for mode in ['light','dark']:
        mascot = OUT / ('jerry-scarf-dark.png' if mode == 'dark' else 'jerry-scarf.png')
        mascot_data = b64encode(mascot.read_bytes()).decode('ascii') if mascot.exists() else None
        p = dict(bg='#FFFFFF', ink='#24495B', secondary='#506B78', accent='#4F8FAA', green='#456F60', line='#A6CAD6', soft='#E9F3F6', mint='#D6E8DC', wash='#F3F8FA', border='#D5E4E9') if mode=='light' else dict(bg='#0D1117', ink='#D5EAF2', secondary='#A0B7C3', accent='#8AC4D9', green='#A5CFB8', line='#43636E', soft='#213843', mint='#345749', wash='#15252E', border='#2D4652')
        for mobile in [False,True]:
            size='mobile' if mobile else 'desktop'
            w,h=(450,212) if mobile else (900,226)
            b=f'<rect width="{w}" height="{h}" rx="14" fill="{p["bg"]}"/>'
            b+=label('Yongxue Xu  /  徐永雪',2,32,21,p['secondary'],REGULAR)
            b+=label("Hi, I'm Jerry.",0,96 if mobile else 105,49 if mobile else 62,p['ink'])
            b+=label('Video generation & world models',2,141 if mobile else 155,23 if mobile else 28,p['accent'],REGULAR)
            b+=label('4D understanding  ·  Research tools',2,176 if mobile else 192,21 if mobile else 24,p['secondary'],REGULAR)
            if mascot_data:
                mx,my,mw,mh=(329,13,118,118) if mobile else (624,0,262,222)
                b+=f'<image x="{mx}" y="{my}" width="{mw}" height="{mh}" href="data:image/png;base64,{mascot_data}" preserveAspectRatio="xMidYMid meet"/>'
            elif mobile: b+=world_scene(338,14,.37,p)
            else: b+=world_scene(620,0,1,p)
            save(f'hero-{size}-{mode}',w,h,'Yongxue Xu — Hi, I’m Jerry. Video generation, world models and 4D understanding.',b)
            copy_block('bio', ["I'm an undergraduate at Sun Yat-sen University and a member of InkMind.AI.", "I study generative models for visual understanding and build research tools with friends."], mobile, mode, p)
            copy_block('connect', ["Always happy to exchange ideas and collaborate. You'll find more about my work and my WeChat contact on my homepage."], mobile, mode, p)
            for key,title,kind,category,desc,lines in PROJECTS:
                w,h=(450,150) if mobile else (900,98)
                b=f'<rect x="1" y="1" width="{w-2}" height="{h-6}" rx="12" fill="{p["bg"]}" stroke="{p["border"]}"/>'
                b+=f'<rect x="{16 if mobile else 17}" y="16" width="52" height="52" rx="14" fill="{p["wash"]}"/>'
                b+=icon(kind,17,18,.76,p)
                b+=label(title,82,47,29,p['ink'])
                if mobile:
                    for j,line in enumerate(lines): b+=label(line,25,100+25*j,20,p['secondary'],SANS)
                else:
                    b+=label(desc,82,76,21,p['secondary'],SANS)
                    b+=label(category,620,39,13,p['accent'],SANS)
                b+=f'<path d="M{w-38} 27h13m-6-6 6 6-6 6" fill="none" stroke="{p["green"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
                save(f'project-{key}-{size}-{mode}',w,h,title+': '+desc,b)
        for key,title,kind in [('home','Homepage','home'),('scholar','Scholar','scholar'),('mail','Email','mail')]:
            width={'home':150,'scholar':136,'mail':114}[key]
            b=f'<rect x="2" y="2" width="{width-4}" height="44" rx="14" fill="{p["wash"]}" stroke="{p["border"]}"/>'
            b+=icon(kind,9,7,.49,p)+label(title,46,31,21,p['ink'])
            save(f'nav-{key}-{mode}',width,49,title,b)
        b=icon('paper',0,2,.60,p)+label('Selected work',48,32,28,p['ink'])
        b+=f'<path d="M240 30h360" stroke="{p["border"]}" stroke-width="1.3"/>'
        save(f'heading-work-{mode}',600,48,'Selected work',b)
        b=snow(16,28,8,p['accent'])+label('Never economize on your future.',36,36,25,p['secondary'],REGULAR)
        save(f'closing-{mode}',500,62,'Never economize on your future.',b)
    print('Built profile artwork for desktop/mobile and light/dark themes.')

if __name__=='__main__': build()
