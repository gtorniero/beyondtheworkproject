"""18/11 (Gui, comentários na Mesa): ADC-RZ-18-SP-v1 "deixe o CTA bem maior" · ADC-RZ-19-SP-v1 "CTA MAIOR".
Versões novas do MESMO criativo (mesmo título, número, tela, texto e cores); só o botão de CTA cresce, em todos os formatos.
O botão fica no mesmo lugar (rodapé, à esquerda, ancorado embaixo); a URL e a linha fina continuam embaixo dele.
Registrado no adapt1811.py (import kvcta)."""
import kvx, kvab  # noqa: kvab registra os -SP-v1
K = kvx.K

# fonte e respiro do botão por formato (v1 → v2): cerca de 1,6× a fonte, botão bem mais alto e largo
BIG = {
    'story': dict(cta=64, cta_p=(36, 54)),
    'feed45': dict(cta=54, cta_p=(30, 46)),
    'sq': dict(cta=48, cta_p=(26, 40)),
    'land': dict(cta=36, cta_p=(18, 30)),
    '16x9': dict(cta=58, cta_p=(32, 50)),
}
NEW = {'ADC-RZ-18-SP-v2': 'ADC-RZ-18-SP-v1', 'ADC-RZ-19-SP-v2': 'ADC-RZ-19-SP-v1'}
for new, old in NEW.items():
    kvx.SPEC[new] = dict(kvx.SPEC[old], big_cta=True)
    K.HERO[new] = None

# 4:5: o botão maior encostava no celular (RZ-18) e cobria o rodapé do pôster (RZ-19). Só no 4:5 o visual da direita
# fica um pouco menor (mesmo topo, mesma tela, nada cortado) para o botão caber sem cobrir nada.
import kvrz
PO45 = (360, 640, 430)            # pôster: era (410, 615, 430)
PH45 = {(420, 610, 380): (390, 630, 380)}  # celular: era 420 px de largura
_phone = K.phone
def _phone45(src, pw, px, py, *a, **k):
    pw, px, py = PH45.get((pw, px, py), (pw, px, py))
    return _phone(src, pw, px, py, *a, **k)

_page = K.page
def page(v, fmt, anim=False):
    if not kvx.SPEC[v].get('big_cta'): return _page(v, fmt, anim)
    g0, t = kvx.G[fmt]; p0 = kvrz.P['feed45']
    kvx.G[fmt] = (dict(g0, **BIG[fmt]), t)
    if fmt == 'feed45': kvrz.P['feed45'] = PO45; K.phone = _phone45
    try:
        h = _page(v, fmt, anim)
    finally:
        kvx.G[fmt] = (g0, t); kvrz.P['feed45'] = p0; K.phone = _phone
    return h.replace('border-radius:16px;padding', 'border-radius:22px;padding', 1)
kvx.page = page; K.page = page
