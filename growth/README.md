# Growth da Beyond the Work

Material do Growth Manager para Retrozap, Quiddo e SportDNA.

| Arquivo | Para quem | O que é |
|---|---|---|
| [plano-aceleracao.md](plano-aceleracao.md) | Você | Plano de aceleração (14/11): onde aprovar, status, lançamento do Retrozap, Quiddo, SportDNA, jornada dos 3 sites, Google, Meta, AdSense |
| [plano.md](plano.md) | Você | Diagnóstico, economia por marca, estratégia, plano e permissões |
| [briefing-conteudo.md](briefing-conteudo.md) | Chat de conteúdo (Claude) | 14 criativos novos com gancho, formato e texto |
| [briefing-chatgpt.md](briefing-chatgpt.md) | Agentes do ChatGPT | Tarefas de navegador na Meta e no Google, mais exportações semanais |
| [medicao-spec.md](medicao-spec.md) | Claude Code nos repositórios dos sites | Eventos padrão, Conversions API, Consent Mode e checkout |
| [postagem/](postagem/README.md) | Claude (publicador) | Publica a agenda aprovada do branch `social` no Instagram e no Facebook pela API |

Painel: **BTW Growth Board** (artifact no claude.ai, aberto pelo link que o Claude enviou no chat).

## Papéis e rotina (Gui, 15/11)

| Quem | Faz | Quando |
|---|---|---|
| ChatGPT do Gui | Opera os anúncios na Meta e no Google (cria, pausa, orçamento), sempre com o ok do Gui | 1 vez por semana, lendo a [fila](anuncios/fila.csv) |
| BTW Conteúdo (sessão do Estúdio) | Cria os ADs e o conteúdo orgânico a partir dos briefs do Growth; regras em `pipeline/ads/DIRECAO.md` (branch `social`) | Contínuo |
| Gui | Aprova na Mesa só o formato principal (9:16 ou 1:1) | 1 vez por semana (revisão de domingo) |
| Growth (Claude) | Posta o orgânico, mantém a fila de anúncios e a biblioteca da Meta, B2B (lojas, academias, creators) | Todo dia, às 9h47 |
| Growth (Claude) | **Revisão semanal**: lê as campanhas da Meta e do Google e sugere otimizações, ranqueia os criativos e manda briefs de variação ao Conteúdo, propõe fontes novas de receita. Resultado em [semanal/](semanal/) | Toda quinta, às 8h42, antes da revisão de domingo |

O Growth só lê as campanhas e sugere; quem executa é o ChatGPT, depois do ok do Gui.

## IDs que os agentes usam

- Business: Beyond the Work `303359410698910` (não verificado)
- Conta de anúncios com as 3 marcas: `act_1471479281571654` (nome atual "Retrozap", BRL)
- Conta vazia em USD: `act_1015430674912922` (não usar)
- Páginas: Retrozap `1481891254996380` · Quiddo `1336804232858527` · SPORT DNA `1460739327115922`
- Instagram: @retrozap.app · @sportdna.app · Quiddo `17841425670576940`
- Pixels: Retrozap `1522604139713675` · Quiddo `39663521416595790` · SPORT DNA `1109514848506414`
- GA4: Retrozap `G-R8R1EN0KQN` · Quiddo `G-18PBXS3GQZ` · SportDNA `G-BL3GWV6MGQ`
- Google Ads: `AW-18547334686` (tag só no Retrozap) · GTM Retrozap `GTM-NMLZBBQS`

## Regras que valem para todos

1. Tudo que for criado fica **PAUSADO**. Ativar, mudar orçamento ou gastar só com ok explícito do Guilherme.
2. Nunca subir dado de cliente ou usuário. No Retrozap: nada de mensagens, nomes ou telefones, nem em criativo.
3. Token da Meta só pelo formulário seguro, nunca em chat.
4. Site só na Cloudflare Pages. Nunca GitHub Pages.
