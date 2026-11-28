"""Gera o guia de publicação para o DOT (ChatGPT) e a agenda do pack, a partir do manifesto."""
import csv, io
import common as C

DATAS = C.DATAS
RAW = f'https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/social/packs/{C.PACK}'
SLUG = {'Quiddo': 'quiddo', 'Retrozap': 'retrozap', 'SPORT DNA': 'sportdna'}
SUB = {'reel': 'reels', 'carrossel': 'carrosseis', 'story': 'stories'}
ZIP = {'Quiddo': 'quiddo.zip', 'Retrozap': 'retrozap.zip', 'SPORT DNA': 'sportdna.zip'}

def como(p):
    return {'reel': 'Instagram · reel', 'carrossel': 'Instagram · carrossel', 'story': 'Instagram · story (sequência)'}[p['fmt']]

def hora(p):
    return p.get('slot') or ('12h' if p['fmt'] == 'story' else '12h30')

def arquivos(p):
    return ', '.join(p['media'])

def links(p):
    return ' '.join(f"{RAW}/{SLUG[p['brand']]}/{SUB[p['fmt']]}/{f}" for f in p['media'])

def linhas(P):
    order = {'reel': 0, 'carrossel': 1, 'story': 2}
    return sorted(P, key=lambda p: (p['day'], hora(p).zfill(3), p['brand'], order[p['fmt']]))

def quadros(p):
    """Story em sequência (S05+): cada quadro vira uma linha "<PECA>.<n>" (formato lido pelo postar.py, como na STORIES-SEQ)."""
    n = p.get('frames') or 0
    if p['fmt'] != 'story' or n < 2: return [(p['id'], p['version'], p['media'], 0, '')]
    base = p['version'].rsplit('-v', 1)
    return [(f"{p['id']}.{k}", f"{base[0].replace(p['id'], p['id'] + '.' + str(k))}-v{base[1]}", [p['media'][k - 1]], k, f"{p['id']}.{k - 1}" if k > 1 else '') for k in range(1, n + 1)]

def audio(p):
    if p['fmt'] != 'reel': return ''
    return 'Música de banco (Mixkit) já no vídeo, sem narração; entrada e saída suaves.' if p.get('music') else 'Sem áudio.'

def agenda_csv(P):
    b = io.StringIO(); w = csv.writer(b, lineterminator='\n')
    w.writerow(['data', 'hora', 'marca', 'formato', 'peca', 'versao', 'onde', 'arquivos', 'links', 'audio', 'titulo', 'como', 'serie', 'observacao', 'quadro', 'anterior'])
    for p in linhas(P):
        for peca, ver, media, q, ant in quadros(p):
            m = list(media) + ([f"{p['id']}-capa.png"] if p['fmt'] == 'reel' else [])
            obs = 'candidata do S03 (sem decisão); FIXAR no perfil' if p['id'] == 'D-FX1' else ('sequência de 3, mesmo horário' if q else '')
            w.writerow([DATAS[p['day']], hora(p), p['brand'], p['fmt'], peca, ver, como(p), ', '.join(m),
                        ' '.join(f"{RAW}/{SLUG[p['brand']]}/{SUB[p['fmt']]}/{f}" for f in m), audio(p), p['title'], 'postar.py', '', obs, q or '', ant])
    return b.getvalue()

PROMPT = f"""Growth, publique o Pack Semanal {C.NUM} (Quiddo, Retrozap e SPORT DNA, {C.SEMANA_LONGA}) com o postar.py, lendo packs/{C.PACK}/agenda.csv, STATUS.json e LEGENDAS.txt do branch social.
Só sai o que o STATUS.json marca como liberado, na versão exata. Antes de cada peça, rode as travas de duplicidade do CONTINUIDADE.md. Stories saem em sequência (quadro 1, 2 e 3 no mesmo horário)."""

def guia_md(P, pack=C.PACK):
    rows = '\n'.join(f"| {DATAS[p['day']]} | {hora(p)} | {p['brand']} | {p['fmt']} | {p['id']} ({p['version'].split('-')[-1]}) | {p['title']} |" for p in linhas(P))
    return f"""# Guia de publicação · Pack Semanal {C.NUM}

Semana de {C.SEMANA_LONGA} (grade de dezembro: carrossel ter, qui, sáb e seg às 12h30; reel qua, sex e dom às 19h45; stories todo dia às 12h).
Quem publica: o Growth, com `growth/postagem/postar.py` (regra do Gui, 22/11). O DOT não recebe mais nada.

## Onde está tudo

- Mídia, `agenda.csv`, `STATUS.json`, `manifest.json` e `LEGENDAS.txt` de cada marca: `packs/{C.PACK}` do branch `social` ({RAW}).
- Só sai peça com `"liberado": true` no STATUS.json, na versão indicada (a Mesa libera peça a peça).
- Reels: MP4 1080×1920 com música de banco (Mixkit) já no arquivo, sem narração; capa `-capa.png` (arte 4:5 no centro).
- Stories: cada um é uma sequência de 3 quadros (`<PECA>.1`, `.2`, `.3`), no mesmo horário, sem adesivo (o CTA está na arte).
- D-FX1 v2 é candidata do S03 (sem decisão): só sai se o Gui aprovar, e é para FIXAR no perfil.

## Regras

- Travas de duplicidade do `CONTINUIDADE.md` antes de cada peça; registro com link e status depois.
- Legenda exatamente como no `LEGENDAS.txt`. Não editar arte, legenda, bio nem destaques.
- Nada de anúncio, impulsionamento ou gasto.

## Agenda

| Data | Hora | Marca | Formato | Peça | Título |
|---|---|---|---|---|---|
{rows}
"""
