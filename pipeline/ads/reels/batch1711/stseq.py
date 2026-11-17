"""Sequências de stories 17/11–07/12 (pedido do Gui, 17/11): cada story vira uma historinha de 3 quadros.
Quiddo: quadro 1 refeito com matéria (Geografia, Português, História, Ciências, Matemática), quadro 2 resposta + explicação, quadro 3 CTA de aula/treinamento.
Retrozap e SPORT DNA: o quadro 1 aprovado fica; entram o 2 (o gancho vira produto) e o 3 (CTA claro).
Uso: python3 stseq.py <saída>"""
import sys, os, asyncio, base64, json
from pathlib import Path
P = Path(__file__).resolve().parent.parent / 'social' / 'pipeline'; sys.path.insert(0, str(P))
OUT = Path(sys.argv[1]).resolve(); OUT.mkdir(parents=True, exist_ok=True)
WK = Path(__file__).resolve().parent
os.chdir(P)
import common as C
import quiddo as Q, retrozap as R, sportdna as D
C.PIECES.clear()

DATAS = ['17/11', '18/11', '19/11', '20/11', '21/11', '22/11', '23/11', '24/11', '25/11', '26/11', '27/11', '28/11', '29/11', '30/11',
         '01/12', '02/12', '03/12', '04/12', '05/12', '06/12', '07/12']
SEM = ['ter', 'qua', 'qui', 'sex', 'sáb', 'dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom', 'seg']
SEM = ['ter', 'qua', 'qui', 'sex', 'sáb', 'dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom', 'dom']
# 07/12 é segunda; corrige
SEM[-1] = 'seg'
AVS = ['arara.festa.-.2', 'capivara.-.-.4', 'tatu.bone.-.1', 'onca.-.-.5', 'coruja.-.-.3', 'boto.-.-.6', 'tucano.gorro.-.7']
MAT = {'Geografia': '#1E7FD6', 'Português': '#E5383B', 'História': '#FF7A1A', 'Ciências': '#13A07A', 'Matemática': '#7B4BD6'}

