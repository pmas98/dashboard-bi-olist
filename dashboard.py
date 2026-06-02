from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.olist_etl import (
    apply_filters,
    build_analytics_model,
    calculate_metrics,
    category_opportunity,
    load_source_frames,
)


st.set_page_config(
    page_title="BI Olist - E-commerce Brasileiro",
    page_icon="BI",
    layout="wide",
)


@st.cache_data(show_spinner="Baixando e preparando a base publica da Olist...")
def load_model() -> pd.DataFrame:
    frames = load_source_frames()
    return build_analytics_model(frames)


def brl(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def number(value: float, suffix: str = "") -> str:
    return f"{value:,.2f}{suffix}".replace(",", "X").replace(".", ",").replace("X", ".")


model = load_model()

st.title("Painel BI Interativo - Olist Brazilian E-commerce")
st.caption(
    "Base publica de pedidos de e-commerce no Brasil. Analise descritiva de receita, "
    "logistica e satisfacao do cliente."
)

with st.sidebar:
    st.header("Filtros combinados")

    min_date = pd.to_datetime(model["order_purchase_timestamp"]).min().date()
    max_date = pd.to_datetime(model["order_purchase_timestamp"]).max().date()
    selected_dates = st.date_input(
        "Periodo da compra",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if len(selected_dates) == 2:
        date_range = (
            pd.Timestamp(selected_dates[0]),
            pd.Timestamp(selected_dates[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1),
        )
    else:
        date_range = (pd.Timestamp(min_date), pd.Timestamp(max_date))

    states = st.multiselect(
        "UF do cliente",
        sorted(model["customer_state"].dropna().unique()),
        default=[],
    )
    categories = st.multiselect(
        "Categoria",
        sorted(model["category"].dropna().unique()),
        default=[],
    )
    statuses = st.multiselect(
        "Status do pedido",
        sorted(model["order_status"].dropna().unique()),
        default=["delivered"] if "delivered" in set(model["order_status"]) else [],
    )
    payment_types = st.multiselect(
        "Forma de pagamento",
        sorted(model["payment_type"].dropna().unique()),
        default=[],
    )
    review_range = st.slider("Faixa de avaliacao", 1, 5, (1, 5))

filtered = apply_filters(
    model,
    date_range=date_range,
    states=states,
    categories=categories,
    statuses=statuses,
    payment_types=payment_types,
    review_range=review_range,
)

metrics = calculate_metrics(filtered)

if filtered.empty:
    st.warning("Nenhum registro encontrado com a combinacao atual de filtros.")
    st.stop()

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6, kpi7 = st.columns(7)
kpi1.metric("Faturamento", brl(metrics.revenue))
kpi2.metric("Pedidos", f"{metrics.orders:,}".replace(",", "."))
kpi3.metric("Ticket medio", brl(metrics.average_ticket))
kpi4.metric("Frete medio", brl(metrics.average_freight))
kpi5.metric(
    "Atraso geral",
    number(metrics.average_delay_days, " dias"),
    help="Media calculada sobre todos os pedidos filtrados; entregas no prazo ou antecipadas entram como zero.",
)
kpi6.metric(
    "Atraso atrasados",
    number(metrics.average_late_only_delay_days, " dias"),
    help="Media calculada apenas entre os pedidos que passaram da data estimada de entrega.",
)
kpi7.metric("Avaliacao media", number(metrics.average_review_score, "/5"))

st.divider()

monthly = (
    filtered.groupby("purchase_month", as_index=False)
    .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
    .sort_values("purchase_month")
)

left, right = st.columns((1.4, 1))
with left:
    fig = px.line(
        monthly,
        x="purchase_month",
        y="revenue",
        markers=True,
        title="Evolucao mensal do faturamento",
        labels={"purchase_month": "Mes", "revenue": "Faturamento"},
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.bar(
        monthly,
        x="purchase_month",
        y="orders",
        title="Pedidos por mes",
        labels={"purchase_month": "Mes", "orders": "Pedidos"},
    )
    st.plotly_chart(fig, use_container_width=True)

category_rank = (
    filtered.groupby("category", as_index=False)
    .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"), review=("review_score", "mean"))
    .sort_values("revenue", ascending=False)
    .head(15)
)

state_rank = (
    filtered.groupby("customer_state", as_index=False)
    .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"), delay=("late_delay_days", "mean"))
    .sort_values("revenue", ascending=False)
)

left, right = st.columns(2)
with left:
    fig = px.bar(
        category_rank.sort_values("revenue"),
        x="revenue",
        y="category",
        orientation="h",
        color="review",
        title="Top categorias por faturamento",
        labels={"revenue": "Faturamento", "category": "Categoria", "review": "Nota media"},
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.bar(
        state_rank.head(15),
        x="customer_state",
        y="revenue",
        color="delay",
        title="Receita por UF e atraso medio",
        labels={"customer_state": "UF", "revenue": "Faturamento", "delay": "Atraso medio"},
    )
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    sample = filtered.dropna(subset=["late_delay_days", "review_score"])
    if len(sample) > 5000:
        sample = sample.sample(5000, random_state=42)
    fig = px.scatter(
        sample,
        x="late_delay_days",
        y="review_score",
        color="customer_state",
        hover_data=["category", "order_status", "revenue"],
        title="Relacao entre atraso de entrega e avaliacao",
        labels={"late_delay_days": "Dias de atraso", "review_score": "Avaliacao"},
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    payment = (
        filtered.groupby("payment_type", as_index=False)
        .agg(orders=("order_id", "nunique"), value=("total_order_value", "sum"))
        .sort_values("orders", ascending=False)
        .head(12)
    )
    fig = px.bar(
        payment,
        x="orders",
        y="payment_type",
        orientation="h",
        title="Pedidos por forma de pagamento",
        labels={"orders": "Pedidos", "payment_type": "Pagamento"},
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Diagnostico e plano de acao")
opportunity = category_opportunity(filtered, minimum_orders=max(5, int(metrics.orders * 0.005)))

if opportunity.empty:
    st.info("A combinacao de filtros atual nao tem volume suficiente para ranking diagnostico.")
else:
    top = opportunity.iloc[0]
    col_a, col_b = st.columns((1, 1))
    with col_a:
        st.markdown(
            f"""
            **Oportunidade detectada:** `{top['category']}` combina alto faturamento
            com risco de experiencia ruim.

            - Pedidos: {int(top['orders'])}
            - Faturamento: {brl(float(top['revenue']))}
            - Avaliacao media: {number(float(top['average_review']), '/5')}
            - Taxa de atraso: {number(float(top['late_rate'] * 100), '%')}
            """
        )
    with col_b:
        st.markdown(
            """
            **Acao sugerida:** priorizar a categoria/UF filtrada com revisao de SLA,
            acompanhamento de transportadoras e campanha seletiva de recuperacao
            quando houver atraso. A decisao deve mirar categorias com receita alta,
            atraso elevado e nota baixa, pois elas concentram impacto financeiro e
            reputacional.
            """
        )

    fig = px.bar(
        opportunity.head(10).sort_values("opportunity_score"),
        x="opportunity_score",
        y="category",
        orientation="h",
        color="average_review",
        title="Ranking de oportunidade por categoria",
        labels={
            "opportunity_score": "Score de oportunidade",
            "category": "Categoria",
            "average_review": "Nota media",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

with st.expander("Ver dados filtrados"):
    st.dataframe(
        filtered[
            [
                "order_id",
                "order_purchase_timestamp",
                "customer_state",
                "category",
                "order_status",
                "payment_type",
                "revenue",
                "freight_value",
                "late_delay_days",
                "delivery_delay_days",
                "review_score",
            ]
        ].head(1000),
        use_container_width=True,
    )
