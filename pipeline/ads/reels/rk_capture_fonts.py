"""Fontes do Google servidas localmente para as capturas (mesmo trecho do rk_capture.py)."""
import base64
from pathlib import Path
FD = Path(__file__).parent / 'fonts'
LAT = 'U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD'
def gfonts_css():
    # O proxy desta sessão bloqueia fonts.googleapis.com: servimos as MESMAS fontes do Google (pacotes @fontsource) para a captura sair fiel.
    d = lambda f: 'data:font/woff2;base64,' + base64.b64encode((FD / f).read_bytes()).decode()
    css = ''
    for fam, lat, ext, w, extra in (('Archivo', 'archivo-latin-wght-normal.woff2', 'archivo-latin-ext-wght-normal.woff2', '100 900', ''),
                                    ('DM Sans', 'dm-sans-latin-opsz-normal.woff2', 'dm-sans-latin-ext-opsz-normal.woff2', '100 1000', '')):
        css += f"@font-face{{font-family:'{fam}';font-style:normal;font-display:swap;font-weight:{w};src:url({d(ext)}) format('woff2');unicode-range:U+0100-02AF,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}"
        css += f"@font-face{{font-family:'{fam}';font-style:normal;font-display:swap;font-weight:{w};src:url({d(lat)}) format('woff2');unicode-range:{LAT}}}"
    for w in ('700', '800'):
        css += f"@font-face{{font-family:'Syne';font-style:normal;font-display:swap;font-weight:{w};src:url({d(f'syne-latin-{w}-normal.woff2')}) format('woff2')}}"
    return css

