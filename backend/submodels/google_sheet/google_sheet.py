from django.db import models
from backend.models import Group


class GoogleSheet(models.Model):
    TITLE = models.CharField(max_length=100)
    URL = models.URLField(max_length=200, verbose_name="目標網址")
    SID = models.IntegerField(verbose_name="學號欄位", blank=True, null=True)
    CNAME = models.IntegerField(verbose_name="中文名稱欄位", blank=True, null=True)
    VIP = models.IntegerField(verbose_name="是否為學生會員欄位", blank=True, null=True)
    EMAIL = models.IntegerField(verbose_name="EMAIL 在第幾欄", blank=True,
                                null=True)
    GP = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.GP.GNAME + " - " + self.TITLE
