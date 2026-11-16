import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from dashboard.models import SupplyChainRecord


class Command(BaseCommand):
    help = "Import DataCo supply-chain records from the included CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Replace existing records with the records in the CSV file",
        )

    def handle(self, *args, **options):
        file_path = (
            Path(settings.BASE_DIR)
            / "data"
            / "processed"
            / "DataCo_SupplyChain.csv"
        )

        if not file_path.is_file():
            raise CommandError(f"DataCo source CSV was not found: {file_path}")

        if SupplyChainRecord.objects.exists() and not options["replace"]:
            raise CommandError(
                "Records already exist. Run with --replace only if you "
                "intend to replace the existing dashboard records."
            )

        batch_size = 2000
        batch = []
        imported = 0

        def parse_datetime(value):
            parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M")
            if timezone.is_naive(parsed):
                parsed = timezone.make_aware(
                    parsed, timezone.get_default_timezone()
                )
            return parsed

        def make_record(row, line_number):
            try:
                return SupplyChainRecord(
                    order_item_id=int(row["Order Item Id"]),
                    order_id=int(row["Order Id"]),
                    order_date=parse_datetime(row["Order_Date"]),
                    shipping_date=parse_datetime(row["Shipping_Date"]),
                    shipping_mode=row["Shipping Mode"],
                    delivery_status=row["Delivery Status"],
                    late_delivery_risk=row["Late_delivery_risk"] == "1",
                    product_name=row["Product Name"],
                    category_name=row["Category Name"],
                    department_name=row["Department Name"],
                    customer_segment=row["Customer Segment"],
                    market=row["Market"],
                    order_region=row["Order Region"],
                    order_country=row["Order Country"],
                    sales=Decimal(row["Sales"]),
                    order_item_total=Decimal(row["Order Item Total"]),
                    order_profit_per_order=Decimal(
                        row["Order Profit Per Order"]
                    ),
                    order_item_quantity=int(row["Order Item Quantity"]),
                    days_for_shipping_real=int(
                        row["Days for shipping (real)"]
                    ),
                    days_for_shipment_scheduled=int(
                        row["Days for shipment (scheduled)"]
                    ),
                )
            except (KeyError, ValueError, InvalidOperation) as exc:
                raise CommandError(
                    f"Invalid value in source CSV at line {line_number}: {exc}"
                ) from exc

        try:
            # The delete and the import are one transaction. If parsing or
            # insertion fails, the old data is restored automatically.
            with transaction.atomic():
                if options["replace"]:
                    self.stdout.write("Replacing existing DataCo records...")
                    SupplyChainRecord.objects.all().delete()

                with file_path.open(
                    "r", encoding="latin1", newline=""
                ) as csv_file:
                    reader = csv.DictReader(csv_file)

                    required_columns = {
                        "Order Item Id",
                        "Order Id",
                        "Order_Date",
                        "Shipping_Date",
                        "Shipping Mode",
                        "Delivery Status",
                        "Late_delivery_risk",
                        "Product Name",
                        "Category Name",
                        "Department Name",
                        "Customer Segment",
                        "Market",
                        "Order Region",
                        "Order Country",
                        "Sales",
                        "Order Item Total",
                        "Order Profit Per Order",
                        "Order Item Quantity",
                        "Days for shipping (real)",
                        "Days for shipment (scheduled)",
                    }

                    missing_columns = required_columns - set(
                        reader.fieldnames or []
                    )
                    if missing_columns:
                        raise CommandError(
                            "The source CSV is missing required columns: "
                            + ", ".join(sorted(missing_columns))
                        )

                    for line_number, row in enumerate(reader, start=2):
                        batch.append(make_record(row, line_number))

                        if len(batch) >= batch_size:
                            SupplyChainRecord.objects.bulk_create(
                                batch, batch_size=batch_size
                            )
                            imported += len(batch)
                            batch.clear()

                    if batch:
                        SupplyChainRecord.objects.bulk_create(
                            batch, batch_size=batch_size
                        )
                        imported += len(batch)

        except OSError as exc:
            raise CommandError(f"Could not read the DataCo CSV: {exc}") from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {imported:,} DataCo records."
            )
        )
