from django.db import models
from backend.models import Member


class Staff(models.Model):
    user_id = models.CharField(max_length=100, unique=True, verbose_name='LINE User ID')
    CNAME = models.CharField(max_length=20, verbose_name='中文姓名')

    def __str__(self):
        return self.CNAME
