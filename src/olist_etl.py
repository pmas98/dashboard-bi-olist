from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import pandas as pd


BASE_URL = "https://raw.githubusercontent.com/Athospd/work-at-olist-data/master/datasets"

DATASET_URLS = {
    "orders": f"{BASE_URL}/olist_orders_dataset.csv",
    "customers": f"{BASE_URL}/olist_customers_dataset.csv",
    "items": f"{BASE_URL}/olist_order_items_dataset.csv",
    "products": f"{BASE_URL}/olist_products_dataset.csv",
    "payments": f"{BASE_URL}/olist_order_payments_dataset.csv",
    "reviews": f"{BASE_URL}/olist_order_reviews_dataset.csv",
    "category_translation": f"{BASE_URL}/product_category_name_translation.csv",
}


DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


@dataclass(frozen=True)
class DashboardMetrics:
    revenue: float
    orders: int
    average_ticket: float
    average_freight: float
    average_delay_days: float
    average_late_only_delay_days: float
    average_review_score: float


def load_source_frames(urls: Mapping[str, str] | None = None) -> dict[str, pd.DataFrame]:
    source_urls = urls or DATASET_URLS
    return {name: pd.read_csv(url, low_memory=False) for name, url in source_urls.items()}


def compute_delivery_metrics(orders: pd.DataFrame) -> pd.DataFrame:
    result = orders.copy()
    for column in DATE_COLUMNS:
        if column in result.columns:
            result[column] = pd.to_datetime(result[column], errors="coerce")

    delivered = result["order_delivered_customer_date"]
    estimated = result["order_estimated_delivery_date"]
    purchased = result["order_purchase_timestamp"]

    result["delivery_delay_days"] = (delivered - estimated).dt.days
    result["late_delay_days"] = result["delivery_delay_days"].clip(lower=0)
    result["delivery_days"] = (delivered - purchased).dt.days
    result["purchase_month"] = purchased.dt.to_period("M").dt.to_timestamp()
    result["purchase_date"] = purchased.dt.date
    result["is_late"] = result["delivery_delay_days"] > 0
    return result


def aggregate_payments(payments: pd.DataFrame) -> pd.DataFrame:
    payment_order = (
        payments.sort_values(["order_id", "payment_type"])
        .groupby("order_id", as_index=False)
        .agg(
            payment_value=("payment_value", "sum"),
            payment_type=("payment_type", lambda values: " + ".join(sorted(set(values)))),
        )
    )
    return payment_order