# ---------------- QUIDDO: (id, matéria, pergunta, opções, certa, explicação, cta)  cta: 'aula' | 'treino'
QZ = [
 ('Q-S7', 'Ciências', 'Quantos ossos tem o corpo de um adulto?', ['106', '206', '306', '406'], 1, 'Um bebê nasce com uns 300; vários se juntam no crescimento. O maior é o fêmur, na coxa.', 'aula'),
 ('Q-S8', 'Ciências', 'Qual é o maior roedor do mundo?', ['Rato-gigante', 'Capivara', 'Castor', 'Paca'], 1, 'A capivara passa dos 60 kg e vive perto de rios e lagos, do Brasil à Argentina.', 'aula'),
 ('Q-S9', 'Ciências', 'Qual é o planeta mais quente do Sistema Solar?', ['Mercúrio', 'Vênus', 'Marte', 'Júpiter'], 1, 'Mercúrio é o mais perto do Sol, mas Vênus é o mais quente: a atmosfera de gás carbônico prende o calor e passa de 460 °C.', 'treino'),
 ('Q-S10', 'Geografia', 'Quantos estados tem o Brasil?', ['24', '25', '26', '27'], 2, 'São 26 estados e o Distrito Federal: 27 unidades da federação.', 'aula'),
 ('Q-S11', 'Geografia', 'Qual é o maior bioma do Brasil?', ['Cerrado', 'Mata Atlântica', 'Amazônia', 'Caatinga'], 2, 'A Amazônia cobre quase metade do território brasileiro.', 'aula'),
 ('Q-S12', 'Português', 'Qual é o plural de "cidadão"?', ['Cidadões', 'Cidadães', 'Cidadãos', 'Cidadãoes'], 2, 'Cidadão faz cidadãos, como irmão faz irmãos. Já pão faz pães e leão faz leões: cada um tem o seu.', 'treino'),
 ('Q-S13', 'Português', 'Complete: "___ dois anos que a gente não se vê."', ['Faz', 'Fazem', 'Fizeram', 'Faziam'], 0, 'Quando indica tempo, o verbo "fazer" fica no singular: faz dois anos, faz dez dias.', 'aula'),
 ('Q-S14', 'Geografia', 'Qual é a capital da Austrália?', ['Sydney', 'Melbourne', 'Camberra', 'Perth'], 2, 'Sydney é a maior cidade, mas a capital é Camberra, planejada para ser a sede do governo.', 'aula'),
 ('Q-S15', 'Português', '"Mal" ou "mau"? Ele é um ___ perdedor.', ['Mal', 'Mau'], 1, 'Mau é o contrário de bom; mal é o contrário de bem. Ele é um mau perdedor; ele joga mal.', 'treino'),
 ('Q-S16', 'Geografia', 'Qual é o maior oceano do mundo?', ['Atlântico', 'Índico', 'Pacífico', 'Ártico'], 2, 'O Pacífico é maior do que todos os continentes juntos.', 'aula'),
 ('Q-S17', 'Matemática', 'Quantos minutos tem um dia?', ['1.240', '1.440', '1.640', '2.400'], 1, '24 horas × 60 minutos = 1.440 minutos.', 'aula'),
 ('Q-S18', 'Geografia', 'Qual é o menor país do mundo?', ['Mônaco', 'Vaticano', 'San Marino', 'Malta'], 1, 'O Vaticano fica dentro de Roma e tem menos de 0,5 km².', 'treino'),
 ('Q-S19', 'História', 'Em que ano o ser humano pisou na Lua pela primeira vez?', ['1959', '1965', '1969', '1972'], 2, 'Foi em julho de 1969, na missão Apollo 11.', 'aula'),
 ('Q-S20', 'História', 'Quem assinou a Lei Áurea, em 1888?', ['Dom Pedro I', 'Princesa Isabel', 'Dom Pedro II', 'Tiradentes'], 1, 'A Lei Áurea, assinada pela Princesa Isabel em 13 de maio de 1888, aboliu a escravidão no Brasil.', 'aula'),
 ('Q-S21', 'Geografia', 'Qual é o maior país da América do Sul?', ['Argentina', 'Brasil', 'Peru', 'Colômbia'], 1, 'O Brasil ocupa quase metade da América do Sul.', 'treino'),
 ('Q-S22', 'Matemática', 'Quantos lados tem um hexágono?', ['5', '6', '7', '8'], 1, 'Hexa quer dizer seis. Os favos de mel são hexágonos.', 'aula'),
 ('Q-S23', 'Português', 'Qual destas palavras é proparoxítona?', ['Café', 'Lâmpada', 'Caju', 'Janela'], 1, 'Proparoxítona tem a sílaba forte na antepenúltima: lâm-pa-da. E toda proparoxítona leva acento.', 'aula'),
 ('Q-S24', 'Matemática', 'Quantos dias tem um ano bissexto?', ['364', '365', '366', '367'], 2, 'O ano bissexto tem 366 dias: fevereiro ganha o dia 29, de quatro em quatro anos.', 'treino'),
 ('Q-S25', 'Ciências', 'Qual é o maior animal do mundo?', ['Elefante-africano', 'Baleia-azul', 'Girafa', 'Tubarão-baleia'], 1, 'A baleia-azul pode passar de 30 metros. É o maior animal que já existiu.', 'aula'),
 ('Q-S26', 'História', 'Em que mês o Brasil comemora a Independência?', ['Abril', 'Setembro', 'Outubro', 'Novembro'], 1, 'Em 7 de setembro de 1822, às margens do riacho do Ipiranga, em São Paulo.', 'aula'),
 ('Q-S27', 'História', 'Em que país começou a tradição da árvore de Natal?', ['Itália', 'Alemanha', 'Portugal', 'Estados Unidos'], 1, 'O costume de enfeitar pinheiros no Natal vem da Alemanha e se espalhou pela Europa no século 19.', 'treino'),
]
def _b64(p):
    from PIL import Image; import io
    im = Image.open(p).convert('RGB'); im.thumbnail((1200, 1200)); bf = io.BytesIO(); im.save(bf, 'JPEG', quality=88)
    return 'data:image/jpeg;base64,' + base64.b64encode(bf.getvalue()).decode()
