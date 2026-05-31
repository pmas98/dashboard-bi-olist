# RELATÓRIO TÉCNICO DE ANÁLISE

## Painel BI Interativo da Base Olist

## Capa

**Instituição:** Universidade de Fortaleza (UNIFOR)  
**Curso:** preencher com o nome do curso  
**Disciplina:** Business Intelligence / Análise de Dados  
**Professor:** preencher com o nome do professor  
**Equipe:** preencher com os nomes dos integrantes  
**Base analisada:** Brazilian E-Commerce Public Dataset by Olist  
**Ferramenta usada:** Python, Streamlit, Pandas e Plotly

---

# 1. Definição do Problema

A equipe analisou uma base pública de e-commerce brasileiro para responder uma pergunta de gestão: **onde a operação vende bem, onde entrega mal e onde isso afeta a experiência do cliente?**

Essa pergunta importa porque uma loja virtual não decide apenas por faturamento. Um estado pode gerar muitas vendas e, ao mesmo tempo, concentrar atrasos. Uma categoria pode parecer boa por receita, mas esconder avaliações baixas. O gestor precisa enxergar receita, prazo, frete e nota do cliente juntos.

O dashboard apoia quatro decisões principais:

- quais categorias merecem prioridade comercial;
- quais estados exigem revisão logística;
- quais períodos indicam crescimento, queda ou sazonalidade;
- quais combinações de categoria, estado e atraso ameaçam a satisfação do cliente.

## Informação gerada por cada gráfico

| Gráfico ou indicador | Informação produzida | Decisão possível |
|---|---|---|
| KPIs principais | Faturamento, pedidos, ticket médio, frete médio, atraso médio real e avaliação média | Avaliar se o recorte filtrado está saudável |
| Linha de faturamento mensal | Meses de alta, queda e retomada de receita | Planejar estoque, campanha e capacidade operacional |
| Barras de pedidos por mês | Volume de pedidos em cada mês | Separar aumento de receita por volume de aumento por ticket |
| Categorias por faturamento | Categorias que mais geram receita | Priorizar estoque, marketing e negociação com vendedores |
| Receita por UF e atraso médio | Estados com maior impacto financeiro e maior atraso | Direcionar melhoria logística para regiões críticas |
| Dispersão entre atraso e avaliação | Relação entre demora na entrega e nota do cliente | Identificar se atraso reduz satisfação |
| Formas de pagamento | Meios de pagamento mais usados | Ajustar checkout, parcelamento e campanhas |
| Ranking de oportunidade | Categorias com receita alta, atraso e risco de nota baixa | Escolher onde agir primeiro |

O painel permite combinar filtros. A equipe pode, por exemplo, selecionar pedidos entregues, escolher um estado, limitar uma categoria e observar se a nota cai quando o atraso aumenta. Essa combinação transforma o painel em ferramenta de investigação, não em lista de gráficos.

---

# 2. Metadados e Estrutura

## Fonte da base

A equipe usou a base **Brazilian E-Commerce Public Dataset by Olist**, disponível publicamente no Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Para facilitar a execução do dashboard, o projeto carrega os arquivos CSV por um espelho público no GitHub:

`https://raw.githubusercontent.com/Athospd/work-at-olist-data/master/datasets/`

A base contém pedidos de e-commerce realizados no Brasil entre 2016 e 2018. Ela reúne dados de compra, cliente, produto, pagamento, entrega e avaliação.

## Tabelas usadas

### `olist_orders_dataset.csv`

Tabela central dos pedidos.

| Coluna | Descrição |
|---|---|
| `order_id` | Código único do pedido |
| `customer_id` | Código do cliente naquele pedido |
| `order_status` | Situação do pedido |
| `order_purchase_timestamp` | Data e hora da compra |
| `order_approved_at` | Data de aprovação do pagamento |
| `order_delivered_carrier_date` | Data de envio para a transportadora |
| `order_delivered_customer_date` | Data de entrega ao cliente |
| `order_estimated_delivery_date` | Data prometida para entrega |

### `olist_customers_dataset.csv`

Tabela de localização do cliente.

| Coluna | Descrição |
|---|---|
| `customer_id` | Código do cliente no pedido |
| `customer_unique_id` | Código único do cliente |
| `customer_zip_code_prefix` | Prefixo do CEP |
| `customer_city` | Cidade do cliente |
| `customer_state` | Estado do cliente |

### `olist_order_items_dataset.csv`

Tabela dos itens vendidos.

| Coluna | Descrição |
|---|---|
| `order_id` | Código do pedido |
| `order_item_id` | Número do item dentro do pedido |
| `product_id` | Código do produto |
| `seller_id` | Código do vendedor |
| `shipping_limit_date` | Prazo limite de envio |
| `price` | Preço do produto |
| `freight_value` | Valor do frete |

### `olist_products_dataset.csv`

Tabela de características do produto.

