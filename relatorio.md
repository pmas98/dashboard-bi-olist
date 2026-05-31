# RELATÓRIO TÉCNICO DE ANÁLISE

## Painel BI Interativo de E-commerce Brasileiro com a Base Pública da Olist

**Instituição:** Universidade de Fortaleza (UNIFOR)  
**Curso:** preencher com o nome do curso  
**Disciplina:** Business Intelligence / Análise de Dados  
**Professor:** preencher com o nome do professor  
**Equipe:** preencher com os nomes dos integrantes  
**Projeto:** Análise descritiva e dashboard interativo com dados públicos de e-commerce

---

# 1. Definição do Problema

Este trabalho analisa uma base pública de comércio eletrônico brasileiro com o objetivo de apoiar decisões gerenciais sobre vendas, desempenho logístico, comportamento regional, formas de pagamento e satisfação do cliente. A base escolhida foi a **Brazilian E-Commerce Public Dataset by Olist**, que reúne informações de pedidos realizados no marketplace da Olist entre 2016 e 2018.

A dor de negócio investigada é a seguinte: **como identificar, de forma interativa, quais categorias, estados e períodos concentram maior faturamento, maior risco logístico e pior experiência do cliente?**

Em uma operação de e-commerce, olhar apenas o total de pedidos ou o faturamento absoluto não é suficiente. Uma categoria pode vender muito, mas apresentar atrasos e avaliações ruins. Um estado pode gerar receita relevante, mas exigir revisão de prazo ou frete. Uma forma de pagamento pode concentrar pedidos e influenciar a estratégia comercial. Por isso, o dashboard foi construído para cruzar indicadores comerciais e operacionais em uma mesma visão.

O dashboard deve apoiar decisões como:

- priorizar categorias com maior faturamento;
- identificar regiões com maior impacto financeiro;
- avaliar se atrasos de entrega prejudicam a satisfação;
- observar tendências mensais de crescimento ou queda;
- selecionar oportunidades de ação logística ou comercial;
- comparar formas de pagamento usadas pelos clientes.

## Informação gerada por cada gráfico e decisão possível

| Elemento do dashboard | Informação produzida | Decisão apoiada |
|---|---|---|
| KPIs principais | Faturamento, número de pedidos, ticket médio, frete médio, atraso médio e avaliação média | Avaliar rapidamente a saúde geral da operação filtrada |
| Linha temporal de faturamento | Evolução mensal da receita | Identificar sazonalidade, queda, crescimento ou meses de maior demanda |
| Barras de pedidos por mês | Volume mensal de pedidos | Planejar capacidade operacional, estoque e atendimento |
| Barras por categoria | Categorias com maior faturamento | Priorizar campanhas, estoque e negociação com vendedores |
| Barras por UF | Estados com maior receita e atraso médio | Direcionar melhorias logísticas para regiões de maior impacto |
| Dispersão entre atraso e avaliação | Relação entre atraso de entrega e nota do cliente | Verificar se a experiência de entrega afeta a satisfação |
| Barras por forma de pagamento | Meios de pagamento mais utilizados | Apoiar decisões de checkout, parcelamento e promoções |
| Ranking de oportunidade | Categorias que combinam receita alta, atraso e avaliação menor | Definir plano de ação prático para maior retorno gerencial |

Com os filtros combinados, a análise deixa de ser apenas descritiva geral e passa a permitir investigação: por exemplo, selecionar um estado, uma categoria e um período para observar se a queda na avaliação está associada a atraso ou a outro comportamento operacional.

---

# 2. Metadados e Estrutura

## Fonte dos dados

A base utilizada é pública e foi disponibilizada pela Olist para estudos de dados e inteligência de negócios.

- Fonte principal: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- CSVs usados no projeto: `https://raw.githubusercontent.com/Athospd/work-at-olist-data/master/datasets/`

## Estrutura geral da base

A base é relacional, ou seja, os dados estão distribuídos em várias tabelas que se conectam principalmente pelo campo `order_id`. Essa estrutura é adequada para BI porque permite combinar dimensões de venda, cliente, produto, pagamento, entrega e avaliação.

## Tabelas utilizadas

### `olist_orders_dataset.csv`

Tabela central dos pedidos.

| Coluna | Significado |
|---|---|
| `order_id` | Identificador único do pedido |
| `customer_id` | Identificador do cliente no pedido |
| `order_status` | Situação do pedido, como entregue, cancelado ou enviado |
| `order_purchase_timestamp` | Data e hora da compra |
| `order_approved_at` | Data de aprovação do pagamento |
| `order_delivered_carrier_date` | Data em que o pedido foi entregue à transportadora |
| `order_delivered_customer_date` | Data em que o cliente recebeu o pedido |
| `order_estimated_delivery_date` | Data estimada de entrega |

