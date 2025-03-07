# Generated by Django 5.1.3 on 2024-12-30 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz_app", "0004_quiz_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