def build_analytics_model(frames: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    orders = compute_delivery_metrics(frames["orders"])
    payments = aggregate_payments(frames["payments"])

    item_columns = ["order_id", "order_item_id", "product_id", "seller_id", "price", "freight_value"]
    items = frames["items"][item_columns].drop_duplicates()

    model = (
        items.merge(orders, on="order_id", how="left")
        .merge(frames["customers"], on="customer_id", how="left")
        .merge(frames["products"], on="product_id", how="left")
        .merge(frames["category_translation"], on="product_category_name", how="left")
        .merge(payments, on="order_id", how="left")
        .merge(frames["reviews"][["order_id", "review_score"]], on="order_id", how="left")
    )

    model["category"] = model["product_category_name_english"].fillna(model["product_category_name"])
    model["category"] = model["category"].fillna("uncategorized")
    model["revenue"] = model["price"].fillna(0)
    model["total_order_value"] = model["payment_value"].fillna(
        model["price"].fillna(0) + model["freight_value"].fillna(0)
    )
    model["customer_state"] = model["customer_state"].fillna("N/I")
    model["payment_type"] = model["payment_type"].fillna("not_informed")
    model["review_score"] = pd.to_numeric(model["review_score"], errors="coerce")
    return model


def apply_filters(
    model: pd.DataFrame,
    date_range: tuple[pd.Timestamp, pd.Timestamp] | None = None,
    states: list[str] | None = None,
    categories: list[str] | None = None,
    statuses: list[str] | None = None,
    payment_types: list[str] | None = None,
    review_range: tuple[int, int] | None = None,
) -> pd.DataFrame:
    filtered = model.copy()

    if date_range is not None:
        start, end = date_range
        purchased = pd.to_datetime(filtered["order_purchase_timestamp"], errors="coerce")
        filtered = filtered[(purchased >= start) & (purchased <= end)]
    if states:
        filtered = filtered[filtered["customer_state"].isin(states)]
    if categories:
        filtered = filtered[filtered["category"].isin(categories)]
    if statuses:
        filtered = filtered[filtered["order_status"].isin(statuses)]
    if payment_types:
        filtered = filtered[filtered["payment_type"].isin(payment_types)]
    if review_range is not None:
        minimum, maximum = review_range
        filtered = filtered[filtered["review_score"].between(minimum, maximum, inclusive="both")]

    return filtered


def build_delivery_review_distribution(model: pd.DataFrame) -> pd.DataFrame:
    required_columns = ["order_id", "delivery_delay_days", "review_score"]
    base = model.dropna(subset=required_columns).drop_duplicates("order_id").copy()
    result_columns = ["delivery_band", "review_score", "orders", "average_delivery_gap"]
    if base.empty:
        return pd.DataFrame(columns=result_columns)

    labels = [
        "15+ dias antes",
        "6 a 14 dias antes",
        "No prazo",
        "1 a 2 dias depois",
        "3 a 5 dias depois",
        "6+ dias depois",
    ]
    base["delivery_band"] = pd.cut(
        base["delivery_delay_days"],
        bins=[float("-inf"), -15, -6, 0, 2, 5, float("inf")],
        labels=labels,
    )

    return (
        base.groupby(["delivery_band", "review_score"], observed=True, as_index=False)
        .agg(
            orders=("order_id", "nunique"),
            average_delivery_gap=("delivery_delay_days", "mean"),
        )
        .sort_values(["delivery_band", "review_score"])
    )


def calculate_metrics(model: pd.DataFrame) -> DashboardMetrics:
    order_count = model["order_id"].nunique()
    revenue = float(model["revenue"].sum())
    late_orders = model[model["late_delay_days"] > 0]
    return DashboardMetrics(
        revenue=revenue,
        orders=int(order_count),
        average_ticket=float(revenue / order_count) if order_count else 0.0,
        average_freight=float(model["freight_value"].mean()) if not model.empty else 0.0,
        average_delay_days=float(model["late_delay_days"].mean()) if not model.empty else 0.0,
        average_late_only_delay_days=float(late_orders["late_delay_days"].mean()) if not late_orders.empty else 0.0,
        average_review_score=float(model["review_score"].mean()) if not model.empty else 0.0,
    )


def category_opportunity(model: pd.DataFrame, minimum_orders: int = 30) -> pd.DataFrame:
    grouped = (
        model.groupby(["customer_state", "category"], as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
            average_review=("review_score", "mean"),
            average_delay=("late_delay_days", "mean"),
            late_rate=("is_late", "mean"),
        )
        .query("orders >= @minimum_orders")
    )
    if grouped.empty:
        return grouped

    grouped["segment"] = grouped["customer_state"] + " + " + grouped["category"]
    grouped["score_revenue_rank"] = grouped["revenue"].rank(pct=True)
    grouped["score_orders_rank"] = grouped["orders"].rank(pct=True)
    grouped["score_delay_rank"] = grouped["average_delay"].fillna(0).rank(pct=True)
    grouped["score_late_rate_rank"] = grouped["late_rate"].fillna(0).rank(pct=True)
    grouped["score_low_review_penalty"] = 1 - grouped["average_review"].fillna(5) / 5
    grouped["opportunity_score"] = grouped[
        [
            "score_revenue_rank",
            "score_orders_rank",
            "score_delay_rank",
            "score_late_rate_rank",
            "score_low_review_penalty",
        ]
    ].sum(axis=1)
    return grouped.sort_values("opportunity_score", ascending=False)