QE = WK / 'qedu'
TV = {'Geografia': _b64(QE / 'geo' / 'tv_q0_rev.png'), 'História': _b64(QE / 'hist' / 'tv_q0_rev.png'), 'Português': _b64(QE / 'port' / 'tv_q0_rev.png'),
      'Ciências': _b64(QE / 'geo' / 'tv_q1_rank.png'), 'Matemática': _b64(QE / 'port' / 'tv_q1_rank.png'), 'treino': _b64(QE / 'treino' / 'tv_q1_rev.png')}

def q_frames(i, row):
    sid, mat, q, opts, ok, exp, cta = row
    dt = DATAS[i]; cor = MAT[mat]; k = AVS[i % len(AVS)]; dark = i % 2 == 1
    bg = 'var(--mata)' if dark else 'var(--amarelo)'; ink = '#fff' if dark else 'var(--tinta)'
    tag = f'<span class="chip" style="background:{cor};color:#fff;border-color:{cor}">Quiz de {mat}</span>'
    fs = 84 if len(q) < 40 else 70
    grid = ''.join(Q.resp(j, o, 'height:140px;font-size:40px') for j, o in enumerate(opts))
    f1 = f'''<section class="page" style="width:1080px;height:1920px;background:{bg}">
      <div class="abs carta" style="left:70px;top:270px;width:940px;height:1120px;transform:rotate({-1.2 if i % 2 else 1.2}deg)">
        <div class="abs" style="left:50px;top:46px">{tag}</div>
        <div class="abs" style="right:40px;top:-60px;transform:rotate(8deg)">{Q.av(k, 200)}</div>
        <div class="abs t" style="left:50px;top:200px;width:840px;font-size:{fs}px">{q}</div>
        <div class="abs" style="left:50px;top:{600 if len(q) < 60 else 650}px;width:840px;display:grid;grid-template-columns:1fr 1fr;gap:24px">{grid}</div>
        <div class="abs" style="left:50px;top:990px;font-size:40px;font-weight:900">Responde de cabeça. A resposta está no próximo story →</div>
      </div>
      <div class="abs" style="left:80px;top:1480px">{Q.logo('neg' if dark else 'cor', 170)}</div></section>'''
    f2 = f'''<section class="page" style="width:1080px;height:1920px;background:{bg}">
      <div class="abs carta" style="left:70px;top:300px;width:940px;height:1060px;transform:rotate({1 if i % 2 else -1}deg)">
        <div class="abs" style="left:50px;top:46px">{tag}</div>
        <div class="abs mini" style="left:50px;top:170px;font-size:34px;color:var(--txt2)">{q}</div>
        <div class="abs" style="left:50px;top:{300 if len(q) < 45 else 350}px;width:840px">{Q.resp(ok, opts[ok], 'height:170px;font-size:60px', '<span style="margin-left:auto;font-size:64px">✓</span>')}</div>
        <div class="abs" style="left:50px;top:{560 if len(q) < 45 else 610}px;width:840px;font-size:46px;line-height:1.3;font-weight:700">{exp}</div>
        <div class="abs" style="right:40px;bottom:-70px;transform:rotate(-6deg)">{Q.av(k, 180)}</div>
      </div>
      <div class="abs" style="left:80px;top:1440px;width:920px;font-size:46px;font-weight:900;color:{ink}">Acertou? Manda pra quem ia errar.</div>
      <div class="abs" style="left:80px;top:1540px">{Q.logo('neg' if dark else 'cor', 170)}</div></section>'''
    if cta == 'aula':
        h3 = f'Professor(a): essa pergunta cabe na sua aula de {mat}.'
        b3 = 'Monte o quiz da matéria em minutos. A turma responde pelo celular, a resposta aparece no telão e o pódio sai na hora.'
    else:
        h3 = 'No treinamento da empresa, o conteúdo também vira quiz.'
        b3 = 'Escreva as perguntas do treinamento e a equipe responde pelo celular. Ranking e pódio no telão.'
    f3 = f'''<section class="page" style="width:1080px;height:1920px;background:var(--mata)">
      <div class="abs" style="left:80px;top:250px">{Q.logo('neg', 200)}</div>
      <div class="abs t" style="left:80px;top:380px;width:920px;font-size:82px;color:#fff">{h3}</div>
      <div class="abs" style="left:80px;top:{720 if len(h3) < 60 else 800}px;width:900px;font-size:44px;line-height:1.3;color:#fff;font-weight:600">{b3}</div>
      <div class="abs" style="left:180px;top:{930 if len(h3) < 60 else 980}px;width:720px">
        <div style="background:#111;border-radius:22px;padding:16px;box-shadow:0 30px 70px rgba(0,0,0,.45)"><img src="{TV['treino' if cta == 'treino' else mat]}" style="display:block;width:100%;border-radius:8px"></div>
        <div style="margin:0 auto;width:120px;height:34px;background:#111"></div><div style="margin:0 auto;width:300px;height:14px;border-radius:8px;background:#111"></div></div>
      <div class="abs" style="left:80px;top:1500px;width:920px;height:130px;border-radius:30px;background:var(--amarelo);color:var(--tinta);display:flex;align-items:center;justify-content:center;font-family:Fraunces,serif;font-weight:900;font-size:58px">Criar meu quiz grátis →</div>
      <div class="abs" style="left:80px;top:1660px;width:920px;text-align:center;font-size:36px;font-weight:800;color:#fff">quiddo.com.br · grátis até 10 pessoas</div></section>'''
    out = []
    for n, (body, ttl, note) in enumerate(((f1, f'Quiz de {mat}: {q}', 'Quadro 1 refeito com a matéria e o aviso "a resposta está no próximo story".'),
                                          (f2, f'Resposta: {opts[ok]}', 'Quadro 2: resposta e explicação curta.'),
                                          (f3, 'CTA ' + ('sala de aula' if cta == 'aula' else 'treinamento'), 'Quadro 3: CTA de ' + ('sala de aula' if cta == 'aula' else 'treinamento corporativo') + '. Oferta do site: grátis até 10 pessoas, sem baixar app.')), 1):
        pid = sid if n == 1 else f'{sid}-{n}'
        out.append(dict(id=pid, base=sid, brand='Quiddo', n=n, data=dt, sem=SEM[i], title=ttl, notes=note, html=C.doc(pid, Q.FONTS, Q.CSS, body, 1080, 1920)))
    return out