| Coluna | Descrição |
|---|---|
| `product_id` | Código do produto |
| `product_category_name` | Categoria original |
| `product_name_lenght` | Tamanho do nome do produto |
| `product_description_lenght` | Tamanho da descrição |
| `product_photos_qty` | Quantidade de fotos |
| `product_weight_g` | Peso em gramas |
| `product_length_cm` | Comprimento em centímetros |
| `product_height_cm` | Altura em centímetros |
| `product_width_cm` | Largura em centímetros |

### `product_category_name_translation.csv`

Tabela auxiliar de tradução das categorias.

| Coluna | Descrição |
|---|---|
| `product_category_name` | Categoria original |
| `product_category_name_english` | Categoria traduzida |

### `olist_order_payments_dataset.csv`

Tabela de pagamentos.

| Coluna | Descrição |
|---|---|
| `order_id` | Código do pedido |
| `payment_sequential` | Ordem do pagamento |
| `payment_type` | Tipo de pagamento |
| `payment_installments` | Número de parcelas |
| `payment_value` | Valor pago |

### `olist_order_reviews_dataset.csv`

Tabela de avaliações.

| Coluna | Descrição |
|---|---|
| `review_id` | Código da avaliação |
| `order_id` | Código do pedido avaliado |
| `review_score` | Nota de 1 a 5 |
| `review_comment_title` | Título do comentário |
| `review_comment_message` | Texto do comentário |
| `review_creation_date` | Data da avaliação |
| `review_answer_timestamp` | Data de resposta |

## Colunas criadas

| Coluna | Descrição |
|---|---|
| `delivery_delay_days` | Diferença entre entrega real e entrega prometida. Pode ser negativa quando a entrega chegou antes |
| `late_delay_days` | Dias reais de atraso. Pedidos no prazo ou antecipados entram como zero |
| `delivery_days` | Tempo entre compra e entrega |
| `purchase_month` | Mês da compra |
| `purchase_date` | Data da compra |
| `is_late` | Indica se o pedido atrasou |
| `category` | Categoria usada no painel |
| `revenue` | Receita do produto, sem frete |
| `total_order_value` | Valor total pago no pedido |

---

# 3. Processo de Pré-processamento

A base original não vinha pronta para análise. Cada arquivo respondia por uma parte da operação. A equipe precisou unir pedidos, itens, clientes, produtos, pagamentos e avaliações.

## 3.1 Limpeza

A equipe aplicou os seguintes tratamentos:

- converteu colunas de data para formato temporal;
- manteve datas nulas de entrega quando o pedido não tinha entrega registrada;
- marcou categorias ausentes como `uncategorized`;
- marcou pagamentos ausentes como `not_informed`;
- removeu duplicidades nos campos usados para itens;
- uniu as tabelas por `order_id`, `customer_id` e `product_id`;
- padronizou a categoria final usada nos gráficos.

A equipe também corrigiu uma armadilha comum na métrica de atraso. A diferença `entrega real - entrega estimada` gera valores negativos quando o pedido chega antes do prazo. Esse valor ajuda a estudar antecipação, mas não serve como KPI de atraso médio.

Por isso, o dashboard usa `late_delay_days` para o indicador principal:

- atraso maior que zero mantém o número de dias;
- entrega no prazo recebe zero;
- entrega antecipada recebe zero.

Com essa regra, o KPI informa atraso real. No filtro padrão de pedidos entregues, o atraso médio fica em torno de **0,69 dia**, e não em valor negativo.

## 3.2 Transformação

A equipe criou variáveis analíticas para responder às perguntas do painel:

- `delivery_delay_days`, para medir diferença contra o prazo prometido;
- `late_delay_days`, para medir atraso real;
- `delivery_days`, para calcular tempo total de entrega;
- `purchase_month`, para analisar tendência mensal;
- `is_late`, para calcular taxa de atraso;
- `revenue`, para medir venda de produto;
- `total_order_value`, para acompanhar valor pago.

A equipe também agregou pagamentos por pedido. Quando um pedido usou mais de um meio de pagamento, o painel combinou os tipos em uma única descrição e somou os valores pagos.

A receita foi calculada sem frete. Essa escolha evita inflar o faturamento com custo logístico. O frete aparece como indicador separado.

## 3.3 Redução

A equipe reduziu a base por relevância analítica usando filtros interativos:

- período da compra;
- UF do cliente;
- categoria;
- status do pedido;
- forma de pagamento;
- faixa de avaliação.

O painel inicia com `delivered` como status padrão. Esse recorte faz sentido porque pedidos entregues têm datas de entrega e avaliações mais úteis para a análise logística.

---

# 4. Dashboard Interativo

A equipe desenvolveu o painel em Python com Streamlit e Plotly. O usuário filtra a base pela barra lateral e todos os gráficos mudam junto.

## Filtros disponíveis

- período da compra;
- UF do cliente;
- categoria;
- status do pedido;
- forma de pagamento;
- faixa de avaliação.

