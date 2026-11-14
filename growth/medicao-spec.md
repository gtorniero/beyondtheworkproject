# Especificação de medição: Retrozap, Quiddo e SportDNA

**Para:** Claude Code nos repositórios de cada site
**Objetivo:** a Meta e o Google precisam enxergar o funil inteiro e a compra real, respeitando o consentimento. Hoje o pixel só liga depois do "Aceitar", quase nada chega pelo servidor e as etapas do funil são eventos personalizados que a Meta não usa para otimizar.

Auditoria feita em 14/11/2026, no celular (iPhone), aceitando cookies e com os envios bloqueados para não sujar os dados.

## 1. Eventos padrão junto com os personalizados

Mantenha os eventos atuais (são usados em relatórios). **Dispare também** o evento padrão, sempre com `value` e `currency: 'BRL'` e `content_category` = a página/produto real.

| Site | Evento atual | Evento padrão a adicionar | Parâmetros |
|---|---|---|---|
| Retrozap | RetrospectivaConcluida | `Lead` | content_category: grupo/casal |
| Retrozap | OfertaVista | `ViewContent` | value 8.99, content_ids: ['rz-premium'] |
| Retrozap | CheckoutAberto | `InitiateCheckout` | value, content_ids |
| Retrozap | PixGerado | `AddPaymentInfo` | value, payment: pix |
| Quiddo | CreateRoom | `Lead` (ou `StartTrial`) | content_category: corporativo/familia/escola |
| Quiddo | (abrir /precos) | `ViewContent` | content_ids: ['qd-passe7','qd-anual'] |
| SportDNA | QuizCompleted | `Lead` | content_category: racket/surf/run |
| SportDNA | OfferViewed | `ViewContent` | value 19.99/9.99, content_ids: ['racket-report'] etc. |
| Todos | Purchase | `Purchase` (já existe) | value, currency, content_ids, **event_id** |

Use os mesmos `content_ids` do catálogo de preços (`racket-report`, `surf-report`, `run-report`, `racket-comparator`) para resolver o alerta de "content_ids sem catálogo".

## 2. Conversions API para a compra

**Ela já existe.** No SportDNA: `payments/src/meta-capi.mjs` e `meta-adapter.mjs`, com consentimento guardado por pedido, fila de envio e revogação. Retrozap e Quiddo usam o mesmo padrão (`btw_capi_choice_v1`, `/api/meta/revoke`). Ela só envia compras de quem aceitou cookies, o que está certo. Por isso os eventos de servidor são poucos (4, 0 e 2) e a EMQ da compra está em 4,6 e 4,4.

O que conferir e ajustar:

- Em produção, nos 3 workers: `META_CAPI_ENABLED=true` e `META_EMAIL_MATCHING=true`. O Quiddo tem 0 eventos de servidor, então provavelmente está desligado lá.
- O payload leva `event_id` igual ao do navegador, `fbp`, `fbc`, `client_user_agent`, `external_id` com hash e `em` com hash quando `META_EMAIL_MATCHING` está ligado.
- O Pix de cada marca também enfileira a compra: SportDNA via Mercado Pago, Retrozap via Efí.
- O token de CAPI fica como secret do worker. Nunca no código.

## 3. Página real no pixel do Quiddo e do SportDNA

Nesses dois sites o pixel roda num iframe em `/medicao`, então toda visita chega à Meta como `/medicao?…`. Escolha uma opção:

- **(a)** Carregar o `fbevents.js` na página principal depois do consentimento, como o Retrozap já faz, ou
- **(b)** Manter o iframe e mandar em todo evento `content_category` e um parâmetro `page_path` com o caminho real (`/racket/`, `/run/`, `/criar`, `/precos`).

## 4. Compras de teste e internas

- O Stripe tem compras de teste do próprio dono, que viraram Purchase no pixel.
- Crie um modo interno (ex.: `?btw_interno=1` grava um cookie de 1 ano) que **não** dispara pixel, GA4 nem CAPI.
- Na Meta, use o código de teste do Gerenciador de Eventos para validar, nunca compras reais.

## 5. Google

- **Quiddo e SportDNA:** adicionar o **Consent Mode v2**, com padrão `denied` e `update` no aceite, como no Retrozap. Hoje o GA4 deles só carrega depois do aceite, então o Google não modela nada de quem recusa.
- **Quiddo e SportDNA:** adicionar a tag do Google Ads (mesma conta `AW-18547334686` ou uma por marca) e a conversão de compra com **conversões otimizadas** (e-mail com hash).
- **Os 3:** mandar `purchase` ao GA4 com `transaction_id`, `value` e `currency`, também pelo servidor (Measurement Protocol) a partir do webhook.

## 6. Checkout e funil

- **SportDNA:** `CheckoutError` disparou 2 vezes contra 8 compras. Ver os logs do worker de pagamento e testar Pix e cartão no celular. O config usa `sportdna-payments-test.guitorniero.workers.dev` com `mode: 'live'`: confirmar que é o worker de produção e renomear.
- **Retrozap:** o AdSense carrega na landing que recebe o tráfego pago. Mostrar anúncios só depois do resultado e nunca na tela da oferta ou do checkout.
- **Os 3:** o banner de cookies decide quanto do funil a gente enxerga. Testar uma versão com "Aceitar" em destaque e texto de uma linha (o "Recusar" continua visível, para seguir a LGPD) e medir a taxa de aceite pelo Cloudflare Web Analytics, que não usa cookie.

## 7. Endpoint de métricas (para o painel)

Em cada worker: `GET /api/metrics?from=AAAA-MM-DD&to=AAAA-MM-DD` protegido por um header `Authorization: Bearer <token>`. Deve devolver só agregados por dia, sem nenhum dado pessoal:

```json
{"rows":[{"data":"2026-11-13","produto":"racket-report","meio":"pix","vendas":2,"receita":39.98,"reembolsos":0}]}
```

Com isso o painel soma Pix + cartão e calcula o ROAS real. O Guilherme cola o token no formulário seguro do Claude, nunca no chat.

## Como validar

1. **Eventos de teste:** Gerenciador de Eventos → Eventos de teste. Cada evento padrão aparece com `value` e com "Navegador + Servidor" deduplicado.
2. **EMQ da compra:** acima de 6 em até 7 dias.
3. **Reconciliação:** Purchase na Meta e no GA4 ≈ vendas no Stripe + Efí no mesmo período, com diferença menor que 10%.
