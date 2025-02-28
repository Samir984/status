# Generated by Django 5.1.6 on 2025-02-26 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Service",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("url", models.URLField()),
                ("token", models.CharField(blank=True, max_length=255, null=True)),
                ("is_paused", models.BooleanField(default=False)),
                ("data_created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
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
                ("webhook_url", models.TextField(default="")),
                ("is_paused", models.BooleanField(default=False)),
                (
                    "service",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notification",
                        to="core.service",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Log",
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
                ("is_up", models.BooleanField(default=False)),
                ("last_checked", models.DateTimeField(auto_now_add=True)),
                ("status_code", models.IntegerField(blank=True, null=True)),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="log",
                        to="core.service",
                    ),
                ),
            ],
        ),
    ]
