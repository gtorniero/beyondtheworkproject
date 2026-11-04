# Beyond the Work · Social

Branch só de conteúdo social (não é o site). Nenhum commit daqui deve disparar build do site: toda mensagem de commit leva `[CF-Pages-Skip]`.

## Pastas

- `packs/SNN/`: o que o DOT (agente do ChatGPT) usa para agendar.
  - `STATUS.json`: o que está liberado. O DOT só agenda `"liberado": true`, na versão indicada.
  - `GUIA-PUBLICACAO-DOT.md` e `agenda.csv`: data, hora, conta, links diretos (raw) de cada arquivo.
  - `<marca>/reels|carrosseis|stories/`: mídia final (PNG 1080×1350 e 1080×1920, MP4 H.264 30 fps).
  - `<marca>/LEGENDAS.txt` e `<marca>/editaveis/` (HTML com fontes e SVGs embutidos).
- `pipeline/`: o código que gera as peças, a Mesa de Aprovação e os pacotes.
  - Fontes, SVGs oficiais e a arte do Quiddo já exportada do site estão em `pipeline/assets` e `pipeline/fonts`.
  - `pipeline/state`: versões e manifestos do último render; copie para `pipeline/out/` antes de renderizar.
  - Regras de marca, ritmo e trends: `pipeline/playbook-crescimento.md`. Prompt do DOT: `pipeline/prompt-agente-dot-social.md`.

Links diretos: `https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/social/packs/S01/...`

## Ciclo semanal

| Quando (Brasília) | O quê | Quem |
|---|---|---|
| Sexta 10h | trends da semana em "05. Social Content › Entrada do DOT" | DOT |
| Sábado | produz o pack da semana seguinte e publica na Mesa de Aprovação | Claude (tarefa agendada) |
| Domingo 10h | lembrete para aprovar | Claude (tarefa agendada) |
| Domingo | aprova na Mesa | Gui |
| Domingo 21h e diário 21h | lê a Mesa, gera STATUS.json e publica aqui o que foi aprovado | Claude (tarefa agendada) |
| Segunda 8h e diário | agenda no Meta Business Suite só o que está liberado e ainda não foi agendado | DOT |

Mesa de Aprovação: https://claude.ai/artifact/KAwUuKVHZgYknpdquaTkwd
