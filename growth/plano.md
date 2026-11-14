# Plano de Growth: Retrozap, Quiddo e SportDNA

Retrato de 14/11/2026. Fontes: Meta Marketing API, estatísticas dos 3 pixels, auditoria dos sites no celular e Stripe.

## 1. Onde estamos

- **Investido na Meta desde 09/11:** R$ 145,61, com 5 compras atribuídas e R$ 55,95 de receita. **ROAS 0,38.**
- **Estrutura:** 3 campanhas de Vendas (Purchase) com orçamento total de cerca de R$ 120 cada, terminando em 19/11, todas numa conta só.
- **Por marca:**
  - **Retrozap:** R$ 51,90 investidos, 4 compras de R$ 8,99, ROAS 0,69, custo por compra R$ 12,97. Um anúncio só (RZ-03 Casal) trouxe as 4 compras.
  - **Quiddo:** R$ 47,29 investidos, 0 compras. O CTR é bom (3,3%), mas a compra só acontece quando o evento passa de 10 pessoas, o que leva dias.
  - **SportDNA (RACKET):** R$ 46,42 investidos, 1 compra de R$ 19,99, ROAS 0,43. O CPM é de R$ 103 porque o público é estreito demais.
- **Vendas reais no Stripe:** 4 cobranças no total, 2 delas testes seus. O Pix (Efí) não está visível para mim.

## 2. A conta que precisa fechar

A meta é ROAS 3: receita igual a 3 vezes a mídia. Se você quis dizer ROI 3 no sentido estrito (lucro 3 vezes a mídia), a régua sobe para ROAS 4.

| Marca | Preço principal | Custo máximo por compra para ROAS 3 | Custo por compra hoje |
|---|---|---|---|
| Retrozap | R$ 8,99 | R$ 3,00 | R$ 12,97 |
| Quiddo (Passe 7 dias) | R$ 12,99 | R$ 4,33 | sem compra |
| SportDNA (RACKET) | R$ 19,99 | R$ 6,66 | R$ 46,42 |

**Conclusão:** com esses preços, mídia paga não chega a ROAS 3 só na primeira venda. Otimizar campanha dá algo como 2×. O resto vem de vender mais por cliente e de converter melhor.

Alavancas, da maior para a menor:

1. **SportDNA: afiliados.** O relatório já recomenda raquete, corda, tênis e prancha. Um link de compra com comissão (Amazon, Netshoes, Centauro, lojas de tênis) sobre raquetes de R$ 800 a R$ 1.500 rende de R$ 30 a R$ 100 por comprador, mais que o próprio relatório. É a alavanca nº 1.
2. **Retrozap: combo e preço.** Grupo + Casal por R$ 14,90, "família inteira" (3 grupos) e teste de preço a R$ 12,90 em dezembro. Pix como padrão: no cartão, o Stripe come cerca de 8% de um ticket de R$ 8,99.
3. **Quiddo: vender o plano anual e o B2B.** O anual custa R$ 156, 12 vezes o passe. Empresas e escolas compram por busca, então ir para Google Search. No B2C, usar Natal e confraternização em dezembro.
4. **Conversão:** checkout do SportDNA com erros, AdSense no meio do funil do Retrozap, oferta clara de "grátis até 10" no Quiddo.
5. **Medição** (seção 4). Sem ela, a Meta otimiza às cegas e qualquer escala é chute.

## 3. Mídia: o que mudar

**Duplicar conjuntos com públicos diferentes? Não agora.** Com cerca de R$ 12 por dia por marca, cada conjunto novo divide o pouco sinal que existe e nada sai da fase de aprendizado. Boas práticas atuais:

- **Uma campanha por marca, um conjunto, público aberto** (Advantage+), de 4 a 6 criativos. O criativo é que segmenta.
- **Evento de otimização com volume.** Purchase precisa de cerca de 50 por semana para estabilizar, e estamos com cerca de 5. Teste A/B por 7 dias:
  - SportDNA: "Terminou o teste" contra Purchase
  - Quiddo: "Sala criada" contra Purchase
  - Retrozap: continuar em Purchase (já tem volume) e testar "Gerou o Pix"

  As 7 conversões personalizadas para isso **já foram criadas**.
- **RACKET:** tirar os interesses de tênis e a faixa 25–55 e deixar o público aberto, com o criativo falando com tenista. Meta: CPM abaixo de R$ 40.
- **Quiddo:** separar B2C (festas e Natal, na Meta) de B2B/escola (Google). Os anúncios duplicados entre os dois conjuntos competem entre si.
- **Remarketing** só quando os públicos do pixel passarem de 1.000 pessoas.
- **Atribuição:** comparar 7 dias de clique com 1 dia de clique. Em produto de impulso, 1 dia é mais honesto.
- **Escala:** só abaixo do custo máximo por compra, subindo 20% a cada 3 dias.

**Para executar quando você aprovar** (eu faço pela API, deixando pausado e ativando só com o seu ok):

1. Pausar o RZ-05 Fantasma.
2. Montar a campanha nova do Quiddo, com um conjunto otimizado por Sala criada.
3. Abrir o público do RACKET.
4. Montar a estrutura de dezembro do Retrozap.

