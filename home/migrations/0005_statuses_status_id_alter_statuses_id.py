# Generated by Django 4.2.5 on 2023-10-03 00:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0004_alter_pipelines_id_alter_statuses_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="statuses",
            name="status_id",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="statuses",
            name="id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
