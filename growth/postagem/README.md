# Postagem automática (Instagram + Facebook)

O `postar.py` publica a agenda aprovada das três marcas (Retrozap, Quiddo, SPORT DNA) pela Graph API v23.0. Desde 15/11/2026 o Claude é o único publicador. O DOT e o Business Suite saíram do fluxo.

## O que ele faz

1. Busca o branch `social` (`git fetch`) e lê, de cada `packs/<pack>/`: `agenda.csv`, `STATUS.json`, `manifest.json` e `<marca>/LEGENDAS.txt`. Sempre a versão mais nova.
2. Pega as linhas da agenda que venceram na janela pedida. Uma peça só sai se a versão da agenda estiver no `STATUS.json` com `liberado: true` e `status_mesa: "aprovado"`. Reservas não saem, a não ser com `--incluir-reserva`.
3. A legenda vem do `LEGENDAS.txt` da marca, na versão exata. Se a versão nova não tiver bloco próprio (ex.: reels v2 do S03, que só trocaram a trilha), usa o bloco da mesma peça e avisa. Story não tem legenda.
4. Bloqueia sozinho: "Wrapped" no Retrozap, preço R$ 8,99 do Retrozap fora da promoção de dezembro, reel sem som, legenda acima de 2.200 caracteres, link quebrado, versão fora do STATUS. Para liberar uma peça bloqueada depois do ok do Gui: `--liberar PECA` (ou `--permitir-mudo` para reel sem som).
5. Segura o que está em `segurar.json`. Peça segurada é pulada com "segurado: aguardando versão aprovada" e só sai quando a agenda apontar uma versão diferente da segurada e aprovada. Para segurar ou soltar, edite o arquivo.
6. Não repete nada: confere o `publicados.json` (mesma peça e rede, em qualquer versão) e as contas (últimos 25 posts do Instagram e da página com a mesma 1ª linha de legenda, mais stories não registrados nas 3 h antes do horário).
7. Publica:
   - **story:** Instagram `STORIES`. Facebook story de foto (`/photos` oculta → `/photo_stories`) ou de vídeo (`/video_stories`). Adesivos não entram pela API; o relatório lista os que a agenda pede.
   - **reel:** Instagram `REELS` com capa e `share_to_feed`, espera `FINISHED` e publica. Facebook `/video_reels`. Se o upload do Reels for bloqueado pela rede, sobe como vídeo da página e avisa.
   - **carrossel:** Instagram `CAROUSEL`. Facebook post com várias fotos.
8. Grava cada publicação no `publicados.json` na hora e, no fim, faz `git pull --rebase`, commit e push do registro neste branch. Nunca no `social` nem na `main`.
9. Se uma marca falhar, segue com as outras. Erros temporários têm nova tentativa com espera crescente. O relatório final traz links, pulados, segurados, bloqueados e erros.

O token da Meta é injetado pelo proxy em `graph.facebook.com`. O token de página é pedido na hora e fica só na memória. Nada de token em log, arquivo ou tela.

## Como rodar

Sempre da raiz do repositório, com `python3 -I`.

```sh
# o que sairia agora (últimos 30 min e até 15 min à frente)
python3 -I growth/postagem/postar.py --dry-run

# conferir um dia inteiro, com links, specs do vídeo e containers do Instagram (sem publicar)
python3 -I growth/postagem/postar.py --dry-run --quando 2026-11-16T23:59 --janela 1439 --checar-midia --validar-containers

# publicar o que venceu
python3 -I growth/postagem/postar.py --executar

# tabela de cobertura e buracos de story
python3 -I growth/postagem/postar.py --cobertura 2026-11-15:2026-12-06
```

Outras opções: `--marca quiddo`, `--peca R-RX1`, `--plataformas instagram`, `--relatorio arquivo.json`, `--sem-fetch`, `--sem-git`.

O `--executar` nunca publica o que está marcado para mais de 15 min no futuro. Para recuperar algo atrasado, use um `--quando` no passado, por exemplo `--quando 2026-11-13T12:00 --janela 5 --peca Q-S4`.

## Horários

As agendas usam três horários, em Brasília: **12h** (stories), **12h30** (carrosséis) e **19h45** (reels). Rode `--executar` em cada um deles com a janela padrão de 30 min. Se uma rodada falhar, a seguinte pega o que ficou para trás, desde que esteja dentro da janela. Use `--janela` maior para recuperar.

## Arquivos

| Arquivo | O que é |
|---|---|
| `postar.py` | O publicador |
| `segurar.json` | Peças seguradas, com motivo e a versão a partir da qual podem sair |
| `publicados.json` | Registro do que saiu (ou já existia) em cada rede, com id e link |

## Nada sai duplicado (18/11)

O `postar.py` só publica uma peça se ela passar por todas estas travas:

1. **Registro:** a peça (marca + peça, qualquer versão) já está no `publicados.json`, então não sai de novo.
2. **Conta:** no feed, se já existe post com a mesma 1ª linha de legenda, não sai. No story, se já existe um story fora do registro perto do horário, também não sai.
3. **Mesma mídia:** o mesmo arquivo (mesmo blob do git, com qualquer nome ou versão) já saiu por outra peça da marca, ou sai antes na agenda, então não sai. No carrossel, a regra vale com metade ou mais dos cards repetidos, porque o card final de CTA se repete de propósito. O registro guarda os blobs de cada publicação.
4. **Um por dia:** cada marca tem 1 reel e 1 carrossel por dia. Se houver dois aprovados no mesmo dia, ganha o que já saiu; depois, o de pack especial (ex.: QUIDDO-EDUCACAO) ganha do pack da semana; o outro fica bloqueado.
5. **Facebook:** desligado desde 17/11 (`sem_facebook.json`), porque ele republicava no Instagram.
6. **Sequência de stories:** o story base do Quiddo cede para a sequência aprovada do mesmo dia, e cada quadro só sai depois do anterior.
