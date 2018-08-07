from django.contrib import admin
from .models import Member

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ('SID', 'CNAME', 'DEP', 'GRADE')
    search_fields = ['SID', 'CNAME', 'DEP', 'GRADE']

admin.site.register(Member, MemberAdmin)
