from django.contrib import admin
from .models import (
    Application_Status,
    Service,
    Rate,
    Rate_Name,
    Application,
    Application_Service,
)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    ordering = ("id",)


admin.site.register(Service, ServiceAdmin)
admin.site.register(Rate)
admin.site.register(Rate_Name)
admin.site.register(Application_Status)
admin.site.register(Application)
admin.site.register(Application_Service)