### `olist_customers_dataset.csv`

Tabela com informações geográficas dos clientes.

| Coluna | Significado |
|---|---|
| `customer_id` | Identificador do cliente no pedido |
| `customer_unique_id` | Identificador único do cliente |
| `customer_zip_code_prefix` | Prefixo do CEP |
| `customer_city` | Cidade do cliente |
| `customer_state` | Estado do cliente |

### `olist_order_items_dataset.csv`

Tabela com os itens comprados em cada pedido.

| Coluna | Significado |
|---|---|
| `order_id` | Identificador do pedido |
| `order_item_id` | Número sequencial do item dentro do pedido |
| `product_id` | Identificador do produto |
| `seller_id` | Identificador do vendedor |
| `shipping_limit_date` | Prazo limite para envio |
| `price` | Valor do produto |
| `freight_value` | Valor do frete |

### `olist_products_dataset.csv`

Tabela de produtos.

| Coluna | Significado |
|---|---|
| `product_id` | Identificador do produto |
| `product_category_name` | Categoria original do produto |
| `product_name_lenght` | Tamanho do nome do produto |
| `product_description_lenght` | Tamanho da descrição |
| `product_photos_qty` | Quantidade de fotos |
| `product_weight_g` | Peso em gramas |
| `product_length_cm` | Comprimento |
| `product_height_cm` | Altura |
| `product_width_cm` | Largura |

### `product_category_name_translation.csv`

Tabela auxiliar de tradução das categorias.

| Coluna | Significado |
|---|---|
| `product_category_name` | Categoria original em português |
| `product_category_name_english` | Categoria traduzida para inglês |

### `olist_order_payments_dataset.csv`

Tabela de pagamentos.

| Coluna | Significado |
|---|---|
| `order_id` | Identificador do pedido |
| `payment_sequential` | Sequência do pagamento |
| `payment_type` | Tipo de pagamento |
| `payment_installments` | Número de parcelas |
| `payment_value` | Valor pago |

### `olist_order_reviews_dataset.csv`

Tabela de avaliações dos clientes.

| Coluna | Significado |
|---|---|
| `review_id` | Identificador da avaliação |
| `order_id` | Identificador do pedido |
| `review_score` | Nota dada pelo cliente, de 1 a 5 |
| `review_comment_title` | Título do comentário |
| `review_comment_message` | Mensagem do comentário |
| `review_creation_date` | Data de criação da avaliação |
| `review_answer_timestamp` | Data de resposta da avaliação |

## Colunas criadas no projeto

| Coluna | Significado |
|---|---|
| `delivery_delay_days` | Diferença entre entrega real e entrega estimada. Pode ser negativa quando a entrega ocorreu antes do prazo |
| `late_delay_days` | Atraso real em dias. Entregas antecipadas ou no prazo entram como zero |
| `delivery_days` | Tempo total entre compra e entrega ao cliente |
| `purchase_month` | Mês da compra |
| `purchase_date` | Data da compra |
| `is_late` | Indica se houve atraso |
| `category` | Categoria final usada no dashboard |
| `revenue` | Receita do produto, calculada pelo preço do item |
| `total_order_value` | Valor total pago no pedido |

---

# 3. Processo de Pré-processamento

O pré-processamento foi necessário porque os dados originais estavam distribuídos em tabelas separadas e em diferentes níveis de granularidade. Algumas tabelas estavam no nível do pedido, outras no nível do item, outras no nível do pagamento e outras no nível da avaliação.

## 3.1 Limpeza

A limpeza dos dados envolveu:

- conversão das colunas de data para formato temporal;
- preservação de valores nulos em datas de entrega quando o pedido não tinha entrega registrada;
- tratamento de categorias ausentes como `uncategorized`;
- tratamento de formas de pagamento ausentes como `not_informed`;
- remoção de duplicidades nos itens selecionados para análise;
- integração das tabelas por chaves como `order_id`, `customer_id` e `product_id`;
- padronização da categoria usada no dashboard.

Um ponto importante foi o tratamento da métrica de atraso. A diferença entre entrega real e entrega estimada pode ser negativa quando o pedido chega antes do prazo. Porém, para o KPI **Atraso médio**, não faz sentido apresentar atraso negativo. Por isso, foi criada a coluna `late_delay_days`, em que:

