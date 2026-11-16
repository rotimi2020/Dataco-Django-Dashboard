
from django import forms

from .models import SupplyChainRecord


class SupplyChainRecordForm(forms.ModelForm):

    class Meta:
        model = SupplyChainRecord

        fields = [
            "order_item_id",
            "order_id",
            "order_date",
            "shipping_date",
            "shipping_mode",
            "delivery_status",
            "late_delivery_risk",
            "product_name",
            "category_name",
            "department_name",
            "customer_segment",
            "market",
            "order_region",
            "order_country",
            "sales",
            "order_item_total",
            "order_profit_per_order",
            "order_item_quantity",
            "days_for_shipping_real",
            "days_for_shipment_scheduled",
        ]

        widgets = {
            "order_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "shipping_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "late_delivery_risk": forms.Select(
                choices=[
                    (True, "Yes"),
                    (False, "No"),
                ]
            ),
            "sales": forms.NumberInput(attrs={"step": "0.01"}),
            "order_item_total": forms.NumberInput(attrs={"step": "0.01"}),
            "order_profit_per_order": forms.NumberInput(attrs={"step": "0.01"}),
            "order_item_quantity": forms.NumberInput(attrs={"min": "1"}),
        }

        labels = {
            "order_item_id": "Order Item ID",
            "order_id": "Order ID",
            "order_date": "Order Date and Time",
            "shipping_date": "Shipping Date and Time",
            "shipping_mode": "Shipping Method",
            "delivery_status": "Delivery Status",
            "late_delivery_risk": "Late Delivery Risk",
            "product_name": "Product Name",
            "category_name": "Product Category",
            "department_name": "Department",
            "customer_segment": "Customer Segment",
            "market": "Market",
            "order_region": "Order Region",
            "order_country": "Order Country",
            "sales": "Sales Amount",
            "order_item_total": "Order Item Total",
            "order_profit_per_order": "Profit",
            "order_item_quantity": "Quantity",
            "days_for_shipping_real": "Actual Shipping Days",
            "days_for_shipment_scheduled": "Scheduled Shipping Days",
        }
