# Generated by Django 5.1.3 on 2025-02-04 18:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dragdrop_app", "0001_initial"),
        ("quiz_app", "0007_image_container_image_item"),
    ]

    operations = [
        migrations.RenameField(
            model_name="image", old_name="container", new_name="containerdragdrop",
        ),
        migrations.RenameField(
            model_name="image", old_name="item", new_name="itemdragdrop",
        ),
        migrations.AddField(
            model_name="image",
            name="taskdragdrop",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="dragdrop_app.dragdroptask",
            ),
        ),
    ]
