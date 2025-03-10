# Generated by Django 5.1.3 on 2025-02-04 15:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("quiz_app", "0006_quizresult"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DragDropTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("resettle", "Рассели"),
                            ("place", "Положи"),
                            ("continue", "Продолжи"),
                            ("fill", "Заполни"),
                            ("replace", "Замени на верные"),
                            ("fill_replace", "Заполни и замени"),
                        ],
                        default="continue",
                        max_length=50,
                    ),
                ),
                ("task", models.TextField()),
                ("replacement", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dragdrop_tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "background_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="dragdrop_tasks",
                        to="quiz_app.image",
                    ),
                ),
                (
                    "music",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="dragdrop_tasks",
                        to="quiz_app.music",
                    ),
                ),
                (
                    "next_task",
                    models.ManyToManyField(
                        blank=True,
                        related_name="previous_tasks",
                        to="dragdrop_app.dragdroptask",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Container",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("condition", models.CharField(blank=True, max_length=255)),
                ("visibility_text", models.BooleanField(default=True)),
                ("alt_text", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "image_url",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="containers",
                        to="quiz_app.image",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="containers",
                        to="dragdrop_app.dragdroptask",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=255)),
                ("condition", models.CharField(blank=True, max_length=255)),
                ("visibility_text", models.BooleanField(default=True)),
                ("alt_text", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "image_url",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="items",
                        to="quiz_app.image",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="dragdrop_app.dragdroptask",
                    ),
                ),
            ],
        ),
    ]
