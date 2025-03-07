# Generated by Django 5.1.3 on 2025-02-14 20:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz_app", "0009_image_taskpixi"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="page_background",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="quiz_page_background_images",
                to="quiz_app.image",
            ),
        ),
    ]
