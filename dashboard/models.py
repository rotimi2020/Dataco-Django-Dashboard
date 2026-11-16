from django.db import models


class SupplyChainRecord(models.Model):
    order_item_id = models.BigIntegerField(unique=True, primary_key=True)
    order_id = models.BigIntegerField(db_index=True)

    order_date = models.DateTimeField()
    shipping_date = models.DateTimeField()

    shipping_mode = models.CharField(max_length=100)
    delivery_status = models.CharField(max_length=100)
    late_delivery_risk = models.BooleanField()

    product_name = models.CharField(max_length=255)
    category_name = models.CharField(max_length=150)
    department_name = models.CharField(max_length=150)

    customer_segment = models.CharField(max_length=100)
    market = models.CharField(max_length=100)
    order_region = models.CharField(max_length=150)
    order_country = models.CharField(max_length=150)

    sales = models.DecimalField(max_digits=15, decimal_places=2)
    order_item_total = models.DecimalField(max_digits=15, decimal_places=2)
    order_profit_per_order = models.DecimalField(max_digits=15, decimal_places=2)
    order_item_quantity = models.PositiveIntegerField()

    days_for_shipping_real = models.IntegerField()
    days_for_shipment_scheduled = models.IntegerField()

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f"Order Item {self.order_item_id}"