# ---------------- RETROZAP: (base, casa, ícone, texto quadro 2, troféu?)
RZ = [
 ('R-S7', 'grupo', 'eyes', 'A retrospectiva lê o grupo inteiro: quem fala mais, quem some e quem só manda kkkk.', None),
 ('R-S8', 'casal', 'speech-balloon', 'Na retrospectiva de casal, isso tem troféu.', 'Tagarela do Casal'),
 ('R-S9', 'grupo', 'face-with-tears-of-joy', 'Isso tem troféu na retrospectiva. Ela conta cada kkkk do ano.', 'Rei(nha) do Kkkk'),
 ('R-S21', 'casal', 'two-hearts', 'Na retrospectiva de casal, a conversa do ano vira 8 troféus e o placar um contra o outro.', None),
 ('R-S11', 'grupo', 'chart-with-upwards-trend', 'A retrospectiva mostra o ano do grupo em números: mensagens, áudios, risadas e figurinhas.', None),
 ('R-S12', 'grupo', 'spiral-calendar-pad', 'Como funciona: exporta a conversa do grupo, escolhe o arquivo no site e vê os troféus de cada um.', None),
 ('R-S13', 'grupo', 'paperclip', 'A retrospectiva mostra quem mais fala, quem some e quem só aparece pra mandar link.', None),
 ('R-S14', 'grupo', 'ghost', 'A retrospectiva mostra quem conversa todo dia e quem some por meses. Os troféus saem da conversa do ano.', None),
 ('R-S15', 'grupo', 'studio-microphone', 'Quem fala mais, quem manda mais áudio, quem mais ri: o grupo inteiro vira troféu.', None),
 ('R-S16', 'casal', 'heart-with-arrow', 'Na retrospectiva de casal, isso tem troféu.', 'Mais Romântico(a)'),
 ('R-S17', 'grupo', 'speech-balloon', 'Black Friday passa. O troféu de quem mais manda mensagem no ano fica.', 'O Tagarela'),
 ('R-S18', 'grupo', 'camera-with-flash', 'A retrospectiva junta o ano do grupo: mensagens, áudios, risadas e um troféu pra cada um.', None),
 ('R-S19', 'grupo', 'studio-microphone', 'O Tagarela, o Podcaster do Grupo, o Rei do Kkkk: quem leva no seu?', None),
 ('R-S22', 'grupo', 'party-popper', 'Antes do réveillon que não vai acontecer, a retrospectiva do grupo que aconteceu.', None),
 ('R-S23', 'grupo', 'house-with-garden', 'Grupo da família também tem troféu: quem fala mais, quem manda áudio, quem só manda figurinha.', None),
 ('R-S24', 'casal', 'slice-of-pizza', 'Na retrospectiva de casal, isso tem troféu.', 'Fominha'),
 ('R-S25', 'grupo', 'studio-microphone', 'Isso tem troféu na retrospectiva. Ela conta cada áudio do ano.', 'Podcaster do Grupo'),
 ('R-S26', 'grupo', 'clinking-beer-mugs', 'Nenhuma decisão, mas muita mensagem. A retrospectiva mostra quem mais fala no grupo.', None),
 ('R-S27', 'casal', 'black-sun-with-rays', 'Na retrospectiva de casal, isso tem troféu.', 'Despertador do Amor'),
 ('R-S28', 'grupo', 'speech-balloon', 'Quem mais manda mensagem leva este troféu. E tem mais 7.', 'O Tagarela'),
 ('R-S29', 'grupo', 'briefcase', 'Grupo do trabalho também tem retrospectiva: quem fala mais, quem some, quem só manda kkkk.', None),
]

