# Generated by Django 5.1.3 on 2025-02-16 20:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                    "stripe_payment_intent_id",
                    models.CharField(blank=True, max_length=250),
                ),
                (
                    "stripe_subscription_id",
                    models.CharField(blank=True, max_length=250),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "subscription_type",
                    models.CharField(
                        choices=[("monthly", "Monthly"), ("yearly", "Yearly")],
                        max_length=10,
                    ),
                ),
                ("coupon_code", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "discount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=5),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