- se o pedido atrasou, mantém os dias de atraso;
- se o pedido chegou no prazo ou antes, o valor é zero.

Com isso, o painel evita a interpretação incorreta de que existe “atraso médio negativo”.

## 3.2 Transformação

As principais transformações foram:

- criação de `delivery_delay_days`;
- criação de `late_delay_days`;
- criação de `delivery_days`;
- criação de `purchase_month`;
- criação de `is_late`;
- criação de `revenue`;
- criação de `total_order_value`;
- agregação dos pagamentos no nível do pedido;
- junção dos pedidos com clientes, itens, produtos, pagamentos, categorias e avaliações.

Também foi feita a separação conceitual entre receita e frete. A receita do dashboard foi calculada a partir do valor dos produtos (`price`). O frete foi mantido como indicador próprio (`freight_value`), pois misturar frete com receita poderia inflar artificialmente o faturamento.

## 3.3 Redução

A redução foi aplicada de forma analítica, por meio dos filtros interativos do dashboard:

- período da compra;
- estado do cliente;
- categoria;
- status do pedido;
- forma de pagamento;
- faixa de avaliação.

No painel, o status padrão utilizado é `delivered`, pois pedidos entregues possuem maior coerência para análise de prazo, atraso e avaliação. Pedidos cancelados, indisponíveis ou ainda em processamento podem ser selecionados quando a equipe quiser investigar outros comportamentos, mas não são o foco do diagnóstico logístico principal.

---

# 4. Dashboard Interativo

O painel foi desenvolvido em **Python**, utilizando **Streamlit** para a interface e **Plotly** para os gráficos interativos. A escolha dessa combinação permite que o usuário aplique múltiplos filtros ao mesmo tempo e observe a atualização automática dos indicadores.

O dashboard possui os seguintes filtros combinados:

- período da compra;
- UF do cliente;
- categoria do produto;
- status do pedido;
- forma de pagamento;
- faixa de avaliação.

Ao modificar qualquer filtro, todos os KPIs e gráficos são recalculados. Portanto, o painel não é um conjunto de gráficos estáticos, mas sim uma ferramenta de exploração de dados.

## Indicadores principais exibidos

Com o filtro padrão de pedidos entregues, o painel mostra aproximadamente:

- **Pedidos:** 96.478;
- **Ticket médio:** R$ 137,66;
- **Frete médio:** R$ 19,98;
- **Atraso médio real:** 0,69 dia;
- **Avaliação média:** 4,07 de 5;
- **Taxa de atraso:** aproximadamente 6,58% dos pedidos entregues.

Esses indicadores permitem uma leitura executiva da operação. A equipe pode iniciar a apresentação pelos KPIs e, em seguida, aprofundar a análise nos gráficos.

## Demonstração de uso dos filtros

Um exemplo de uso do dashboard é:

1. selecionar apenas pedidos entregues;
2. escolher um estado específico, como SP, RJ, MG ou BA;
3. selecionar uma categoria de alto faturamento;
4. ajustar o período para observar meses específicos;
5. comparar a avaliação média e o atraso real.

Esse processo permite responder perguntas como:

- A queda de avaliação está concentrada em alguma categoria?
- O atraso aparece mais em algum estado?
- O faturamento cresceu em determinado período?
- A categoria com maior receita também apresenta maior risco logístico?

---

# 5. Justificativa Visual

A escolha dos gráficos seguiu o tipo de pergunta que cada visual precisa responder.

## KPIs

Os cartões de KPI foram usados porque permitem leitura rápida dos principais indicadores da operação. Eles são adequados para gestores que precisam iniciar a análise por uma visão geral antes de investigar os detalhes.

## Gráfico de linha

O gráfico de linha foi usado para mostrar a evolução mensal do faturamento. Esse tipo de gráfico é adequado para tendências temporais, pois facilita a identificação de crescimento, queda e sazonalidade.

## Gráfico de barras por mês

O gráfico de barras de pedidos por mês permite comparar volumes mensais. Ele complementa o gráfico de linha porque mostra se o faturamento cresceu por aumento de pedidos ou por variação no ticket médio.

## Gráfico de barras por categoria

O gráfico de barras por categoria foi usado para comparação direta entre grupos. Ele permite identificar rapidamente quais categorias concentram maior receita e, portanto, merecem maior atenção comercial.

## Gráfico por UF

O gráfico por UF permite comparar a receita por estado e associar essa informação ao atraso médio. Essa visão apoia decisões logísticas regionais, pois estados com alta receita e atraso elevado devem ser priorizados.

