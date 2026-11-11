"""Stories avulsos (briefing de 11/11: cobrir as lacunas de 16/11 a 06/12). Não mexe nos packs; gera PNG 1080×1920, prévia JPG e editável HTML.
Uso: python3 stories_extra.py <saida> [IDs]
Regras: CTA na arte, sem adesivo, sem etiqueta de exemplo, só ícones/logos oficiais, números de produto só os do site (conferidos em 11/11).
Layout em fluxo dentro da zona segura do story (290 a 1590 px), para nada se sobrepor."""
import asyncio, sys
from pathlib import Path
import common as C
import retrozap as R
import sportdna as D
from playwright.async_api import async_playwright

STORIES = {}


def story(sid, brand, data, title, notes, inner, fonts, css, cls='', bg=''):
    body = (f'<section class="page {cls}" style="width:1080px;height:1920px;{bg}">{inner[0]}'
            f'<div class="abs" style="left:80px;right:80px;top:290px;bottom:330px;display:flex;flex-direction:column;gap:34px">{inner[1]}</div></section>')
    STORIES[sid] = dict(id=sid, brand=brand, data=data, title=title, notes=notes, html=C.doc(sid, fonts, css, body, 1080, 1920))


BOT = 'margin-top:auto;display:flex;flex-direction:column;gap:22px'


# ------------------------------------------------------------------ RETROZAP
def card_row(ic, txt, casa='grupo'):
    return (f'<div style="display:flex;align-items:center;gap:22px;padding:18px 0;border-top:3px solid {"var(--clinha)" if casa == "casal" else "var(--linha)"}">'
            f'{R.icon(ic, 58, casa)}<div style="font-size:34px;font-weight:700;line-height:1.2">{txt}</div></div>')


def rz_card(casa, head, big, label, rows):
    box = ('background:#fff;border:4px solid var(--clinha);border-radius:40px;transform:rotate(1.2deg);box-shadow:0 30px 70px rgba(94,11,43,.18)' if casa == 'casal'
           else 'background:var(--acai);border-radius:34px;transform:rotate(-1.2deg);box-shadow:0 30px 70px rgba(0,0,0,.45)')
    return (f'<div style="{box};padding:36px 46px 14px">'
            f'<div style="display:flex;align-items:center;gap:18px">{R.taca(56, casa)}<span class="mono" style="font-size:24px;letter-spacing:.08em;color:{"var(--vinho2)" if casa == "casal" else "var(--neblina)"}">{head}</span></div>'
            f'<div class="t hl" style="font-size:180px;margin-top:22px">{big}</div>'
            f'<div style="font-size:38px;font-weight:700;margin:4px 0 14px">{label}</div>'
            + ''.join(card_row(i, t, casa) for i, t in rows) + '</div>')


story('R-S20', 'Retrozap', '16/11/2026 (seg)', 'Retrospectiva: o "bom dia" das 6h vira número',
      'Situação de grupo reconhecível (o "bom dia" das 6h) e como ela aparece na retrospectiva: o Retrozap conta "bom dia", horários e mensagens por pessoa (FAQ do site). Números e nome de um grupo fictício, sem etiqueta. Sem troféu, sem preço. Motivo de envio: mandar no grupo que tem um desses.',
      ('', '<div class="mono" style="font-size:28px;color:var(--neblina);letter-spacing:.08em">SEGUNDA · 6H12</div>'
           '<div class="t" style="font-size:100px;margin-top:-14px">Todo grupo tem o “bom dia” das <span class="hl">6h da manhã.</span></div>'
           '<div style="font-size:42px;font-weight:700">Na retrospectiva, ele vira número:</div>'
           + rz_card('grupo', 'RETROSPECTIVA 2026 · RESUMO DO GRUPO', '1.932', '“bom dia” mandados no ano',
                     [('black-sun-with-rays', 'Quem mais mandou: Tio Beto, 611'), ('speech-balloon', 'Horário mais agitado do grupo: 22h')])
           + f'<div style="{BOT}"><div style="font-size:42px;font-weight:700;color:var(--manga)">Manda no grupo que tem um desses.</div>'
           f'<div style="display:flex;align-items:center;gap:28px">{R.assinatura(260)}<span style="font-size:30px;font-weight:700">1º grupo grátis · retrozap.com.br</span></div></div>'),
      R.FONTS, R.CSS)

story('R-S21', 'Retrozap', '20/11/2026 (sex)', 'Retrospectiva de casal: o "vou dormir" que não dorme',
      'Casa Casal (creme, cereja, vinho). Situação de casal reconhecível (o "vou dormir" e a última mensagem 1h40) e como os horários aparecem na retrospectiva de casal. Números de um casal fictício, sem etiqueta. Oferta conforme o FAQ do site em 11/11: casal no acesso completo, R$ 8,99, pagamento único. Não repete o "mesmo sofá" (R-S8) nem o "chegou?" (R-C4). Motivo de envio: mandar pro parceiro.',
      ('', '<div class="mono" style="font-size:28px;color:var(--cereja);letter-spacing:.08em">FERIADO · 23H48</div>'
           '<div class="t" style="font-size:104px;margin-top:-14px">“Vou dormir.” Última mensagem: <span class="hl">1h40.</span></div>'
           '<div style="font-size:42px;font-weight:700">Na retrospectiva de casal, isso vira número:</div>'
           + rz_card('casal', 'VOCÊS DOIS · 2026', '23h48', 'o horário em que vocês mais conversam',
                     [('crescent-moon', 'Mensagem mais tarde do ano: 2h13'), ('two-hearts', '18.420 mensagens trocadas')])
           + f'<div style="{BOT}"><div style="font-size:42px;font-weight:700;color:var(--cereja)">Manda pro seu amor que fala “vou dormir” e não dorme.</div>'
           f'<div style="display:flex;align-items:center;gap:28px">{R.assinatura(260, "casal")}<span style="font-size:28px;font-weight:700;line-height:1.3">Retrospectiva de casal no acesso completo:<br>R$ 8,99, pagamento único · retrozap.com.br</span></div></div>'),
      R.FONTS, R.CSS, cls='casal')

