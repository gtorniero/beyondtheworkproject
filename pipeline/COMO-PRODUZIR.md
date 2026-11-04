# Runbook do Claude (sessões agendadas)

Use este runbook quando uma tarefa agendada pedir para liberar, ajustar ou produzir um pack. Tudo roda numa sessão nova, sem memória da conversa original.

## Peças fixas
- **Mesa de Aprovação:** https://claude.ai/artifact/KAwUuKVHZgYknpdquaTkwd
  - Banco `reviews/<id>`: no S01 a chave é o id da peça; do S02 em diante, `<SNN>_<id>`.
  - Banco `pack/<SNN>`: feedback geral, `ultimaRodada`, `enviadaEm`.
  - Banco `rodadas/R<n>`: foto de cada rodada finalizada, com o campo `resumo`.
  - Leia e escreva com a ferramenta ArtifactData.
- **Repositório:** gtorniero/beyondtheworkproject, branch `social` (nunca o `main`, que é o site).
  - Peça acesso de push com add_repo e clone só esse branch: `git clone --depth 1 -b social https://github.com/gtorniero/beyondtheworkproject btw-social`.
  - Todo commit leva `[CF-Pages-Skip]` na mensagem e termina com as linhas de atribuição da sessão.
- **Drive "05. Social Content"** (id 1y4dovKtUNSnNvcflf5d3cLItGrH8ajOm):
  - "Entrada do DOT" (id 1CF-8gBdSVkyIgd3fVP-wcL6AsisXXoPD): trends, métricas e a planilha "Registro de publicações".
  - Playbook de crescimento.
- **Regras de marca, ritmo e horários:** `pipeline/playbook-crescimento.md` e os docs de identidade de cada marca no Drive. Nunca redesenhe logo, mascote ou ícone: use só `pipeline/assets`.

## Preparar o ambiente
```bash
cd btw-social/pipeline
pip install --break-system-packages -q brotli markdown
mkdir -p out && cp state/*.json out/
# Playwright e ffmpeg já vêm instalados. As fontes estão em fonts/. A arte do Quiddo está em assets/quiddo/art.json.
```

## A. Liberar o que foi aprovado (tarefa diária)
1. ArtifactData `list` em `reviews`, com `out_dir` = uma pasta nova (ex.: `db/reviews`).
2. Para cada pack em `packs/` que ainda não está todo liberado:
   ```bash
   python3 pipeline/status.py db/reviews packs/SNN/STATUS.json packs/SNN/manifest.json
   ```
3. Se o STATUS.json mudou, faça commit e push. Notifique o Gui só se algo novo foi liberado ("X peças liberadas para o DOT").

## B. Aplicar uma rodada finalizada
1. Leia `pack/<SNN>`. Se `ultimaRodada` for maior que a última rodada que você já processou (veja `pipeline/state/rodadas-processadas.json`), leia `rodadas/R<n>`.
2. Para cada peça "reprovado" ou com comentário novo:
   - ajuste o código da peça em `pipeline/<marca>.py`;
   - renderize: `python3 render.py --part=x <ids>`;
   - monte: `python3 make_tool.py`;
   - republique a Mesa no mesmo URL (Artifact `read` antes, depois `publish` com `url` e `root=pipeline/tool`).
3. Acrescente a explicação da mudança em `MUDOU` no make_tool.py.
4. Atualize `packs/SNN/` com `pipeline/entrega/*`, `pipeline/state/` com `out/versions-*.json` e `out/manifest*.json`, e `rodadas-processadas.json`. Commit e push.
5. Notifique: "Rodada n aplicada: N peças novas na Mesa".

## Regra de backlog (decisão do Gui, 04/11)
- Sempre que o Gui terminar de aprovar um pack (nenhuma peça "sem decisão" ou "revisar" na Mesa, ou rodada finalizada com quase tudo aprovado), produza logo o próximo. O objetivo é ter sempre um pack aprovado à frente da semana em curso.
- Limite: no máximo 2 packs à frente da semana atual. Se já houver 2, não produza.
- Peças sem decisão do pack anterior entram no pack novo como candidatas (mesma arte, data nova), porque a Mesa mostra só o pack mais recente.

## Não repetir e manter o feed harmônico (vale para toda produção)
- Antes de criar, leia:
  - todos os `packs/*/manifest.json` (títulos, legendas, formatos, temas);
  - o "Registro de publicações" no Drive (o que foi de fato agendado ou publicado);
  - as métricas mais recentes.
- Não repita tema, gancho, piada, pergunta ou dado de peça das últimas 4 semanas da mesma marca. Formato pode repetir; ideia não.
- Monte a grade de cada marca com as 9 últimas peças de feed (as já publicadas e as do pack anterior) mais as novas, na ordem real de publicação, e olhe a imagem:
  - alterne fundo claro e escuro;
  - não ponha duas capas de mesma cor ou mesma composição lado a lado;
  - mantenha a identidade de cada marca.
- Faça essa checagem com uma folha de contato gerada pelo `preview.py` e corrija antes de publicar na Mesa.

## C. Produzir o próximo pack (gatilho de backlog ou sábado)
1. Leia o doc de trends mais recente em "Entrada do DOT", as métricas da semana, o Playbook e faça a checagem de repetição e harmonia acima.
2. Crie o pack S(NN+1), com a semana de segunda a domingo seguinte:
   - por marca, 1 post de feed por dia alternando reel e carrossel, continuando a sequência da semana anterior;
   - de 1 a 3 stories por dia, sem adesivo do Instagram (CTA desenhado na arte com `C.apply_ctas`);
   - reels misturando meme e trend; Quiddo com no mínimo 2 memes;
   - toda peça com um motivo para ser enviada e um CTA de envio na legenda.
3. Em `common.py`, mude `PACK` e `DIAS`. Escreva as peças em `pipeline/<marca>.py`, seguindo o padrão do S01 (funções por peça, `piece(...)` com id, fmt, day, slot, título, legenda e notas).
4. Use só dado verdadeiro:
   - Quiddo: CTA "Faça o seu. Teste grátis.", nunca "até 10 pessoas".
   - Retrozap: dados de exemplo só "Turma do Churras" e "Dani & Cris", com etiqueta.
   - SPORT DNA: números conferidos no site (repo gtorniero/sportdna).
5. Pré-visualize com `preview.py`, corrija sobreposições e renderize tudo (em 2 partes paralelas).
6. Rode `make_tool.py` e republique a Mesa. A Mesa mostra o pack novo; as decisões do S01 continuam no banco.
7. Copie `pipeline/entrega/*` para `packs/S(NN+1)/`, com `STATUS.json` todo `false` e o `manifest.json`. Atualize `pipeline/state`. Commit e push.
8. Notifique: "Pack S(NN+1) na Mesa. Aprove até domingo 21h."