def preco(i):
    return 'R$ 13,99' if i <= 13 else 'R$ 8,99 até 31/12'

def r_frames(i, row):
    sid, casa, ic, txt, trof = row
    casal = casa == 'casal'
    bg = 'var(--creme)' if casal else 'var(--noite)'; ink = 'var(--noite)' if casal else '#fff'; ac = 'var(--cereja)' if casal else 'var(--manga)'
    cls = 'casal' if casal else ''
    trofeu = (f'''<div class="abs" style="left:80px;top:{820 if len(txt) < 50 else 900}px;width:920px;background:{'#fff' if casal else 'var(--acai)'};border-radius:40px;padding:50px;display:flex;gap:40px;align-items:center;box-shadow:0 24px 60px rgba(0,0,0,.25)">
        {R.icon(ic, 200, casa)}<div><div class="mono" style="font-size:30px;opacity:.7;color:{ink}">TROFÉU</div><div class="t" style="font-size:80px;color:{ink}">{trof}</div></div></div>''' if trof else
              f'<div class="abs" style="left:80px;top:{820 if len(txt) < 70 else 900}px">{R.icon(ic, 260, casa)}</div>')
    f2 = f'''<section class="page {cls}" style="width:1080px;height:1920px;background:{bg}">
      <div class="abs t" style="left:80px;top:330px;width:920px;font-size:{92 if len(txt) < 70 else 80}px;color:{ink}">{txt}</div>
      {trofeu}
      <div class="abs" style="left:80px;top:1350px;width:920px;font-size:44px;font-weight:700;color:{ac}">{'Quem leva entre vocês dois?' if casal else 'Quem leva no seu grupo?'}</div>
      <div class="abs" style="left:80px;top:1440px">{R.assinatura(300, casa)}</div></section>'''
    if casal:
        h3, oferta, bt = 'A retrospectiva de vocês dois.', 'Pagamento único · sem assinatura', 'Fazer a de vocês'
        bl = ['8 troféus do casal e o placar um contra o outro', 'O vídeo de vocês e grupos ilimitados', 'Nada sai do seu celular']
    else:
        h3, oferta, bt = 'A retrospectiva do seu grupo do WhatsApp.', '1º grupo grátis · sem cadastro', 'Fazer a do meu grupo'
        bl = ['Um troféu pra cada um, feito da conversa do ano', 'Quem fala mais, quem some, quem manda áudio', 'Nada sai do seu celular']
    bul = ''.join(f'<div style="display:flex;gap:22px;align-items:center;margin-bottom:30px"><span style="flex:none;width:56px;height:56px;border-radius:50%;background:{ac};color:{"#fff" if casal else "var(--noite)"};display:grid;place-items:center;font-weight:900;font-size:32px">✓</span><span>{b}</span></div>' for b in bl)
    f3 = f'''<section class="page {cls}" style="width:1080px;height:1920px;background:{bg}">
      <div class="abs" style="left:80px;top:250px">{R.assinatura(340, casa)}</div>
      <div class="abs t" style="left:80px;top:420px;width:920px;font-size:110px;color:{ink}">{h3}</div>
      <div class="abs" style="left:80px;top:{820 if len(h3) < 35 else 940}px;width:920px;font-size:48px;font-weight:700;line-height:1.25;color:{ink}">{bul}</div>
      <div class="abs" style="left:80px;top:1360px;font-size:38px;font-weight:800;color:{ac};border:3px solid {ac};border-radius:16px;padding:12px 22px">{oferta}</div>
      <div class="abs" style="left:80px;top:1480px;width:920px;height:140px;border-radius:32px;background:{ac};color:{'#fff' if casal else 'var(--noite)'};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:60px">{bt} →</div>
      <div class="abs mono" style="left:80px;top:1650px;width:920px;text-align:center;font-size:40px;color:{ink}">retrozap.com.br</div></section>'''
    return [dict(id=f'{sid}-2', base=sid, brand='Retrozap', n=2, data=DATAS[i], sem=SEM[i], title=('Troféu: ' + trof) if trof else 'O gancho vira retrospectiva', notes='Quadro 2: a frase do quadro 1 vira produto' + (f' (troféu real do site: {trof}).' if trof else '.'), html=C.doc(sid + '-2', R.FONTS, R.CSS, f2, 1080, 1920)),
            dict(id=f'{sid}-3', base=sid, brand='Retrozap', n=3, data=DATAS[i], sem=SEM[i], title='CTA ' + ('casal' if casal else 'grupo'), notes='Quadro 3: CTA claro, sem preço (regra do Gui, rodada 13). ' + ('' if casal else '1º grupo grátis (site).'), html=C.doc(sid + '-3', R.FONTS, R.CSS, f3, 1080, 1920))]

