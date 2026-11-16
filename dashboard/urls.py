
from django.urls import path

from . import views
from . import records_views


urlpatterns = [
    # Existing dashboard pages
    path("", views.home, name="home"),
    path("logistics/", views.logistics, name="logistics"),
    path("supply-chain/", views.supply_chain, name="supply_chain"),
    path("delivery-risk/", views.delivery_risk, name="delivery_risk"),
    path("order-forecast/", views.order_forecast, name="order_forecast"),

    # Data Records page
    path(
        "data-records/",
        records_views.data_records,
        name="data_records",
    ),

    # Add a new record
    path(
        "data-records/add/",
        records_views.add_record,
        name="add_record",
    ),

    # Edit an existing record
    path(
        "data-records/edit/<int:order_item_id>/",
        records_views.edit_record,
        name="edit_record",
    ),

    # Delete an existing record
    path(
        "data-records/delete/<int:order_item_id>/",
        records_views.delete_record,
        name="delete_record",
    ),
]
