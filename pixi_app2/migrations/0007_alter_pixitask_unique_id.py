# Generated by Django 5.1.3 on 2025-02-15 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pixi_app2", "0006_pixitask_unique_id_alter_pixitask_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pixitask",
            name="unique_id",
            field=models.CharField(blank=True, default="", max_length=10),
        ),
    ]
