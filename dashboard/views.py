
import csv
from collections import Counter
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.shortcuts import render
from django.db.models import Sum, Count, Q, Avg, DecimalField, Value
from django.db.models.functions import Coalesce, TruncMonth

from .models import SupplyChainRecord


def read_csv_file(filename):
    path = Path(settings.BASE_DIR) / "data" / "forecasts" / filename

    with open(path, "r", encoding="latin1", newline="") as file:
        return list(csv.DictReader(file))


def home(request):
    money_field = DecimalField(max_digits=15, decimal_places=2)

    summary = SupplyChainRecord.objects.aggregate(
        total_sales=Coalesce(
            Sum("sales"), Value(Decimal("0.00")),
            output_field=money_field,
        ),
        total_profit=Coalesce(
            Sum("order_profit_per_order"), Value(Decimal("0.00")),
            output_field=money_field,
        ),
        total_orders=Count("order_id", distinct=True),
        total_items=Count("order_item_id"),
        late_items=Count(
            "order_item_id",
            filter=Q(delivery_status="Late delivery"),
        ),
    )

    total_items = summary["total_items"]

    late_delivery_rate = (
        summary["late_items"] / total_items * 100
        if total_items else 0
    )

    average_order_value = (
        summary["total_sales"] / summary["total_orders"]
        if summary["total_orders"] else Decimal("0.00")
    )

    monthly_sales = (
        SupplyChainRecord.objects
        .annotate(month=TruncMonth("order_date"))
        .values("month")
        .annotate(total_sales=Sum("sales"))
        .order_by("month")
    )

    context = {
        "summary": summary,
        "late_delivery_rate": late_delivery_rate,
        "average_order_value": average_order_value,
        "monthly_sales_labels": [
            item["month"].strftime("%b %Y")
            for item in monthly_sales
        ],
        "monthly_sales_values": [
            float(item["total_sales"])
            for item in monthly_sales
        ],
    }

    return render(request, "dashboard/home.html", context)


def logistics(request):
    total_items = SupplyChainRecord.objects.count()

    delivery_summary = SupplyChainRecord.objects.aggregate(
        late_items=Count(
            "order_item_id",
            filter=Q(delivery_status="Late delivery"),
        ),
        on_time_items=Count(
            "order_item_id",
            filter=Q(delivery_status="Shipping on time"),
        ),
        advance_items=Count(
            "order_item_id",
            filter=Q(delivery_status="Advance shipping"),
        ),
        average_actual_days=Avg("days_for_shipping_real"),
        average_scheduled_days=Avg("days_for_shipment_scheduled"),
    )

    late_items = delivery_summary["late_items"]
    on_time_items = delivery_summary["on_time_items"]
    advance_items = delivery_summary["advance_items"]

    late_rate = late_items / total_items * 100 if total_items else 0
    on_time_rate = on_time_items / total_items * 100 if total_items else 0
    advance_rate = advance_items / total_items * 100 if total_items else 0

    average_actual_days = delivery_summary["average_actual_days"] or 0
    average_scheduled_days = delivery_summary["average_scheduled_days"] or 0
    average_delay = average_actual_days - average_scheduled_days

    shipping_modes = (
        SupplyChainRecord.objects
        .values("shipping_mode")
        .annotate(
            item_count=Count("order_item_id"),
            average_days=Avg("days_for_shipping_real"),
        )
        .order_by("shipping_mode")
    )

    delivery_statuses = (
        SupplyChainRecord.objects
        .values("delivery_status")
        .annotate(item_count=Count("order_item_id"))
        .order_by("delivery_status")
    )

    context = {
        "total_items": total_items,
        "late_items": late_items,
        "on_time_items": on_time_items,
        "advance_items": advance_items,
        "late_rate": late_rate,
        "on_time_rate": on_time_rate,
        "advance_rate": advance_rate,
        "average_actual_days": average_actual_days,
        "average_scheduled_days": average_scheduled_days,
        "average_delay": average_delay,
        "shipping_mode_labels": [
            item["shipping_mode"] for item in shipping_modes
        ],
        "shipping_mode_counts": [
            item["item_count"] for item in shipping_modes
        ],
        "shipping_mode_days": [
            round(item["average_days"] or 0, 2)
            for item in shipping_modes
        ],
        "delivery_status_labels": [
            item["delivery_status"] for item in delivery_statuses
        ],
        "delivery_status_counts": [
            item["item_count"] for item in delivery_statuses
        ],
    }

    return render(request, "dashboard/logistics.html", context)


