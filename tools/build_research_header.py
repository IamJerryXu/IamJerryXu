"""Compose the profile masthead with the original photograph and vector type."""
from pathlib import Path
from base64 import b64encode
ROOT = Path(__file__).resolve().parents[1]
photo = b64encode((ROOT / 'assets/hong-kong.jpg').read_bytes()).decode()
for mobile in (False, True):
    width,height=(600,250) if mobile else (1200,300)
    name_size=58 if mobile else 76
    margin=34 if mobile else 52
    image_width=900 if mobile else 1200
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Yongxue Xu · Jerry</title>
<desc id="desc">World models and embodied intelligence. Hong Kong skyline.</desc>
<defs>
<linearGradient id="shade"><stop offset="0" stop-color="#dceffc" stop-opacity=".98"/><stop offset=".48" stop-color="#dceffc" stop-opacity=".94"/><stop offset=".76" stop-color="#dceffc" stop-opacity=".48"/><stop offset="1" stop-color="#dceffc" stop-opacity=".20"/></linearGradient>
<linearGradient id="floor" x2="0" y2="1"><stop offset="0" stop-color="#87c5ed" stop-opacity=".30"/><stop offset="1" stop-color="#87c5ed" stop-opacity=".08"/></linearGradient>
<clipPath id="frame"><rect width="{width}" height="{height}" rx="8"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<image href="data:image/jpeg;base64,{photo}" x="{width-image_width}" y="0" width="{image_width}" height="{height}" preserveAspectRatio="xMidYMid slice"/>
<rect width="{width}" height="{height}" fill="url(#shade)"/>
<rect width="{width}" height="{height}" fill="url(#floor)"/>
<g font-family="Helvetica Neue,Helvetica,Arial,sans-serif" font-weight="400">
<text x="{margin-2}" y="{111 if mobile else 137}" font-family="Baskerville,Georgia,serif" font-size="{name_size}" font-weight="400" letter-spacing="-.5" fill="#244e6b">Yongxue Xu</text>
<text x="{margin}" y="{155 if mobile else 184}" font-size="{21 if mobile else 23}" letter-spacing=".2" fill="#305974">World models &amp; embodied intelligence</text>
<text x="{margin}" y="{206 if mobile else 240}" font-size="{15 if mobile else 16}" letter-spacing=".5" fill="#42667d">Sun Yat-sen University · SimpleAI</text>
</g></g></svg>'''
    (ROOT / 'assets' / ('research-header-mobile-v3.svg' if mobile else 'research-header-v3.svg')).write_text(svg)
print('Built desktop and mobile research mastheads.')
