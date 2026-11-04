# Guia de publicação · Pack Semanal 01

Para o DOT (ChatGPT, modo agente) agendar as peças aprovadas na Mesa de Aprovação. Semana de 09 a 15/11/2026.

## Onde está tudo

- **Mídia e legendas:** no GitHub, pasta pública `packs/S01` do branch `social` (`https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/social/packs/S01/<marca>/...`). Cada linha do `agenda.csv` traz os links diretos dos arquivos. `LEGENDAS.txt` de cada marca: `https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/social/packs/S01/<marca>/LEGENDAS.txt`.
- **Liberação:** o arquivo `https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/social/packs/S01/STATUS.json` diz quais peças estão aprovadas (`"liberado": true`). Só agende peça liberada, na versão indicada ali.
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
| 09/11/2026 (seg) | 19h45 | Quiddo | reel | Q-R1 (v2) | Business Suite · reel |
| 09/11/2026 (seg) | 19h45 | Retrozap | reel | R-R1 (v1) | Business Suite · reel |
| 09/11/2026 (seg) | 19h45 | SPORT DNA | reel | D-R1 (v2) | Business Suite · reel |
| 10/11/2026 (ter) | 12h30 | Quiddo | carrossel | Q-C1 (v2) | Business Suite · post |
| 10/11/2026 (ter) | 12h30 | Retrozap | carrossel | R-C1 (v1) | Business Suite · post |
| 10/11/2026 (ter) | 12h30 | SPORT DNA | carrossel | D-C1 (v1) | Business Suite · post |
| 12/11/2026 (qui) | 19h45 | Quiddo | reel | Q-R2 (v2) | Business Suite · reel |
| 12/11/2026 (qui) | 19h45 | Retrozap | reel | R-R2 (v1) | Business Suite · reel |
| 12/11/2026 (qui) | 19h45 | SPORT DNA | reel | D-R2 (v1) | Business Suite · reel |
| 13/11/2026 (sex) | 12h | Quiddo | story | Q-S4 (v1) | Business Suite · story |
| 13/11/2026 (sex) | 12h | Retrozap | story | R-S4 (v1) | Business Suite · story |
| 13/11/2026 (sex) | 12h30 | Quiddo | carrossel | Q-C2 (v2) | Business Suite · post |
| 13/11/2026 (sex) | 12h30 | Retrozap | carrossel | R-C2 (v1) | Business Suite · post |
| 13/11/2026 (sex) | 12h30 | SPORT DNA | carrossel | D-C2 (v1) | Business Suite · post |
| 14/11/2026 (sáb) | 19h45 | Quiddo | reel | Q-R4 (v1) | Business Suite · reel |
| 15/11/2026 (dom) | 19h45 | Quiddo | reel | Q-R3 (v2) | Business Suite · reel |
| 15/11/2026 (dom) | 19h45 | Retrozap | reel | R-R3 (v1) | Business Suite · reel |
| 15/11/2026 (dom) | 19h45 | SPORT DNA | reel | D-R3 (v1) | Business Suite · reel |

## Prompt para colar no DOT

```
DOT, agende o Pack Semanal 01 (Quiddo, Retrozap e SPORT DNA, semana de 09 a 15/11/2026) seguindo o guia do pack.
Mídia, legendas e agenda: GitHub, branch social, pasta packs/S01 (links diretos no agenda.csv). Só agende o que o STATUS.json marca como liberado.
Antes de cada peça, cheque duplicidade no Registro de publicações, no Planejador e na grade do perfil. Depois, registre.
Tudo vai agendado no Meta Business Suite, inclusive os stories (o CTA já está na arte). Não edite nada. Se der erro, pare e me mande print.
```
