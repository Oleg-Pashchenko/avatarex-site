from django.contrib.auth.models import User
from django.db import models


class ModeMessages(models.Model):
    hi_message = models.CharField(default="")
    openai_error_message = models.CharField(default='')
    database_error_message = models.CharField(default='')
    service_settings_error_message = models.CharField(default='')


class ModeQualification(models.Model):
    value = models.JSONField(default={})


class SearchMode(models.Model):
    qualification = models.ForeignKey(ModeQualification, on_delete=models.CASCADE)
    mode_messages = models.ForeignKey(ModeMessages, on_delete=models.CASCADE)
    database_link = models.CharField(default="")
    search_rules = models.JSONField(default=[])
    view_rule = models.CharField(default="")
    results_count = models.IntegerField(default=1)


class KnowledgeMode(models.Model):
    qualification = models.ForeignKey(ModeQualification, on_delete=models.CASCADE)
    mode_messages = models.ForeignKey(ModeMessages, on_delete=models.CASCADE)
    database_link = models.CharField(default='')


class SearchAndKnowledgeMode(models.Model):
    search_mode = models.ForeignKey(SearchMode, on_delete=models.CASCADE)
    knowledge_mode = models.ForeignKey(KnowledgeMode, on_delete=models.CASCADE)


class PromptMode(models.Model):
    qualification = models.ForeignKey(ModeQualification, on_delete=models.CASCADE)
    context = models.CharField(max_length=250000, default="")
    model = models.CharField(max_length=100, default="gpt-3.5-turbo")
    max_tokens = models.IntegerField(default=0)
    temperature = models.FloatField(default=1)


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
    p_id = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voice_message_detection = models.BooleanField(null=True, default=True)
    name = models.CharField(max_length=255, null=True)
    order_number = models.IntegerField(null=True)
    is_exists = models.BooleanField(default=True)
    chosen_work_mode = models.CharField(default='Prompt mode')
    prompt_mode = models.ForeignKey(PromptMode, on_delete=models.CASCADE)
    search_mode = models.ForeignKey(SearchMode, on_delete=models.CASCADE)
    knowledge_mode = models.ForeignKey(KnowledgeMode, on_delete=models.CASCADE)
    knowledge_and_search_mode = models.ForeignKey(SearchAndKnowledgeMode, on_delete=models.CASCADE)


class Statuses(models.Model):
    status_id = models.IntegerField()
    name = models.CharField(max_length=300)
    order_number = models.IntegerField()
    is_active = models.BooleanField(default=True)
    pipeline_id = models.ForeignKey(Pipelines, on_delete=models.CASCADE)
    is_exists = models.BooleanField(default=True)
