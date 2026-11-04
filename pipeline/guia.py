"""Gera o guia de publicação para o DOT (ChatGPT) e a agenda do pack, a partir do manifesto."""
import csv, io

DATAS = {1: '09/11/2026 (seg)', 2: '10/11/2026 (ter)', 3: '11/11/2026 (qua)', 4: '12/11/2026 (qui)',
         5: '13/11/2026 (sex)', 6: '14/11/2026 (sáb)', 7: '15/11/2026 (dom)'}
RAW = 'https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/social/packs/S01'
SLUG = {'Quiddo': 'quiddo', 'Retrozap': 'retrozap', 'SPORT DNA': 'sportdna'}
SUB = {'reel': 'reels', 'carrossel': 'carrosseis', 'story': 'stories'}
ZIP = {'Quiddo': 'quiddo.zip', 'Retrozap': 'retrozap.zip', 'SPORT DNA': 'sportdna.zip'}

def como(p):
    if p['fmt'] == 'reel': return 'Business Suite · reel'
    if p['fmt'] == 'carrossel': return 'Business Suite · post'
    return 'Lembrete ao Gui (app)' if p.get('sticker') and 'Sem adesivo' not in p['sticker'] else 'Business Suite · story'

def hora(p):
    return p.get('slot') or ('12h' if p['fmt'] == 'story' else '12h30')

def arquivos(p):
    return ', '.join(p['media'])

def links(p):
    return ' '.join(f"{RAW}/{SLUG[p['brand']]}/{SUB[p['fmt']]}/{f}" for f in p['media'])

def linhas(P):
    order = {'reel': 0, 'carrossel': 1, 'story': 2}
    return sorted(P, key=lambda p: (p['day'], hora(p).zfill(3), p['brand'], order[p['fmt']]))

def agenda_csv(P):
    b = io.StringIO(); w = csv.writer(b)
    w.writerow(['data', 'hora', 'marca', 'formato', 'peca', 'versao', 'como', 'arquivos', 'links', 'adesivo', 'titulo'])
    for p in linhas(P):
        w.writerow([DATAS[p['day']], hora(p), p['brand'], p['fmt'], p['id'], p['version'], como(p), arquivos(p), links(p), p.get('sticker', ''), p['title']])
    return b.getvalue()

PROMPT = """DOT, agende o Pack Semanal 01 (Quiddo, Retrozap e SPORT DNA, semana de 09 a 15/11/2026) seguindo o guia do pack.
Mídia, legendas e agenda: GitHub, branch social, pasta packs/S01 (links diretos no agenda.csv). Só agende o que o STATUS.json marca como liberado.
Antes de cada peça, cheque duplicidade no Registro de publicações, no Planejador e na grade do perfil. Depois, registre.
Tudo vai agendado no Meta Business Suite, inclusive os stories (o CTA já está na arte). Não edite nada. Se der erro, pare e me mande print."""

def guia_md(P, pack='S01'):
    rows = '\n'.join(f"| {DATAS[p['day']]} | {hora(p)} | {p['brand']} | {p['fmt']} | {p['id']} ({p['version'].split('-')[-1]}) | {como(p)} |" for p in linhas(P))
    stickers = '\n'.join(f"- **{p['id']}** ({p['brand']}, {DATAS[p['day']]}): {p['sticker']}" for p in linhas(P) if p['fmt'] == 'story' and p.get('sticker'))
    return f"""# Guia de publicação · Pack Semanal 01

Para o DOT (ChatGPT, modo agente) agendar as peças aprovadas na Mesa de Aprovação. Semana de 09 a 15/11/2026.

## Onde está tudo

- **Mídia e legendas:** no GitHub, pasta pública `packs/S01` do branch `social` (`{RAW}/<marca>/...`). Cada linha do `agenda.csv` traz os links diretos dos arquivos. `LEGENDAS.txt` de cada marca: `{RAW}/<marca>/LEGENDAS.txt`.
- **Liberação:** o arquivo `{RAW}/STATUS.json` diz quais peças estão aprovadas (`"liberado": true`). Só agende peça liberada, na versão indicada ali.
- **Controle do que já foi feito:** planilha "Registro de publicações" na pasta "Entrada do DOT" do Drive.

## Regras

- Publicar só peças com `"liberado": true` no STATUS.json, na versão indicada.
- **Antes de cada peça, checar duplicidade, nesta ordem:**
  1. o Registro de publicações (mesma peça e versão já marcada "agendado" ou "publicado");
  2. o Planejador do Business Suite (mesma data, hora e conta, ou mesma primeira linha de legenda);
  3. a grade do perfil (mesma primeira linha de legenda).
  Se achar, não agende de novo; marque "já existia" no Registro.
- Logo depois de agendar, preencher o Registro: peça, versão, conta, data/hora, status "agendado" e link.
- Uma marca por conta. Conferir a conta do Instagram antes de cada agendamento.
- Não editar arte, legenda, logo, bio, foto de perfil nem destaques. Legenda exatamente como no `LEGENDAS.txt`.
- Se algo falhar (login, upload, capa, horário, conta), parar e avisar o Gui com um print.
- O Gui não posta nada: tudo vai agendado.

## Como agendar cada formato no Meta Business Suite

Entrar em business.facebook.com, abrir **Planejador** e escolher a conta da marca.

**Carrossel (feed).** Criar post → só a conta do Instagram da marca → adicionar as imagens na ordem do nome (`-1`, `-2`, `-3`…) → colar a legenda da peça → Agendar → data e hora da agenda.

**Reel.** Criar reel → conta da marca → enviar o MP4 → em capa ou miniatura, enviar o PNG `-capa` da mesma peça → colar a legenda → manter "compartilhar no feed" ligado → Agendar.
Os MP4 saem sem música. Se o Business Suite mostrar uma biblioteca de músicas para o reel, escolher uma música animada em alta. Se não mostrar, perguntar ao Gui antes: ele decide entre agendar sem música ou postar pelo app com música.

**Story.** Criar story → conta da marca → PNG → Agendar. Nenhum story usa adesivo do Instagram: o CTA ("responde no direct", "link na bio") já está desenhado na arte. O Gui não posta nada; tudo é agendado.

## Agenda

| Data | Hora | Marca | Formato | Peça | Como |
|---|---|---|---|---|---|
{rows}

## Prompt para colar no DOT

```
{PROMPT}
```
"""
