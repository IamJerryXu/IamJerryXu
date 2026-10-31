"""Compose the profile masthead with the original photograph and vector type."""
from pathlib import Path
from base64 import b64encode
import subprocess
ROOT = Path(__file__).resolve().parents[1]
photo = b64encode((ROOT / 'assets/hong-kong.jpg').read_bytes()).decode()
fonts = ''
for weight, style in [(400, 'regular'), (700, 'bold')]:
    font = Path(subprocess.check_output(['kpsewhich', f'texgyrepagella-{style}.otf'], text=True).strip())
    data = b64encode(font.read_bytes()).decode()
    fonts += f'@font-face{{font-family:Pagella;font-weight:{weight};src:url(data:font/otf;base64,{data})}}'
seal = b64encode((ROOT / 'assets/sysu-logo.png').read_bytes()).decode()
logo = b64encode((ROOT / 'assets/simpleai-logo.png').read_bytes()).decode()
for mobile in (False, True):
    width,height=(600,250) if mobile else (1200,300)
    name_size=54 if mobile else 68
    margin=34 if mobile else 52
    image_width=900 if mobile else 1200
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Yongxue Xu · Jerry</title>
<desc id="desc">World models and embodied intelligence. Hong Kong skyline.</desc>
<defs>
<style>{fonts}</style>
<linearGradient id="shade"><stop offset="0" stop-color="#dceffc" stop-opacity=".98"/><stop offset=".48" stop-color="#dceffc" stop-opacity=".94"/><stop offset=".76" stop-color="#dceffc" stop-opacity=".48"/><stop offset="1" stop-color="#dceffc" stop-opacity=".20"/></linearGradient>
<linearGradient id="floor" x2="0" y2="1"><stop offset="0" stop-color="#87c5ed" stop-opacity=".30"/><stop offset="1" stop-color="#87c5ed" stop-opacity=".08"/></linearGradient>
<clipPath id="frame"><rect width="{width}" height="{height}" rx="8"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<image href="data:image/jpeg;base64,{photo}" x="{width-image_width}" y="0" width="{image_width}" height="{height}" preserveAspectRatio="xMidYMid slice"/>
<rect width="{width}" height="{height}" fill="url(#shade)"/>
<rect width="{width}" height="{height}" fill="url(#floor)"/>
<g font-family="Pagella,Palatino,serif" font-weight="400">
<text x="{margin-2}" y="{111 if mobile else 137}" font-family="Pagella,Palatino,serif" font-size="{name_size}" font-weight="700" letter-spacing="-.5" fill="#244e6b">Yongxue Xu</text>
<text x="{margin}" y="{155 if mobile else 184}" font-size="{21 if mobile else 23}" letter-spacing=".2" fill="#305974">World models &amp; embodied intelligence</text>
<image x="{margin}" y="{179 if mobile else 211}" width="{48 if mobile else 56}" height="{48 if mobile else 56}" href="data:image/png;base64,{seal}"/>
<image x="{margin + (72 if mobile else 82)}" y="{181 if mobile else 213.5}" width="{180 if mobile else 210}" height="{44 if mobile else 51}" href="data:image/png;base64,{logo}"/>
</g></g></svg>'''
    (ROOT / 'assets' / ('research-header-mobile-v4.svg' if mobile else 'research-header-v4.svg')).write_text(svg)
print('Built desktop and mobile research mastheads.')
