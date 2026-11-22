# BTW_Conteúdo · continuidade

Regras permanentes do Gui. Valem para todas as sessões do Claude (Estúdio e Growth) e para o Codex. Registradas em 22/11/2026.

## Divisão permanente (Gui, 22/11/2026)

- **Orgânico é só do Claude, pelo script.** Isso vale para Retrozap, Quiddo e SPORT DNA, no Instagram e no Facebook: posts, reels, carrosséis e stories.
  - O Estúdio produz as peças e as leva à Mesa.
  - O Growth publica com `growth/postagem/postar.py` (branch `claude/sweet-hypatia-43ca1s`), lendo `packs/*/agenda.csv` e `STATUS.json` deste branch.
- **O Codex fica só com anúncios**, sempre sujeitos às autorizações do Gui. Ele não agenda, não publica e não edita orgânico, inclusive no Business Suite.
- **O DOT (agente do ChatGPT) não recebe mais nada** desde 22/11. Os arquivos `GUIA-PUBLICACAO-DOT.md` dos packs antigos ficaram só como histórico.
- **Nenhum agente cria, ativa ou impulsiona anúncio, nem gasta dinheiro**, sem autorização específica do Gui.

## Antes de cada publicação (travas de duplicidade)

1. Conciliar quatro fontes:
   - o registro de publicados (`growth/postagem/publicados.json`);
   - as tentativas sem confirmação;
   - a fila já existente no Meta;
   - o perfil real.
2. Conferir na agenda: código e pack, versão aprovada na Mesa (`liberado: true` e `status_mesa` aprovado), legenda e arte.
3. Não publicar peça repetida, nem com código diferente: mesma mídia, mesma arte ou mesma legenda contam como repetição.
4. Se houver tentativa incerta, reconciliar antes de reenviar.
5. Manter o registro com link e status de cada peça: publicado, removido, falhou.
6. Não excluir nenhum post publicado sem autorização específica do Gui.

## Datas e temas

- **Natal só a partir de 01/12**, na arte, na legenda, no título, no adesivo e nas hashtags.
  - O campo `nao_antes` (AAAA-MM-DD) no `STATUS.json` segura a peça até essa data. O `postar.py` respeita esse campo.
- **Q-C6 (Quiddo, "Natal em 1 mês")** saiu em 22/11 às 12h30 e foi excluído com a confirmação do Gui.
  - Status: `removido`, liberado=false, nao_antes 2026-12-01.
  - Não republicar.
- **Bloqueados até 01/12 por Natal:**
  - F-QD-6 ("Esse Natal vai ter pódio");
  - R-R8 ("Figurinha de Natal" na arte).
  - Os dois entram no pack de dezembro, depois de aprovados de novo na Mesa.
- **Conteúdo de Natal no ar desde antes da regra:** o post do Quiddo de 18/11 (https://www.instagram.com/p/Df41MTGCFXw/) continua publicado. Apagar é decisão do Gui.

## Auditoria de duplicados 13–22/11 (Codex, 22/11)

- Foram 33 publicações: Quiddo 10, Retrozap 12, SPORT DNA 11.
- Nenhum par duplicado confirmado.
- Limite da conferência: os vídeos não foram vistos quadro a quadro, e nem todos os slides internos dos carrosséis foram abertos.
- Nenhum outro post foi excluído.
- O relatório está no ambiente local do Codex.

## Séries

- A agenda tem a coluna `serie`. A trava do Growth usa uma janela de 30 dias por grupo (`growth/postagem/series.json`).
- Não produzir mais peças das séries travadas: F-QD-2/4/5, F-RZ-1..4, D-RX4..7.
