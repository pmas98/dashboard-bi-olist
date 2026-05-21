# Dashboard BI Olist

Dashboard interativo em Python para analise descritiva da base publica **Brazilian E-Commerce Public Dataset by Olist**.

## Base escolhida

Fonte principal: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

O projeto usa CSVs publicos espelhados no GitHub para facilitar a reproducao em sala:

`https://raw.githubusercontent.com/Athospd/work-at-olist-data/master/datasets/`

## Por que esta base

A base da Olist e adequada para BI porque possui varias dimensoes de negocio: pedidos, clientes, produtos, categorias, pagamentos, frete, prazo de entrega e avaliacoes. Isso permite analisar receita, comportamento regional, desempenho logistico e satisfacao do cliente em um mesmo painel.

## Como rodar

```powershell
python -m pip install -r requirements.txt
streamlit run dashboard.py
```

O Streamlit abrira o dashboard no navegador. Na primeira execucao, os CSVs sao baixados da fonte publica e armazenados em cache pelo proprio Streamlit.

## Verificacao

```powershell
python -m pytest tests/test_olist_etl.py -q
python -m py_compile dashboard.py src/olist_etl.py
```

## Arquivos

- `dashboard.py`: painel interativo com filtros e graficos.
- `src/olist_etl.py`: carregamento, limpeza, transformacao e metricas.
- `tests/test_olist_etl.py`: testes automatizados do pre-processamento.
- `relatorio.md`: relatorio academico seguindo o modelo solicitado.
