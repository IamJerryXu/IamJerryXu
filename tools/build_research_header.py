"""Compose the profile masthead with the original photograph and vector type."""
from pathlib import Path
from base64 import b64encode
ROOT = Path(__file__).resolve().parents[1]
photo = b64encode((ROOT / 'assets/hong-kong.jpg').read_bytes()).decode()
for mobile in (False, True):
    width,height=(600,280) if mobile else (1200,320)
    name_size=48 if mobile else 60
    margin=32 if mobile else 48
    image_width=900 if mobile else 1200
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Yongxue Xu · Jerry</title>
<desc id="desc">World models and embodied intelligence. Hong Kong skyline.</desc>
<defs>
<linearGradient id="shade"><stop offset="0" stop-color="#0d2635" stop-opacity=".96"/><stop offset=".48" stop-color="#0d2635" stop-opacity=".78"/><stop offset="1" stop-color="#0d2635" stop-opacity=".10"/></linearGradient>
<linearGradient id="floor" x2="0" y2="1"><stop offset="0" stop-color="#0d2635" stop-opacity="0"/><stop offset="1" stop-color="#0d2635" stop-opacity=".30"/></linearGradient>
<clipPath id="frame"><rect width="{width}" height="{height}" rx="8"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<image href="data:image/jpeg;base64,{photo}" x="{width-image_width}" y="0" width="{image_width}" height="{height}" preserveAspectRatio="xMidYMid slice"/>
<rect width="{width}" height="{height}" fill="url(#shade)"/>
<rect width="{width}" height="{height}" fill="url(#floor)"/>
<g font-family="Arial,Helvetica,sans-serif">
<text x="{margin}" y="{56 if mobile else 63}" font-size="12" letter-spacing="2.8" fill="#d8e3e9">RESEARCH / YONGXUE XU</text>
<text x="{margin-2}" y="{133 if mobile else 156}" font-size="{name_size}" font-weight="600" letter-spacing="-1.6" fill="#ffffff">Yongxue Xu<tspan font-size="{23 if mobile else 28}" font-weight="400" letter-spacing="0" fill="#d7e2e8"> / Jerry</tspan></text>
<text x="{margin}" y="{176 if mobile else 205}" font-size="{21 if mobile else 24}" fill="#e4edf1">World models &amp; embodied intelligence</text>
<path d="M{margin} {220 if mobile else 258}h28" stroke="#b8cdd7" stroke-width="2"/>
<text x="{margin+42}" y="{225 if mobile else 263}" font-size="13" letter-spacing=".4" fill="#d3e0e6">Sun Yat-sen University · SimpleAI</text>
</g></g></svg>'''
    (ROOT / 'assets' / ('research-header-mobile.svg' if mobile else 'research-header.svg')).write_text(svg)
print('Built desktop and mobile research mastheads.')
