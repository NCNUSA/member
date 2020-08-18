# Generated by Django 2.1 on 2018-12-06 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("line_bot", "0002_remove_staff_member")]

    operations = [
        migrations.CreateModel(
            name="RecvMSG",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "user_id",
                    models.CharField(max_length=100, unique=True, verbose_name="LINE User ID"),
                ),
                (
                    "display_name",
                    models.CharField(blank=True, max_length=20, null=True, verbose_name="名稱"),
                ),
                ("MSG", models.TextField(blank=True, null=True, verbose_name="訊息")),
                ("picture_url", models.URLField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="建立時間")),
            ],
        )
    ]
