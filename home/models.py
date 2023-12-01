from django.contrib.auth.models import User
from django.db import models


class ModeMessages(models.Model):
    hi_message = models.CharField(default="")
    openai_error_message = models.CharField(default='')
    database_error_message = models.CharField(default='')
    service_settings_error_message = models.CharField(default='')


class ModeQualification(models.Model):
    value = models.JSONField(default={})
    qualification_finished = models.CharField(default='')


class SearchMode(models.Model):
    qualification = models.ForeignKey(ModeQualification, on_delete=models.CASCADE)
    mode_messages = models.ForeignKey(ModeMessages, on_delete=models.CASCADE)
    database_link = models.CharField(default="")
    database_file_id = models.CharField(default='')
    search_rules = models.JSONField(default=[])
    view_rule = models.CharField(default="")
    results_count = models.IntegerField(default=1)


class KnowledgeMode(models.Model):
    qualification = models.ForeignKey(ModeQualification, on_delete=models.CASCADE)
    mode_messages = models.ForeignKey(ModeMessages, on_delete=models.CASCADE)
    database_link = models.CharField(default='')
    database_file_id = models.CharField(default='')
    prompt_mode_id = models.IntegerField(default=None, null=True)


class SearchAndKnowledgeMode(models.Model):
    search_mode = models.ForeignKey(SearchMode, on_delete=models.CASCADE)
    knowledge_mode = models.ForeignKey(KnowledgeMode, on_delete=models.CASCADE)


class PromptMode(models.Model):
    qualification = models.ForeignKey(ModeQualification, on_delete=models.CASCADE)
    context = models.CharField(max_length=250000, default="")
    model = models.CharField(max_length=100, default="gpt-3.5-turbo")
    max_tokens = models.IntegerField(default=0)
    temperature = models.FloatField(default=1)
    error_message = models.TextField(default='', null=True)
    error_message_time = models.IntegerField(default=3, null=True)
    connected_to = models.IntegerField(null=True, default=None)
    working_stages = models.JSONField(null=True, default=None)


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


class Transactions(models.Model):
    sub_type = models.IntegerField()
    date = models.DateField()
    amount = models.FloatField()
    payment_id = models.TextField()
    owner_id = models.IntegerField()
    is_finished = models.BooleanField()


class Subscriptions(models.Model):
    date_start = models.DateField()
    period = models.IntegerField()
    owner_id = models.IntegerField()
    transaction_id = models.IntegerField(default=None)


class AvatarexSettings(models.Model):
    knowledge_link = models.CharField(max_length=100)
    context = models.CharField(max_length=30000)
    api_token = models.CharField(max_length=100)
    error_message = models.CharField(max_length=30000)


class AmoRegisterTry(models.Model):
    login = models.CharField(max_length=1000, null=True)
    password = models.CharField(max_length=1000, null=True)
    host = models.CharField(max_length=1000, null=True)
    amo_hash = models.CharField(max_length=1000, null=True)
    api_auth_passed = models.BooleanField(null=True)
    site_auth_passed = models.BooleanField(null=True)
