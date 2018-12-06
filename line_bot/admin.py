from django.contrib import admin
from .models import *

# Register your models here.


class StaffAdmin(admin.ModelAdmin):
    list_display = ("user_id", "CNAME")
    search_fields = ["user_id", "CNAME"]


class RecvMSGAdmin(admin.ModelAdmin):
    list_display = ("user_id", "display_name", "MSG", "created_at")
    search_fields = ["user_id", "display_name", "MSG", "created_at"]


admin.site.register(Staff, StaffAdmin)
admin.site.register(RecvMSG, RecvMSGAdmin)