## Indicadores exibidos

No filtro padrão de pedidos entregues, o painel apresenta:

- **96.478 pedidos**;
- **ticket médio de R$ 137,66**;
- **frete médio de R$ 19,98**;
- **atraso médio real de 0,69 dia**;
- **avaliação média de 4,07/5**;
- **taxa de atraso aproximada de 6,58%**.

Esses números resumem a operação. A taxa de atraso mostra que a maioria dos pedidos chegou no prazo ou antes dele. Ao mesmo tempo, o painel permite encontrar os grupos em que o atraso pesa mais.

## Demonstração dos filtros combinados

Durante a apresentação, a equipe pode seguir este roteiro:

1. manter o status `delivered`;
2. observar os KPIs gerais;
3. selecionar uma UF com alto faturamento;
4. escolher uma categoria relevante;
5. analisar a linha de faturamento por mês;
6. comparar atraso e avaliação;
7. consultar o ranking de oportunidade.

Esse roteiro mostra como o painel sai da visão geral e chega em uma decisão específica.

---

# 5. Justificativa Visual

A equipe escolheu cada gráfico de acordo com a pergunta de negócio.

## KPIs

Os KPIs abrem a análise porque o gestor precisa ler a situação geral em poucos segundos. Eles mostram tamanho, valor, custo logístico, atraso e satisfação.

## Linha temporal

A linha mostra faturamento mensal. Esse formato funciona para tendência porque preserva a ordem do tempo e facilita a leitura de crescimento, queda e sazonalidade.

## Barras por mês

As barras mostram pedidos por mês. A comparação de alturas ajuda a separar meses de maior volume de meses de menor movimento.

## Barras por categoria

As barras horizontais ordenam categorias por faturamento. Esse gráfico facilita ranking e evita rótulos apertados.

## Barras por UF

O gráfico por UF compara estados e usa cor para indicar atraso médio. O gestor enxerga onde existe receita alta e risco logístico no mesmo visual.

## Dispersão entre atraso e avaliação

A dispersão mostra cada pedido como ponto. Esse gráfico ajuda a investigar se pedidos com mais dias de atraso recebem notas menores.

## Barras por forma de pagamento

As barras por pagamento mostram preferência dos clientes. O gestor usa essa leitura para campanhas, parcelamento e melhoria de checkout.

## Ranking de oportunidade

O ranking combina receita, atraso e avaliação. Ele ajuda a equipe a sair da descrição e apontar prioridade de ação.

---

# 6. Análise de Diagnóstico e Plano de Ação

## 6.1 O Diagnóstico

A anomalia escolhida para investigação foi:

**por que algumas categorias com bom faturamento ainda representam risco para a satisfação do cliente?**

O painel mostra que a operação geral tem avaliação média positiva, cerca de **4,07/5**, e atraso médio real baixo, cerca de **0,69 dia**. Mesmo assim, a média geral esconde casos críticos. Entre os pedidos que atrasam, o atraso médio fica perto de **10,49 dias**. Esse grupo pequeno pode gerar reclamações, notas baixas e perda de recompra.

A leitura de negócio é simples: a empresa não deve tratar todos os pedidos da mesma forma. O gestor deve procurar categorias e estados em que três sinais aparecem juntos:

- receita alta;
- atraso acima da média;
- avaliação abaixo do ideal.

Essas combinações indicam perda de qualidade em áreas que importam financeiramente.

## 6.2 A Prescrição

A equipe recomenda priorizar ações logísticas e comerciais nos recortes que aparecem no ranking de oportunidade.

Plano de ação:

- revisar prazos prometidos nas UFs com maior atraso;
- negociar SLA com transportadoras desses estados;
- monitorar pedidos de categorias de alto faturamento antes da data prometida;
- oferecer cupom de recompra ou frete grátis para clientes com atraso relevante;
- avaliar vendedores associados a atrasos recorrentes;
- evitar campanhas agressivas em regiões onde a operação não sustenta o prazo.

A ação prática sugerida para o gestor é:

**criar uma rotina semanal de acompanhamento para categorias de alto faturamento com atraso acima de 5 dias, acionando transportadora e vendedor antes que a avaliação do cliente seja registrada.**

Essa ação reduz dano financeiro e reputacional. O gestor atua primeiro onde a receita é maior e a experiência do cliente corre mais risco.

---

# Conclusão

A equipe transformou uma base pública de e-commerce em um painel de BI interativo. O painel permite filtrar a operação por período, estado, categoria, status, pagamento e avaliação.

A análise mostra que os dados mais importantes para decisão não estão isolados. Receita, atraso, frete e avaliação precisam aparecer juntos. Com essa combinação, o gestor entende onde a operação performa bem e onde precisa agir.

O dashboard apoia uma decisão clara: priorizar categorias e regiões com alto impacto financeiro e maior risco logístico. Essa leitura transforma dados históricos em plano de ação.
