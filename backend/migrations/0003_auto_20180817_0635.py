# Generated by Django 2.1 on 2018-08-17 06:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("backend", "0002_auto_20180817_0601")]

    operations = [
        migrations.AlterField(
            model_name="department",
            name="COLLEGE",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="DEP",
                to="backend.College",
                verbose_name="學院",
            ),
        )
    ]
