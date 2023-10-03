# Generated by Django 4.2.5 on 2023-10-02 23:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pipelines",
            fields=[
                ("chosen_work_mode", models.CharField(auto_created="standart")),
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("text", models.CharField(blank=True, max_length=250000, null=True)),
                ("model", models.CharField(max_length=100, null=True)),
                ("ftmodel", models.CharField(max_length=100, null=True)),
                ("tokens", models.IntegerField(null=True)),
                ("temperature", models.FloatField(null=True)),
                ("voice", models.BooleanField(null=True)),
                ("name", models.CharField(max_length=255, null=True)),
                ("order_number", models.IntegerField(null=True)),
                ("filename", models.CharField()),
                ("work_rule", models.JSONField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Statuses",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=300)),
                ("order_number", models.IntegerField()),
                ("is_active", models.BooleanField(default=True)),
                (
                    "pipeline_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.pipelines"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GptApiKey",
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
                ("key", models.CharField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