def supply_chain(request):
    money_field = DecimalField(max_digits=15, decimal_places=2)

    summary = SupplyChainRecord.objects.aggregate(
        total_sales=Coalesce(
            Sum("sales"), Value(Decimal("0.00")),
            output_field=money_field,
        ),
        total_profit=Coalesce(
            Sum("order_profit_per_order"), Value(Decimal("0.00")),
            output_field=money_field,
        ),
        total_orders=Count("order_id", distinct=True),
        total_products=Count("product_name", distinct=True),
        total_quantity=Coalesce(Sum("order_item_quantity"), Value(0)),
    )

    categories = (
        SupplyChainRecord.objects
        .values("category_name")
        .annotate(
            sales=Sum("sales"),
            profit=Sum("order_profit_per_order"),
            item_count=Count("order_item_id"),
        )
        .order_by("-sales")[:10]
    )

    markets = (
        SupplyChainRecord.objects
        .values("market")
        .annotate(
            sales=Sum("sales"),
            profit=Sum("order_profit_per_order"),
        )
        .order_by("-sales")
    )

    segments = (
        SupplyChainRecord.objects
        .values("customer_segment")
        .annotate(
            sales=Sum("sales"),
            item_count=Count("order_item_id"),
        )
        .order_by("-sales")
    )

    departments = (
        SupplyChainRecord.objects
        .values("department_name")
        .annotate(
            sales=Sum("sales"),
            profit=Sum("order_profit_per_order"),
        )
        .order_by("-sales")
    )

    context = {
        "summary": summary,
        "category_labels": [
            item["category_name"] for item in categories
        ],
        "category_sales": [
            float(item["sales"] or 0) for item in categories
        ],
        "category_profit": [
            float(item["profit"] or 0) for item in categories
        ],
        "market_labels": [
            item["market"] for item in markets
        ],
        "market_sales": [
            float(item["sales"] or 0) for item in markets
        ],
        "market_profit": [
            float(item["profit"] or 0) for item in markets
        ],
        "segment_labels": [
            item["customer_segment"] for item in segments
        ],
        "segment_sales": [
            float(item["sales"] or 0) for item in segments
        ],
        "department_labels": [
            item["department_name"] for item in departments
        ],
        "department_sales": [
            float(item["sales"] or 0) for item in departments
        ],
        "department_profit": [
            float(item["profit"] or 0) for item in departments
        ],
    }

    return render(request, "dashboard/supply_chain.html", context)


