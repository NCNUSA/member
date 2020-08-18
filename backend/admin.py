from django.contrib import admin

from .models import *


class MemberAdmin(admin.ModelAdmin):
    list_display = ("SID", "CNAME", "DEP", "GRADE")
    search_fields = ["SID", "CNAME", "DEP", "GRADE"]


class GPAdmin(admin.ModelAdmin):
    list_display = ("GNAME", "created_at", "updated_at")
    search_fields = ["GNAME"]


class GPMAdmin(admin.ModelAdmin):
    list_display = ["get_GNAME", "get_CNAME", "TITLE"]

    def get_GNAME(self, obj):
        return obj.GP.GNAME

    def get_CNAME(self, obj):
        return obj.MEMBER.CNAME

    get_GNAME.short_description = "群組"
    get_CNAME.short_description = "姓名"


admin.site.register(Member, MemberAdmin)
admin.site.register(Group, GPAdmin)
admin.site.register(GroupMember, GPMAdmin)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(GoogleSheet)
admin.site.register(UserPerms)