## Gráfico de dispersão

O gráfico de dispersão entre dias de atraso e avaliação foi usado para investigar a relação entre logística e satisfação. Ele ajuda a visualizar se pedidos com mais atraso tendem a receber notas menores.

## Barras por forma de pagamento

O gráfico de forma de pagamento foi usado porque a comparação entre meios de pagamento é melhor representada por barras. A análise ajuda a entender a preferência dos clientes e pode orientar campanhas comerciais ou melhorias no checkout.

## Ranking de oportunidade

O ranking de oportunidade combina receita, atraso e avaliação. Esse visual é importante porque transforma os dados em prioridade de ação. Em vez de mostrar apenas o que aconteceu, ele indica onde o gestor deve olhar primeiro.

---

# 6. Análise de Diagnóstico e Plano de Ação

## 6.1 O Diagnóstico

A principal oportunidade identificada é a existência de categorias e regiões que combinam **alto faturamento**, **risco de atraso** e **avaliação do cliente abaixo do ideal**.

A análise mostra que a operação tem avaliação média positiva, em torno de 4,07 de 5, e a maior parte dos pedidos é entregue dentro ou antes do prazo. Porém, existe um grupo menor de pedidos atrasados que merece atenção. O atraso médio real geral é baixo, cerca de 0,69 dia, mas entre os pedidos que realmente atrasam a média é muito maior, aproximadamente 10,49 dias. Isso indica que o problema não está distribuído igualmente em toda a base: ele aparece de forma concentrada em certos casos.

A pergunta de diagnóstico escolhida para a apresentação é:

**Por que determinadas categorias de alto faturamento apresentam risco de pior avaliação quando há atraso de entrega em estados específicos?**

Essa pergunta é relevante porque une três dimensões de negócio:

- impacto financeiro, medido pelo faturamento;
- impacto operacional, medido pelo atraso;
- impacto na experiência do cliente, medido pela avaliação.

Durante a apresentação, a equipe pode demonstrar o diagnóstico aplicando os filtros do painel:

1. manter apenas pedidos entregues;
2. selecionar categorias de maior faturamento;
3. observar a avaliação média;
4. verificar o atraso médio por UF;
5. analisar o gráfico de dispersão entre atraso e nota.

Se uma categoria possui alto faturamento, atraso acima da média e avaliações menores, ela deve ser tratada como prioridade gerencial.

## 6.2 A Prescrição

Com base no dashboard, a ação prática recomendada é priorizar melhorias logísticas nas categorias e estados que aparecem no ranking de oportunidade.

As ações recomendadas são:

- revisar o prazo prometido nas regiões com maior atraso;
- negociar SLA com transportadoras nos estados críticos;
- acompanhar de forma preventiva os pedidos de categorias com alto faturamento;
- criar alertas para pedidos próximos da data estimada de entrega;
- oferecer cupom ou frete grátis em compras futuras para clientes afetados por atrasos relevantes;
- ajustar campanhas comerciais para não estimular categorias ou regiões que a logística não consegue atender bem no período;
- avaliar vendedores com recorrência de atraso em categorias estratégicas.

Uma ação gerencial objetiva seria:

**Criar uma campanha de recuperação para clientes de categorias de alto faturamento que tiveram atraso superior a 5 dias, oferecendo cupom de recompra ou frete grátis, enquanto a equipe logística revisa transportadoras e prazos prometidos nos estados com maior incidência de atraso.**

Essa prescrição é justificada porque atua sobre o ponto de maior impacto: clientes que compraram produtos financeiramente relevantes, tiveram experiência logística ruim e podem deixar de recomprar ou avaliar mal a plataforma.

---

# Conclusão

O painel desenvolvido transforma a base pública da Olist em uma ferramenta de Business Intelligence capaz de apoiar decisões comerciais e operacionais. A análise descritiva mostra não apenas o volume de vendas, mas também a relação entre faturamento, entrega, frete, região, pagamento e satisfação.

A principal contribuição do dashboard é permitir que a equipe investigue problemas de forma interativa. Em vez de apresentar apenas gráficos isolados, o painel permite combinar filtros e responder perguntas de negócio em tempo real.

Assim, a análise permite melhor tomada de decisão porque mostra:

- onde está o maior faturamento;
- quais categorias merecem prioridade;
- quais estados possuem maior impacto;
- como atrasos afetam a experiência;
- onde existe oportunidade de ação prática.

O resultado final é um painel de BI interativo que transforma dados brutos em informação gerencial, diagnóstico e plano de ação.