def delivery_risk(request):
    rows = read_csv_file("Late_Delivery_Predictions.csv")

    total = 0
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    actual_late = 0
    actual_not_late = 0
    predicted_late = 0
    predicted_not_late = 0

    confidence_groups = Counter()
    prediction_by_shipping = Counter()

    for row in rows:
        actual = int(row["Late_delivery_risk"])
        predicted = int(row["Prediction (Late_delivery_risk)"])
        confidence = float(
            row["Prediction (Late_delivery_risk) (Confidence)"]
        )

        total += 1

        if actual == 1:
            actual_late += 1
        else:
            actual_not_late += 1

        if predicted == 1:
            predicted_late += 1
        else:
            predicted_not_late += 1

        if actual == 1 and predicted == 1:
            true_positive += 1
        elif actual == 0 and predicted == 0:
            true_negative += 1
        elif actual == 0 and predicted == 1:
            false_positive += 1
        else:
            false_negative += 1

        if confidence < 0.60:
            confidence_groups["Low"] += 1
        elif confidence < 0.80:
            confidence_groups["Medium"] += 1
        else:
            confidence_groups["High"] += 1

        shipping_mode = row.get("Shipping Mode", "Unknown")
        prediction_by_shipping[shipping_mode] += predicted

    accuracy = (
        (true_positive + true_negative) / total * 100
        if total else 0
    )

    precision = (
        true_positive / (true_positive + false_positive) * 100
        if true_positive + false_positive else 0
    )

    recall = (
        true_positive / (true_positive + false_negative) * 100
        if true_positive + false_negative else 0
    )

    f1_score = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    context = {
        "total_predictions": total,
        "actual_late": actual_late,
        "actual_not_late": actual_not_late,
        "predicted_late": predicted_late,
        "predicted_not_late": predicted_not_late,
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "confidence_labels": ["Low", "Medium", "High"],
        "confidence_values": [
            confidence_groups["Low"],
            confidence_groups["Medium"],
            confidence_groups["High"],
        ],
        "shipping_labels": list(prediction_by_shipping.keys()),
        "shipping_predictions": list(prediction_by_shipping.values()),
    }

    return render(request, "dashboard/delivery_risk.html", context)


def order_forecast(request):
    forecast_rows = read_csv_file("Order_Volume_Forecast.csv")
    evaluation_rows = read_csv_file("Order_Volume_Model_Evaluation.csv")
    metric_rows = read_csv_file("Order_Volume_Model_Metrics.csv")

    forecast_labels = []
    arima_111_values = []
    arima_121_values = []

    for row in forecast_rows:
        forecast_labels.append(row["Forecast_Month"][:7])
        arima_111_values.append(
            round(float(row["Monthly_Order_Volume _Arima_1_1_1"]), 2)
        )
        arima_121_values.append(
            round(float(row["Monthly_Order_Volume _Arima_1_2_1"]), 2)
        )

    evaluation_labels = []
    evaluation_actual = []
    evaluation_111 = []
    evaluation_121 = []

    for row in evaluation_rows:
        model = row["Model"]
        month = f'{row["Year"]}-{int(row["Month"]):02d}'

        if month not in evaluation_labels:
            evaluation_labels.append(month)
            evaluation_actual.append(float(row["Actual_Volume"]))
            evaluation_111.append(None)
            evaluation_121.append(None)

        index = evaluation_labels.index(month)

        if model == "ARIMA(1,1,1)":
            evaluation_111[index] = round(
                float(row["Monthly_Order_Volume"]), 2
            )
        elif model == "ARIMA(1,2,1)":
            evaluation_121[index] = round(
                float(row["Monthly_Order_Volume"]), 2
            )

    metrics = {
        row["Model"]: row
        for row in metric_rows
    }

    model_111 = metrics.get("ARIMA(1,1,1)", {})
    model_121 = metrics.get("ARIMA(1,2,1)", {})

    context = {
        "forecast_labels": forecast_labels,
        "arima_111_values": arima_111_values,
        "arima_121_values": arima_121_values,
        "evaluation_labels": evaluation_labels,
        "evaluation_actual": evaluation_actual,
        "evaluation_111": evaluation_111,
        "evaluation_121": evaluation_121,
        "model_111_mae": float(model_111.get("MAE", 0)),
        "model_111_mape": float(model_111.get("MAPE", 0)),
        "model_111_rmse": float(model_111.get("RMSE", 0)),
        "model_121_mae": float(model_121.get("MAE", 0)),
        "model_121_mape": float(model_121.get("MAPE", 0)),
        "model_121_rmse": float(model_121.get("RMSE", 0)),
    }

    return render(request, "dashboard/order_forecast.html", context)
