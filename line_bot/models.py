from django.db import models
from backend.models import Member


class Staff(models.Model):
    user_id = models.CharField(max_length=100, unique=True, verbose_name='LINE User ID')
    CNAME = models.CharField(max_length=20, verbose_name='中文姓名')

    def __str__(self):
        return self.CNAME


class RecvMSG(models.Model):
    user_id = models.CharField(max_length=100, verbose_name='LINE User ID')
    display_name = models.CharField(max_length=20, verbose_name='名稱', blank=True, null=True)
    MSG = models.TextField(verbose_name='訊息', blank=True, null=True)
    picture_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
