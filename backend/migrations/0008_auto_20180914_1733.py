# Generated by Django 2.1 on 2018-09-14 09:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0007_auto_20180914_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpm',
            name='edit',
            field=models.ManyToManyField(related_name='euser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gpm',
            name='view',
            field=models.ManyToManyField(related_name='vuser', to=settings.AUTH_USER_MODEL),
        ),
    ]
