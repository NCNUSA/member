from django.db import models
from .manager import GroupManager


class Group(models.Model):
    from django.contrib.auth.models import User

    GNAME = models.CharField(max_length=30, verbose_name="社團名稱")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="建立時間")
    users = models.ManyToManyField(User, through="UserPerms", related_name="perms")
    objects = GroupManager()

    def __str__(self):
        return self.GNAME
