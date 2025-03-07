# Generated by Django 5.1.3 on 2025-02-04 21:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dragdrop_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="container",
            name="task",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="containers",
                to="dragdrop_app.dragdroptask",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="task",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="items",
                to="dragdrop_app.dragdroptask",
            ),
        ),
    ]