# ------------------------------------------------------------------ SPORT DNA
DCSS = D.CSS + """
.opt{display:flex;align-items:center;gap:28px;border:3px solid var(--line);border-radius:26px;padding:24px 32px;font-size:40px;font-weight:700;margin-bottom:18px}
.opt b{font-family:'JetBrains Mono',monospace;font-size:32px;width:62px;height:62px;border-radius:16px;display:flex;align-items:center;justify-content:center;background:var(--surface);flex:none}
.opt.ok{border-color:var(--run)} .opt.ok b{background:var(--run);color:var(--ink)}
.chk{display:flex;align-items:center;gap:26px;padding:16px 0;border-top:3px solid rgba(10,10,10,.16);font-size:40px;font-weight:700}
.chk i{flex:none;width:56px;height:56px;border:5px solid var(--ink);border-radius:12px}
"""

story('D-S20', 'SPORT DNA', '16/11/2026 (seg)', 'RUN · teste rápido: qual número comprar?',
      'Dúvida concreta de escolha (numeração do tênis de corrida), em formato de teste com a resposta na arte. Resposta e explicação são do site do RUN DNA ("Comprar o número do dia a dia: o pé incha ao correr…"; o teste define o número, ½ ou 1 acima). Sem ilustração de equipamento, sem marca. Motivo de envio: amigo que vai comprar tênis na Black Friday.',
      ('<div class="abs grid-bg" style="inset:0"></div>',
       '<div class="lbl" style="color:var(--run)">RUN DNA · TESTE RÁPIDO</div>'
       '<div class="t" style="font-size:100px;margin-top:-14px">Tênis de corrida: qual <span style="color:var(--run)">número</span> comprar?</div>'
       '<div><div class="opt"><b>A</b>O mesmo do sapato</div><div class="opt ok"><b>B</b>Meio número ou um acima</div><div class="opt" style="margin-bottom:0"><b>C</b>Um abaixo, pra firmar o pé</div></div>'
       '<div style="border-left:8px solid var(--run);padding-left:34px"><div class="t" style="font-size:56px">Na maioria das vezes, B.</div>'
       '<div style="font-size:36px;line-height:1.35;margin-top:12px;color:#D9D9D6">O pé incha ao correr. Sem um dedo de folga na ponta vêm unha roxa e bolha.</div></div>'
       f'<div style="{BOT}"><div style="font-size:40px;font-weight:700">O RUN DNA diz o seu número e o seu modelo. <span style="color:var(--run)">Teste grátis · 3 minutos.</span></div>'
       f'<div style="display:flex;align-items:center;gap:34px">{D.logo("rundna-logo-fundo-escuro", 300)}<span style="font-size:28px;color:var(--muted);line-height:1.35">sportdna.com.br/run<br>Nenhuma marca paga para aparecer.</span></div></div>'),
      D.FONTS, DCSS)

ITENS = ['Pego a onda na parede, antes de quebrar', 'Fico de pé rápido, num movimento só', 'Ando na parede (diagonal)', 'Faço cavada', 'Faço batida', 'Entro no tubo']
story('D-S21', 'SPORT DNA', '18/11/2026 (qua)', 'SURF · checklist: seu nível não é o tempo de prancha',
      'Pequeno teste de escolha: os itens são as opções reais da pergunta "O que você já faz na onda?" do SURF DNA; o site diz que a litragem é calculada pelo que você já faz na onda, não só pelo tempo de surf. Sem ilustração de prancha, sem marca. Motivo de envio: marcar as suas e mandar pro parceiro de surf.',
      ('', '<div class="lbl" style="color:var(--ink)">SURF DNA · CHECKLIST</div>'
           '<div class="t" style="font-size:96px;margin-top:-14px">Seu nível no surf não é o tempo de prancha.</div>'
           '<div style="font-size:40px;font-weight:700">É o que você já faz na onda. Quantas destas você já faz?</div>'
           '<div>' + ''.join(f'<div class="chk"><i></i>{x}</div>' for x in ITENS) + '</div>'
           f'<div style="{BOT}"><div style="font-size:38px;font-weight:700">É isso que define quanto a sua prancha precisa boiar. Prévia grátis · 3 minutos · sem cadastro.</div>'
           f'<div style="display:flex;align-items:center;gap:34px">{D.logo("surfdna-logo-preto", 300)}<span style="font-size:28px;line-height:1.35">sportdna.com.br/surf<br>Tira print, marca as suas e manda pro parceiro de surf.</span></div></div>'),
      D.FONTS, DCSS, cls='light', bg='background:var(--surf)')


async def main(out, ids):
    out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for sid, s in STORIES.items():
            if ids and sid not in ids: continue
            (out / f'{sid}.html').write_text(s['html'])
            await pg.goto((out / f'{sid}.html').resolve().as_uri()); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(200)
            await pg.locator('.page').first.screenshot(path=str(out / f'{sid}.png'))
            print(sid, flush=True)
        await b.close()
    from PIL import Image
    for sid in STORIES:
        if (out / f'{sid}.png').exists(): Image.open(out / f'{sid}.png').convert('RGB').resize((540, 960), Image.LANCZOS).save(out / f'{sid}.jpg', quality=86)


if __name__ == '__main__':
    asyncio.run(main(Path(sys.argv[1]), set(sys.argv[2:])))
