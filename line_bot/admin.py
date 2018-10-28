from django.contrib import admin
from .models import *

# Register your models here.


class StaffAdmin(admin.ModelAdmin):
    list_display = ("user_id", "CNAME")
    search_fields = ["user_id", "CNAME"]


admin.site.register(Staff, StaffAdmin)