# ---------------- SPORT DNA: (base, esporte, termo, na prática)
DN = [
 ('D-S7', 'racket', 'Balanço', 'Balanço mais na cabeça dá potência. Mais no cabo dá manobra e reação rápida na rede.'),
 ('D-S21', 'surf', 'Seu nível', 'O que você já faz na onda define a litragem e o tipo de prancha. Tempo de prancha não.'),
 ('D-S9', 'run', 'Pronação', 'É o quanto o pé gira para dentro ao apoiar. Muda o tipo de tênis: neutro ou com mais estabilidade.'),
 ('D-S10', 'racket', '16×19', 'Padrão mais aberto (16×19) dá mais spin e saída de bola. Mais fechado (18×20) dá mais controle.'),
 ('D-S11', 'surf', 'Quilhas', 'Triquilha é a mais versátil. Quadriquilha dá mais velocidade em onda aberta.'),
 ('D-S12', 'surf', 'Rocker', 'Mais rocker: curva mais fácil em onda cavada. Menos rocker: mais velocidade em onda fraca.'),
 ('D-S13', 'run', 'Drop', 'Drop alto combina com quem pisa com o calcanhar. Drop baixo, com quem apoia o meio do pé.'),
 ('D-S14', 'racket', 'Rigidez', 'Raquete mais rígida devolve mais potência, mas passa mais vibração para o braço.'),
 ('D-S15', 'surf', 'Borda', 'Borda mais fina corta a água na curva. Mais grossa dá estabilidade e flutuação.'),
 ('D-S16', 'racket', 'Cabo', 'Cabo do tamanho certo deixa o punho solto. Grosso demais trava; fino demais faz apertar.'),
 ('D-S17', 'run', 'Entressola', 'Entressola mais macia amortece no longão. Mais firme devolve energia no ritmo.'),
 ('D-S18', 'surf', 'Deck', 'Deck mais cheio põe volume embaixo do pé: a prancha boia mais e fica mais estável.'),
 ('D-S19', 'racket', 'Overgrip', 'Overgrip gasto escorrega e faz você apertar o cabo. Trocar é barato e muda a pegada.'),
 ('D-S22', 'run', 'Palmilha', 'Se a palmilha gastou antes do solado, troque só ela: o tênis ainda tem vida.'),
 ('D-S23', 'racket', 'Peso', 'Leve demais, a raquete treme no impacto. Pesada demais, o golpe atrasa. O teste calcula a faixa certa pra você.'),
 ('D-S24', 'surf', 'Litragem', 'O teste calcula a litragem pelo seu peso e pelo seu nível. No exemplo do site: 32 a 36 L para 70 kg, intermediário.'),
 ('D-S25', 'run', 'Solado', 'Asfalto pede borracha mais resistente. Trilha pede cravos, para segurar na terra.'),
 ('D-S26', 'racket', 'Corda', 'Corda que nunca é trocada perde tensão e endurece. Trocar a corda é o primeiro passo.'),
 ('D-S27', 'surf', 'Outline', 'Outline mais cheio para onda fraca. Mais fino para onda forte e curva fechada.'),
 ('D-S28', 'run', 'Stack', 'Mais stack: mais conforto no longão. Menos stack: mais estabilidade e sensação do chão.'),
 ('D-S29', 'surf', 'Rabeta', 'Rabeta mais larga solta a prancha em onda pequena. Mais fina segura em onda grande.'),
]
SPD = {'racket': dict(nome='RACKET', cor='#DDF247', lg='racketdna', h='A raquete certa para o seu jogo e o seu braço.', bl=['Avaliação grátis da raquete que você já usa', '183 raquetes medidas, cruzadas com você', 'Você vê a prévia antes de pagar'], of='Teste grátis · sem cadastro', bt='Fazer o teste grátis', url='sportdna.com.br/racket'),
       'surf': dict(nome='SURF', cor='#6CCFF6', lg='surfdna', h='A prancha certa para o seu surf e o seu mar.', bl=['Tipo, medidas e litragem certos para você', '13 tipos de prancha disputam o seu resultado', 'Você vê a prévia antes de decidir'], of='Prévia grátis · 3 minutos · sem cadastro', bt='Descobrir minha prancha', url='sportdna.com.br/surf'),
       'run': dict(nome='RUN', cor='#FF8A3D', lg='rundna', h='O tênis de corrida certo para o seu treino.', bl=['19 perguntas sobre seu corpo, sua corrida e seu objetivo', '212 tênis comparados com você', 'Você vê a prévia antes de decidir'], of='Grátis · 3 minutos · sem cadastro', bt='Descobrir meu tênis', url='sportdna.com.br/run')}

