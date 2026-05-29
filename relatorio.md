# Relatorio do Painel BI Interativo

## Capa

**Curso:** preencher com o nome do curso  
**Disciplina:** Business Intelligence / Analise de Dados  
**Professor:** preencher com o nome do professor  
**Equipe:** preencher com os nomes dos integrantes  
**Tema:** Dashboard BI Interativo com a base Brazilian E-Commerce Public Dataset by Olist

> "A mente que se abre a uma nova ideia jamais voltara ao seu tamanho original." - Albert Einstein

## 1. Definicao do Problema

A dor de negocio analisada e entender como vendas, logistica e satisfacao se relacionam no e-commerce brasileiro. Gestores precisam decidir onde investir em melhoria operacional, quais categorias merecem atencao comercial e quais regioes apresentam maior impacto financeiro.

O dashboard apoia as seguintes decisoes:

- **KPIs gerais:** mostram faturamento, pedidos, ticket medio, frete medio, atraso medio e avaliacao media. A tomada de decisao possivel e avaliar rapidamente se a operacao filtrada esta saudavel.
- **Evolucao mensal:** mostra tendencia de faturamento e pedidos ao longo do tempo. A decisao e identificar sazonalidade, queda de demanda ou crescimento por periodo.
- **Categorias por faturamento:** compara categorias e mostra quais concentram receita. A decisao e priorizar estoque, marketing e negociacao com vendedores.
- **Receita por UF:** evidencia estados com maior participacao financeira e atraso medio. A decisao e priorizar regioes logisticas de maior impacto.
- **Atraso versus avaliacao:** mostra se atrasos reduzem a satisfacao. A decisao e agir sobre transporte e prazo prometido.
- **Forma de pagamento:** identifica os meios mais usados. A decisao e adaptar campanhas, parcelamento e experiencia de checkout.
- **Ranking de oportunidade:** combina receita, atraso e avaliacao baixa. A decisao e escolher onde uma acao gerencial tem maior retorno.

## 2. Metadados e Estrutura

Base: **Brazilian E-Commerce Public Dataset by Olist**.

Fonte principal: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

CSVs publicos usados pelo projeto: `https://raw.githubusercontent.com/Athospd/work-at-olist-data/master/datasets/`

Tabelas utilizadas:

- `olist_orders_dataset.csv`: `order_id`, `customer_id`, `order_status`, datas de compra, aprovacao, envio, entrega e entrega estimada.
- `olist_customers_dataset.csv`: `customer_id`, `customer_unique_id`, cidade e UF do cliente.
- `olist_order_items_dataset.csv`: `order_id`, `order_item_id`, `product_id`, `seller_id`, `price`, `freight_value`.
- `olist_products_dataset.csv`: `product_id`, categoria original do produto e atributos fisicos.
- `product_category_name_translation.csv`: traducao da categoria para ingles.
- `olist_order_payments_dataset.csv`: `order_id`, sequencia, tipo de pagamento, parcelas e valor pago.
- `olist_order_reviews_dataset.csv`: `order_id`, `review_score`, comentarios e datas da avaliacao.

Colunas criadas no pre-processamento:

- `delivery_delay_days`: diferenca em dias entre entrega real e entrega estimada.
- `late_delay_days`: dias de atraso real, considerando `0` quando a entrega ocorreu no prazo ou antes do prazo.
- `delivery_days`: tempo entre compra e entrega ao cliente.
- `purchase_month`: mes da compra.
- `is_late`: indica se o pedido foi entregue depois da data estimada.
- `category`: categoria padronizada para analise.
- `revenue`: valor de venda dos produtos.
- `total_order_value`: valor total pago no pedido.

## 3. Processo de Pre-processamento

### Limpeza

As datas foram convertidas para formato temporal. Valores ausentes em datas de entrega foram preservados quando o pedido nao tinha entrega registrada, evitando criar atrasos falsos. Categorias ausentes foram classificadas como `uncategorized`. Pagamentos ausentes foram marcados como `not_informed`. Duplicidades foram reduzidas nas chaves principais de itens e as tabelas foram integradas por `order_id`, `customer_id` e `product_id`.

### Transformacao

Foram criadas colunas de diferenca contra o prazo estimado, atraso real, tempo de entrega, mes da compra, indicador de atraso, receita e valor total do pedido. A metrica `late_delay_days` evita atraso negativo: entregas antecipadas entram como zero no KPI de atraso medio. A tabela de pagamentos foi agregada para o nivel do pedido, somando `payment_value` e combinando os tipos de pagamento quando o pedido usou mais de uma forma.

### Reducao

O dashboard permite reduzir a base de forma interativa por periodo, UF, categoria, status, forma de pagamento e nota de avaliacao. Para os rankings visuais, categorias com volume muito baixo podem ser removidas do diagnostico para evitar conclusoes baseadas em poucos pedidos.

## 4. Dashboard Interativo

O painel foi desenvolvido em Python com Streamlit e Plotly. Os filtros ficam na barra lateral e podem ser combinados:

- periodo da compra;
- UF do cliente;
- categoria;
- status do pedido;
- forma de pagamento;
- faixa de avaliacao.

Ao alterar qualquer filtro, todos os indicadores e graficos sao recalculados automaticamente. Isso caracteriza um painel de BI interativo, nao apenas um conjunto de graficos estaticos.

## 5. Justificativa Visual

- **Cartoes KPI:** adequados para indicadores executivos de leitura rapida.
- **Grafico de linha:** usado para tendencia temporal de faturamento, pois evidencia evolucao, sazonalidade e quedas.
- **Grafico de barras:** usado para comparar categorias, estados e formas de pagamento, facilitando rankings.
- **Dispersao:** usada para investigar relacao entre atraso e avaliacao, pois cada ponto representa uma observacao e ajuda a enxergar concentracoes.
- **Cores por nota ou atraso:** destacam risco operacional e satisfacao sem exigir leitura de tabela.
- **Tabela filtrada:** permite auditoria e rastreabilidade dos registros que sustentam os graficos.

## 6. Analise de Diagnostico e Plano de Acao

### O Diagnostico

Uma anomalia/oportunidade investigada e a existencia de categorias com alto faturamento, atraso elevado e avaliacao media baixa. Esse conjunto indica que a empresa esta ganhando receita em uma categoria importante, mas pode estar perdendo satisfacao e recompra por causa da experiencia logistica.

Exemplo de pergunta diagnostica para apresentar em sala:

**Por que uma categoria de alto faturamento apresenta nota baixa quando ha atraso de entrega em determinados estados?**

O dashboard permite responder filtrando por categoria, UF, status e periodo. A equipe pode observar se a nota cai nos pedidos atrasados, se o problema se concentra em algum estado e se o impacto aparece em meses especificos.

### A Prescricao

Com base no dashboard, o gestor deve priorizar as categorias e UFs que aparecem no ranking de oportunidade. As acoes recomendadas sao:

- revisar SLA e promessa de prazo nas regioes com maior atraso;
- negociar desempenho com transportadoras nos estados mais criticos;
- reforcar acompanhamento de pedidos de categorias com alto faturamento;
- criar campanha de recuperacao para clientes afetados por atraso;
- ajustar estoque e sellers prioritarios nas categorias com maior receita e pior avaliacao.

A decisao final deve buscar maior impacto financeiro e reputacional: agir primeiro onde ha alto faturamento, volume relevante de pedidos, atraso acima da media e avaliacao abaixo da media.
