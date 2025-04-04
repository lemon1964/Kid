# Generated by Django 5.1.3 on 2025-02-09 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pixi_app2", "0001_initial"),
        ("quiz_app", "0008_rename_container_image_containerdragdrop_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="pixiimage",
            name="image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pixi_task_images",
                to="quiz_app.image",
            ),
        ),
        migrations.AddField(
            model_name="pixitask",
            name="music",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="quiz_app.music",
            ),
        ),
    ]