def d_frames(i, row):
    sid, sp, termo, prat = row; s = SPD[sp]; cor = s['cor']
    f2 = f'''<section class="page" style="width:1080px;height:1920px">
      <div class="abs lbl" style="left:80px;top:300px">NA PRÁTICA · {s['nome']}</div>
      <div class="abs" style="left:80px;top:360px;width:920px;height:6px;background:{cor}"></div>
      <div class="abs t" style="left:80px;top:440px;width:920px;font-size:130px;color:{cor}">{termo}</div>
      <div class="abs" style="left:80px;top:700px;width:900px;font-size:66px;line-height:1.22;font-family:Archivo;font-weight:800">{prat}</div>
      <div class="abs" style="left:80px;top:1340px;font-size:42px;color:var(--muted)">Qual é o certo pra você? O teste responde →</div>
      <div class="abs" style="left:80px;top:1430px">{D.logo(s['lg'] + '-logo-fundo-escuro', 460)}</div></section>'''
    bul = ''.join(f'<div style="display:flex;gap:22px;align-items:center;margin-bottom:30px"><span style="flex:none;width:56px;height:56px;border-radius:50%;background:{cor};color:#0A0A0A;display:grid;place-items:center;font-weight:900;font-size:32px">✓</span><span>{b}</span></div>' for b in s['bl'])
    f3 = f'''<section class="page" style="width:1080px;height:1920px">
      <div class="abs" style="left:80px;top:260px">{D.logo(s['lg'] + '-logo-fundo-escuro', 460)}</div>
      <div class="abs t" style="left:80px;top:420px;width:920px;font-size:100px">{s['h'].replace('o seu ', '<span style="color:' + cor + '">o seu ', 1) + '</span>' if 'o seu ' in s['h'] else s['h']}</div>
      <div class="abs" style="left:80px;top:900px;width:920px;font-size:46px;font-weight:700;line-height:1.25">{bul}</div>
      <div class="abs" style="left:80px;top:1360px;font-size:36px;font-weight:700;color:{cor};border:3px solid {cor}88;border-radius:16px;padding:12px 22px">{s['of']}</div>
      <div class="abs" style="left:80px;top:1480px;width:920px;height:140px;border-radius:32px;background:{cor};color:#0A0A0A;display:flex;align-items:center;justify-content:center;font-family:Archivo;font-weight:800;font-size:58px">{s['bt']} →</div>
      <div class="abs m" style="left:80px;top:1650px;width:920px;text-align:center;font-size:40px">{s['url']}</div></section>'''
    return [dict(id=f'{sid}-2', base=sid, brand='SPORT DNA', n=2, data=DATAS[i], sem=SEM[i], title=f'Na prática: {termo}', notes='Quadro 2: o termo do quadro 1 vira decisão de compra. Orientação geral, sem marca, sem promessa médica.', html=C.doc(sid + '-2', D.FONTS, D.CSS, f2, 1080, 1920)),
            dict(id=f'{sid}-3', base=sid, brand='SPORT DNA', n=3, data=DATAS[i], sem=SEM[i], title=f'CTA {s["nome"]}', notes='Quadro 3: CTA claro com oferta do site.', html=C.doc(sid + '-3', D.FONTS, D.CSS, f3, 1080, 1920))]

FR = []
for i in range(21):
    FR += q_frames(i, QZ[i]) + r_frames(i, RZ[i]) + d_frames(i, DN[i])

from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for f in FR:
            h = OUT / f"{f['id']}.html"; h.write_text(f['html'])
            await pg.goto(h.as_uri()); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(150)
            await pg.locator('.page').first.screenshot(path=str(OUT / f"{f['id']}.png"))
        await b.close()
asyncio.run(main())
json.dump([{k: v for k, v in f.items() if k != 'html'} for f in FR], open(OUT / 'meta.json', 'w'), ensure_ascii=False, indent=1)
print(len(FR), 'quadros')
