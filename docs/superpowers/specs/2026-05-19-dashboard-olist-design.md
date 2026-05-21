# Dashboard BI Olist Design

## Objetivo

Construir um dashboard interativo em Python para analise descritiva de pedidos de e-commerce da Olist no Brasil, apoiando decisoes sobre desempenho comercial, atraso logistico e satisfacao do cliente.

## Base de Dados

A base escolhida e a Brazilian E-Commerce Public Dataset by Olist, publicada no Kaggle e espelhada em CSV publico no GitHub. Ela contem pedidos entre 2016 e 2018, clientes, itens, produtos, pagamentos e avaliacoes.

## Problema de Negocio

Gestores precisam entender quais estados, categorias e periodos geram mais receita, onde ha atrasos de entrega e como esses atrasos afetam avaliacoes. O dashboard deve apoiar decisoes de priorizacao logistica, campanhas comerciais e melhoria de categorias com baixa satisfacao.

## Arquitetura

O projeto sera dividido em:

- `src/olist_etl.py`: carrega, integra, limpa e transforma os CSVs.
- `dashboard.py`: interface Streamlit com filtros combinados e graficos Plotly.
- `tests/test_olist_etl.py`: testes das transformacoes principais.
- `relatorio.md`: relatorio academico seguindo o roteiro pedido.
- `README.md`: instrucoes de execucao e apresentacao.

## Filtros e Graficos

Filtros combinados: periodo, UF do cliente, categoria, status, forma de pagamento e faixa de avaliacao.

Graficos:

- KPIs de receita, pedidos, ticket medio, frete medio, atraso medio e avaliacao media.
- Linha temporal de receita e pedidos.
- Barras por categoria.
- Barras por UF.
- Dispersao entre atraso e avaliacao.
- Barras de formas de pagamento.
- Ranking diagnostico de oportunidades por categoria.

## Pre-processamento

O ETL tratara datas, duplicidades, pagamentos agregados por pedido, atraso de entrega, tempo de entrega, receita total, categoria em portugues/ingles e registros sem entrega. Reducoes serao feitas por relevancia analitica, mantendo pedidos com data de compra e itens vinculados.

## Verificacao

Os testes cobrirao calculo de atraso, agregacao de pagamentos, criacao de receita total e aplicacao de filtros combinados.
