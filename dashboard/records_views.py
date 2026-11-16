
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SupplyChainRecordForm
from .models import SupplyChainRecord


def staff_required(user):
    return user.is_authenticated and user.is_staff


def data_records(request):
    records = SupplyChainRecord.objects.all()

    search = request.GET.get("search", "").strip()
    if search:
        records = records.filter(
            Q(product_name__icontains=search)
            | Q(category_name__icontains=search)
            | Q(department_name__icontains=search)
            | Q(market__icontains=search)
            | Q(order_region__icontains=search)
            | Q(order_country__icontains=search)
            | Q(order_id__icontains=search)
            | Q(order_item_id__icontains=search)
        )

    shipping_mode = request.GET.get("shipping_mode", "").strip()
    if shipping_mode:
        records = records.filter(shipping_mode=shipping_mode)

    delivery_status = request.GET.get("delivery_status", "").strip()
    if delivery_status:
        records = records.filter(delivery_status=delivery_status)

    late_risk = request.GET.get("late_risk", "").strip()
    if late_risk == "yes":
        records = records.filter(late_delivery_risk=True)
    elif late_risk == "no":
        records = records.filter(late_delivery_risk=False)

    shipping_modes = (
        SupplyChainRecord.objects
        .values_list("shipping_mode", flat=True)
        .distinct()
        .order_by("shipping_mode")
    )

    delivery_statuses = (
        SupplyChainRecord.objects
        .values_list("delivery_status", flat=True)
        .distinct()
        .order_by("delivery_status")
    )

    paginator = Paginator(records, 25)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "search": search,
        "shipping_mode": shipping_mode,
        "delivery_status": delivery_status,
        "late_risk": late_risk,
        "shipping_modes": shipping_modes,
        "delivery_statuses": delivery_statuses,
        "total_records": paginator.count,
    }

    return render(request, "dashboard/data_records.html", context)


@login_required
@user_passes_test(staff_required)
def add_record(request):
    if request.method == "POST":
        form = SupplyChainRecordForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "The new record was saved successfully.")
            return redirect("data_records")
    else:
        form = SupplyChainRecordForm()

    return render(
        request,
        "dashboard/record_form.html",
        {
            "form": form,
            "page_title": "Add New Record",
            "button_text": "Save Record",
        },
    )


@login_required
@user_passes_test(staff_required)
def edit_record(request, order_item_id):
    record = get_object_or_404(
        SupplyChainRecord,
        order_item_id=order_item_id,
    )

    if request.method == "POST":
        form = SupplyChainRecordForm(request.POST, instance=record)
    else:
        form = SupplyChainRecordForm(instance=record)

    # Keep the existing record's unique ID unchanged.
    form.fields["order_item_id"].disabled = True

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "The record was updated successfully.")
        return redirect("data_records")

    return render(
        request,
        "dashboard/record_form.html",
        {
            "form": form,
            "page_title": "Edit Record",
            "button_text": "Update Record",
            "record": record,
        },
    )


@login_required
@user_passes_test(staff_required)
def delete_record(request, order_item_id):
    record = get_object_or_404(
        SupplyChainRecord,
        order_item_id=order_item_id,
    )

    if request.method == "POST":
        record.delete()
        messages.success(request, "The record was deleted successfully.")
        return redirect("data_records")

    return render(
        request,
        "dashboard/record_confirm_delete.html",
        {"record": record},
    )
