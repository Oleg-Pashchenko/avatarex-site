# Generated by Django 4.2.5 on 2023-10-27 20:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0004_alter_pipelines_voice_message_detection"),
    ]

    operations = [
        migrations.AddField(
            model_name="knowledgemode",
            name="database_file_id",
            field=models.CharField(default=""),
        ),
        migrations.AddField(
            model_name="searchmode",
            name="database_file_id",
            field=models.CharField(default=""),
        ),
    ]
