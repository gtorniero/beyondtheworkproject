# Runbook do Claude (sessões agendadas)

Use este runbook quando uma tarefa agendada pedir para liberar, ajustar ou produzir um pack. Tudo roda numa sessão nova, sem memória da conversa original.

## Peças fixas
- **Mesa de Aprovação:** https://claude.ai/artifact/KAwUuKVHZgYknpdquaTkwd
  - Banco `reviews/<id>`: no S01 a chave é o id da peça; do S02 em diante, `<SNN>_<id>`.
  - Banco `pack/<SNN>`: feedback geral, `ultimaRodada`, `enviadaEm`.
  - Banco `rodadas/<SNN>_R<n>` (do S02 rodada 3 em diante; antes era `rodadas/R<n>`, e o R2 do S02 sobrescreveu o R2 do S01): foto de cada rodada finalizada, com o campo `resumo`.
  - Ao finalizar a rodada, a Mesa limpa `pack/<SNN>.geral` e guarda o texto em `pack/<SNN>.geralHist` (aparece no painel Aprovados). Não reaplique feedback geral que já está no histórico.
  - Banco `ads/<SNN>_<id>` (desde 06/11): aprovação dos **Assets para ADs** (mídia paga), separada da orgânica. Nunca copie uma decisão de `reviews` para `ads`, nem o contrário: peça orgânica aprovada não é AD aprovado. O `status.py` e o DOT leem só `reviews`; AD aprovado não vai para o STATUS.json.
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
4. **ADs aprovados (regra do Gui, 10/11):** leia também o banco `ads` da Mesa. Para cada AD com `status: "aprovado"` na versão atual (a de `pipeline/ads/S02.json`) que ainda não tem pasta em `ads/aprovados/<marca>/<ID>-v<n>/`:
   - jeito rápido: ArtifactData `list` em `ads` com `out_dir=db` e `python3 pipeline/ads/exporta.py db/ads <pasta com media/ da Mesa>` (exporta todos os aprovados que faltam e refaz o INDEX.md; para estáticos e reels antigos, baixe antes a mídia da Mesa com Artifact `read` + `paths`);
   - ou, um a um: baixe a mídia da Mesa (Artifact `read` com `paths`) e rode `python3 pipeline/ads/placements.py <pasta baixada> ads/aprovados <IDs>`;
   - o script gera todos os posicionamentos da Meta (reel: 9:16 original e sem trilha, 4:5, 1:1, 16:9 in-stream e capas; estático: 4:5 hero, 1:1, 9:16, 1,91:1 e vídeos 4:5, 1:1, 9:16) com nomes por posicionamento e um LEIA-ME.md; reel novo precisa de entrada em `REEL` no script (fundo, frase do CTA, URL, logo);
   - confira um quadro de cada formato, atualize `ads/aprovados/INDEX.md` e o doc "ADs aprovados" no Drive (pasta "05. Social Content"), commit e push;
   - nunca suba nada para a conta de anúncios.

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
- Faça essa checagem com `python3 grade.py out/grade.jpg` (feed do pack anterior + o novo, por marca) e com o `preview.py` peça a peça; corrija antes de publicar na Mesa.

## C. Produzir o próximo pack (gatilho de backlog ou sábado)
1. Leia o doc de trends mais recente em "Entrada do DOT", as métricas da semana, o Playbook e faça a checagem de repetição e harmonia acima.
2. Crie o pack S(NN+1), com a semana de segunda a domingo seguinte:
   - por marca, 1 post de feed por dia alternando reel e carrossel, continuando a sequência da semana anterior;
   - de 1 a 3 stories por dia, sem adesivo do Instagram (CTA desenhado na arte com `C.apply_ctas`);
   - reels misturando meme e trend; Quiddo com no mínimo 2 memes;
   - toda peça com um motivo para ser enviada e um CTA de envio na legenda.
3. Mova o código do pack anterior para `pipeline/arquivo/SNN/` e o estado para `pipeline/state/SNN/`. Em `common.py`, mude `PACK`, `NUM`, `SEMANA`, `SEMANA_LONGA`, `PREV`, `DIAS` e `DATAS` (guia e Mesa leem daí). Escreva as peças em `pipeline/<marca>.py`, seguindo o padrão do S01 (funções por peça, `piece(...)` com id, fmt, day, slot, título, legenda e notas).
4. Use só dado verdadeiro:
   - Quiddo: CTA "Faça o seu. Teste grátis.", nunca "até 10 pessoas".
   - Retrozap: dados de exemplo só "Turma do Churras" e "Dani & Cris", com etiqueta.
   - SPORT DNA: números conferidos no site (repo gtorniero/sportdna).
5. Pré-visualize com `preview.py`, corrija sobreposições e renderize tudo (em 2 partes paralelas).
6. Rode `make_tool.py` e republique a Mesa. A Mesa mostra o pack novo; as decisões do S01 continuam no banco.
7. Copie `pipeline/entrega/*` para `packs/S(NN+1)/`, com `STATUS.json` todo `false` e o `manifest.json`. Atualize `pipeline/state`. Commit e push.
8. Notifique: "Pack S(NN+1) na Mesa. Aprove até domingo 21h."

## D. Assets para ADs (mídia paga)
- A Mesa tem dois tipos no topo: "Assets de conteúdo" (orgânico: identificação, utilidade, engajamento) e "Assets para ADs" (mídia paga: oferta clara, texto direto, CTA explícito, destino coerente). O filtro de marca vale nos dois.
- Os ADs ficam em `pipeline/ads/<SNN>.json` (um objeto por AD; campos no topo do bloco ADs do `make_tool.py`). Cada card mostra objetivo, formato, versão, copy, CTA e URL final; campo vazio aparece como "falta definir".
- Só crie AD com objetivo, oferta e URL final definidos pelo Gui. Pode reaproveitar a mídia de uma peça orgânica (campo `origem`), sem duplicar o render.
- Aprovar AD na Mesa não autoriza nada fora dela: nenhum upload em conta de anúncios, campanha, ativação, impulsionamento ou gasto sem ordem explícita e específica do Gui.
