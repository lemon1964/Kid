# Generated by Django 5.1.3 on 2025-02-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz_app", "0015_alter_quiz_unique_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="unique_id",
            field=models.CharField(
                blank=True, editable=False, max_length=10, unique=True
            ),
        ),
    ]
