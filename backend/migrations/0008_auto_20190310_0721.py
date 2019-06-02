# Generated by Django 2.1 on 2019-03-10 07:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0007_googlesheet_email'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GP',
            new_name='Group',
        ),
        migrations.RenameModel(
            old_name='GPM',
            new_name='GroupMember',
        ),
    ]