from django.db import connection
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from .models import Service


def service_list(request):
    query = request.GET.get("query", "")

    if query:
        services = Service.objects.filter(
            Q(is_active=True)
            & (Q(name__icontains=query) | Q(mini_description__icontains=query))
        )
    else:
        services = Service.objects.filter(is_active=True)

    return render(
        request, "vps_app/service_list.html", {"services": services, "query": query}
    )


def service_detail(request, service_id):
    service = Service.objects.get(id=service_id)
    return render(request, "vps_app/service_detail.html", {"service": service})


def service_delete(request, service_id):
    if request.method != "POST":
        return redirect("service_list")
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE vps_app_service SET is_active = %s WHERE id = %s",
            [False, service_id],
        )
    return redirect("service_list")
