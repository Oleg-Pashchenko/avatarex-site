from django.contrib.auth.models import User
from django.db import models


class AmoConnect(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField()
    host = models.CharField()
    password = models.CharField()
    account_chat_id = models.CharField()


class GptApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField()


class Pipelines(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=250000, null=True, blank=True)
    model = models.CharField(max_length=100, null=True)
    ftmodel = models.CharField(max_length=100, null=True)
    tokens = models.IntegerField(null=True)
    temperature = models.FloatField(null=True)
    voice = models.BooleanField(null=True)
    name = models.CharField(max_length=255, null=True)
    order_number = models.IntegerField(null=True)
    chosen_work_mode = models.CharField(auto_created='Standart', default='Standart', null=False)
    filename = models.CharField(null=True)
    work_rule = models.JSONField(null=True)
    is_exists = models.BooleanField(default=True)


class Statuses(models.Model):
    status_id = models.IntegerField()
    name = models.CharField(max_length=300)
    order_number = models.IntegerField()
    is_active = models.BooleanField(default=True)
    pipeline_id = models.ForeignKey(Pipelines, on_delete=models.CASCADE)
    is_exists = models.BooleanField(default=True)


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
