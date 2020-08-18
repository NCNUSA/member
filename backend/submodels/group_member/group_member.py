from django.db import models
from backend.models import Member, Group
from .manager import GroupMemberManager


class GroupMember(models.Model):
    MEMBER = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="成員")
    GP = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="群組")
    TITLE = models.CharField(max_length=15, blank=True, null=True, verbose_name="職稱")
    RM = models.CharField(max_length=30, blank=True, null=True, verbose_name="備註")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="建立時間")
    objects = GroupMemberManager()

    def __str__(self):
        return self.GP.GNAME + " " + self.MEMBER.CNAME