## 4. Medição: o que está errado

Detalhes técnicos em [medicao-spec.md](medicao-spec.md).

- **Os 3 sites só ligam o pixel e o GA4 depois do "Aceitar".** Isso está certo pela LGPD, mas cerca de 2 em cada 3 cliques somem. O "vazamento" clique→visita é em boa parte medição. Os sites são rápidos (primeiro conteúdo em 0,4 a 1,3 s).
- **Conversions API praticamente desligada:** 4, 0 e 2 eventos de servidor. A nota de correspondência da compra (EMQ) está em 4,6 e 4,4; o saudável é a partir de 6.
- **O funil está em eventos personalizados** (OfertaVista, CheckoutAberto, PixGerado, QuizCompleted). A Meta não usa essas etapas para otimizar: a campanha do Retrozap mostra 0 checkouts.
- **Pixel do Quiddo e do SportDNA dentro de um iframe `/medicao`:** toda visita aparece como /medicao.
- **O pixel conta mais compras que o caixa:** 10 no Retrozap e 8 no SportDNA, contra 4 cobranças no Stripe. Faltam o Pix e a exclusão das compras de teste.
- **SportDNA:** 2 erros de checkout, e o worker de pagamento tem "test" no nome em produção.
- **Google:** GA4 nos 3 sites; Google Ads e Consent Mode v2 só no Retrozap.

## 5. Google ou Meta

| Marca | Comece em | Por quê |
|---|---|---|
| SportDNA | **Google Search** | "qual raquete comprar", "raquete para iniciante", "qual tênis de corrida" são buscas de decisão |
| Quiddo empresas/escola | **Google Search** | "quiz ao vivo", "quiz para convenção", "dinâmica para treinamento"; ticket anual de R$ 156 |
| Quiddo festas | Meta (dezembro) | Natal, aniversário, chá-bar: descoberta e vídeo |
| Retrozap | **Meta** | Impulso e viral, Reels/Stories/WhatsApp; Google só na temporada |

Regra de decisão: a mesma régua (custo por compra real contra o máximo para a meta) nos dois canais. Teste de 14 dias, depois 70/20/10.

## 6. Plano

| Quando | Ação | Quem | Precisa ok |
|---|---|---|---|
| Hoje | Pausar RZ-05 | Claude (API) | Sim |
| Hoje | Aceitar os termos de público personalizado (1 clique) | Você ou ChatGPT | — |
| Hoje | ✅ 7 conversões personalizadas criadas | Claude | — |
| Depois do aceite | 12 públicos do pixel por etapa do funil | Claude (API) | Não |
| Semana 1 | Eventos padrão + Conversions API + exclusão de testes | Claude Code nos repositórios | Não |
| Semana 1 | Correspondência automática avançada nos 3 pixels | ChatGPT | Não |
| Semana 1 | Combo/preço do Retrozap; afiliados do SportDNA | Você | Sim |
| Semana 1 | Quiddo num conjunto só (Sala criada); abrir o público do RACKET | Claude (API) | Sim |
| Semana 1 | 14 criativos novos | Chat de conteúdo | Aprovação |
| Semana 2 | Tag Google Ads + Consent Mode v2 em Quiddo e SportDNA | Claude Code | Não |
| Semana 2 | Search para RACKET DNA e Quiddo empresas/escola | ChatGPT | Sim (verba) |
| Toda segunda | Exportar GA4, Search Console e Google Ads para o Drive | ChatGPT | Não |
| Toda segunda | Atualizar o painel e mandar 3 decisões | Claude | — |
| 1/12 a 7/1 | Temporada da retrospectiva (Retrozap) e do Natal (Quiddo) | Todos | Sim |

## 7. Permissões que ainda faltam

| O quê | Para quê | Como |
|---|---|---|
| Termos de público personalizado da Meta | Criar os 12 públicos | Abrir facebook.com/customaudiences/app/tos/?act=1471479281571654 e aceitar |
| Verificação do Business | Mais recursos e limites | Meta Business → Central de segurança → Verificar (CNPJ) |
| Conectar GitHub dos sites (Retrozap, Quiddo, SportDNA) | Eu mesmo implementar a medição | Pedir aqui e eu adiciono o repositório à sessão |
| Endpoint de métricas por site (vendas por dia e produto, sem dado pessoal) | Somar o Pix (Efí) ao painel e fechar o ROAS real | Claude Code cria o `/api/metrics` com token; você cola o token no formulário seguro |
| Token de leitura do Cloudflare Web Analytics | Visitas reais, sem depender de cookie | Cloudflare → API Tokens → "Account Analytics: Read" e formulário seguro para api.cloudflare.com |
| GA4, Search Console, Google Ads | Ler o Google | Por enquanto, exportação semanal no Drive (já conectado aqui). Depois, API do Google Ads com developer token |
| `instagram_basic`, `instagram_manage_insights`, `read_insights` no token | Ler resultado orgânico | Gerar o token de novo com essas permissões |

Não precisa: publicar posts pela minha sessão (o agente do ChatGPT já faz) nem modelo Fable para este trabalho.
