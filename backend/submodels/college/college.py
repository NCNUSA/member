from django.db import models


class College(models.Model):
    CNAME = models.CharField(max_length=30, verbose_name="中文名稱")
    ENAME = models.CharField(max_length=200, blank=True, null=True, verbose_name="英文名稱")
    CABBR = models.CharField(max_length=10, blank=True, null=True, verbose_name="中文簡稱")
    EABBR = models.CharField(max_length=30, blank=True, null=True, verbose_name="英文簡稱")

    def __str__(self):
        return self.CABBR
