# Generated by Django 5.1.3 on 2025-02-15 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dragdrop_app", "0007_remove_dragdroptask_task_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="dragdroptask",
            name="unique_id",
            field=models.CharField(
                max_length=10, editable=False, blank=True, default=""
            ),
        ),
        migrations.AlterField(
            model_name="dragdroptask",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
