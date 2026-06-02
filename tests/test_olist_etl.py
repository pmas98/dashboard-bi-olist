import pandas as pd

from src.olist_etl import (
    aggregate_payments,
    apply_filters,
    build_analytics_model,
    calculate_metrics,
    category_opportunity,
    compute_delivery_metrics,
)


def test_compute_delivery_metrics_calculates_delay_days():
    orders = pd.DataFrame(
        {
            "order_id": ["a", "b", "c"],
            "order_purchase_timestamp": ["2018-01-01", "2018-01-02", "2018-01-03"],
            "order_delivered_customer_date": ["2018-01-05", "2018-01-08", None],
            "order_estimated_delivery_date": ["2018-01-04", "2018-01-10", "2018-01-09"],
        }
    )

    result = compute_delivery_metrics(orders)

    assert result.loc[result["order_id"] == "a", "delivery_delay_days"].iloc[0] == 1
    assert result.loc[result["order_id"] == "b", "delivery_delay_days"].iloc[0] == -2
    assert result.loc[result["order_id"] == "a", "late_delay_days"].iloc[0] == 1
    assert result.loc[result["order_id"] == "b", "late_delay_days"].iloc[0] == 0
    assert pd.isna(result.loc[result["order_id"] == "c", "delivery_delay_days"].iloc[0])
    assert result.loc[result["order_id"] == "a", "delivery_days"].iloc[0] == 4


def test_aggregate_payments_creates_order_level_payment_summary():
    payments = pd.DataFrame(
        {
            "order_id": ["a", "a", "b"],
            "payment_type": ["credit_card", "voucher", "boleto"],
            "payment_value": [100.0, 10.0, 50.0],
        }
    )

    result = aggregate_payments(payments)

    row_a = result[result["order_id"] == "a"].iloc[0]
    assert row_a["payment_value"] == 110.0
    assert row_a["payment_type"] == "credit_card + voucher"


def test_build_analytics_model_merges_tables_and_creates_business_columns():
    frames = sample_frames()

    result = build_analytics_model(frames)

    assert set(["revenue", "total_order_value", "customer_state", "category"]).issubset(result.columns)
    first = result[result["order_id"] == "a"].iloc[0]
    assert first["revenue"] == 120.0
    assert first["total_order_value"] == 130.0
    assert first["category"] == "health_beauty"
    assert first["customer_state"] == "SP"


def test_apply_filters_combines_period_state_category_status_payment_and_review():
    model = build_analytics_model(sample_frames())

    result = apply_filters(
        model,
        date_range=(pd.Timestamp("2018-01-01"), pd.Timestamp("2018-01-31")),
        states=["SP"],
        categories=["health_beauty"],
        statuses=["delivered"],
        payment_types=["credit_card + voucher"],
        review_range=(4, 5),
    )

    assert result["order_id"].tolist() == ["a"]


def test_calculate_metrics_uses_only_real_delay_for_average_delay():
    model = build_analytics_model(sample_frames())

    metrics = calculate_metrics(model)

    assert metrics.average_delay_days == 1 / 2
    assert metrics.average_late_only_delay_days == 1


def test_category_opportunity_keeps_state_category_segments_separate():
    model = pd.DataFrame(
        {
            "customer_state": ["RJ", "RJ", "SP"],
            "category": ["bed_bath_table", "bed_bath_table", "bed_bath_table"],
            "revenue": [100.0, 50.0, 200.0],
            "order_id": ["rj-1", "rj-2", "sp-1"],
            "review_score": [3, 4, 5],
            "late_delay_days": [2, 0, 0],
            "is_late": [True, False, False],
        }
    )

    result = category_opportunity(model, minimum_orders=1)

    bed_segments = result[result["category"] == "bed_bath_table"]
    assert sorted(bed_segments["customer_state"].tolist()) == ["RJ", "SP"]
    assert bed_segments.loc[bed_segments["customer_state"] == "RJ", "orders"].iloc[0] == 2


def test_category_opportunity_scores_volume_delay_late_rate_and_review():
    model = pd.DataFrame(
        {
            "customer_state": ["RJ", "RJ", "RJ", "RJ", "RJ", "RJ"],
            "category": [
                "bed_bath_table",
                "bed_bath_table",
                "bed_bath_table",
                "bed_bath_table",
                "watches_gifts",
                "watches_gifts",
            ],
            "revenue": [20.0, 20.0, 20.0, 20.0, 120.0, 80.0],
            "order_id": ["bed-1", "bed-2", "bed-3", "bed-4", "watch-1", "watch-2"],
            "review_score": [3.5, 3.5, 3.5, 3.5, 3.5, 3.5],
            "late_delay_days": [6.0, 6.0, 0.0, 0.0, 1.0, 0.0],
            "is_late": [True, True, False, False, True, False],
        }
    )

    result = category_opportunity(model, minimum_orders=1)

    assert result.iloc[0]["segment"] == "RJ + bed_bath_table"


def sample_frames():
    return {
        "orders": pd.DataFrame(
            {
                "order_id": ["a", "b"],
                "customer_id": ["c1", "c2"],
                "order_status": ["delivered", "delivered"],
                "order_purchase_timestamp": ["2018-01-10", "2018-02-10"],
                "order_delivered_customer_date": ["2018-01-15", "2018-02-18"],
                "order_estimated_delivery_date": ["2018-01-14", "2018-02-20"],
            }
        ),
        "customers": pd.DataFrame(
            {
                "customer_id": ["c1", "c2"],
                "customer_unique_id": ["u1", "u2"],
                "customer_city": ["sao paulo", "rio de janeiro"],
                "customer_state": ["SP", "RJ"],
            }
        ),
        "items": pd.DataFrame(
            {
                "order_id": ["a", "b"],
                "order_item_id": [1, 1],
                "product_id": ["p1", "p2"],
                "seller_id": ["s1", "s2"],
                "price": [120.0, 80.0],
                "freight_value": [10.0, 20.0],
            }
        ),
        "products": pd.DataFrame(
            {
                "product_id": ["p1", "p2"],
                "product_category_name": ["beleza_saude", "esporte_lazer"],
            }
        ),
        "payments": pd.DataFrame(
            {
                "order_id": ["a", "a", "b"],
                "payment_type": ["credit_card", "voucher", "boleto"],
                "payment_value": [120.0, 10.0, 100.0],
            }
        ),
        "reviews": pd.DataFrame(
            {
                "order_id": ["a", "b"],
                "review_score": [5, 2],
            }
        ),
        "category_translation": pd.DataFrame(
            {
                "product_category_name": ["beleza_saude", "esporte_lazer"],
                "product_category_name_english": ["health_beauty", "sports_leisure"],
            }
        ),
    }
