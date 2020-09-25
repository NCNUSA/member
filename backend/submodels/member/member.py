from django.db import models
from .manager import MemberManager
from .validator import Validator


class Member(models.Model):
    SID = models.CharField(max_length=10, unique=True, verbose_name="學號")
    CNAME = models.CharField(max_length=20, verbose_name="中文姓名")
    ENAME = models.CharField(max_length=100, blank=True, null=True, verbose_name="英文姓名")
    DEP = models.CharField(max_length=30, blank=True, null=True, verbose_name="系所")
    GRADE = models.CharField(max_length=10, blank=True, null=True, verbose_name="年級")
    EMAIL = models.EmailField(blank=True, null=True)
    PHONE = models.CharField(max_length=20, blank=True, null=True, verbose_name="手機")
    EXT = models.CharField(max_length=20, blank=True, null=True, verbose_name="校內分機")
    ICN = models.CharField(max_length=15, blank=True, null=True, verbose_name="身份證字號")
    ADDR = models.CharField(max_length=200, blank=True, null=True, verbose_name="住址")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="修改時間")
    objects = MemberManager()

    def __str__(self):
        return self.SID + " " + self.CNAME

    def save(self, *args, **kwargs):
        self.clean()
        return super(Member, self).save()

    def clean(self):
        super().clean()
        Validator(self).execute()
