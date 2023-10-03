import json
import os
import openpyxl

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from . import amo_auth
from .forms import AmoRegisterForm, GptDefaultMode
from .models import AmoConnect, Pipelines, Statuses, GptApiKey, UploadedFile


@login_required
def home(request):
    instance = AmoConnect.objects.filter(user=request.user).first()
    if instance:
        # amo_auth.update_pipelines(instance.host, instance.email, instance.password, request.user)
        pipelines = Pipelines.objects.all().filter(user=request.user, is_exists=True).order_by('order_number')

        gpt_token_instance = GptApiKey.objects.filter(user=request.user).first()
        if not gpt_token_instance:
            gpt_token = ''
        else:
            gpt_token = GptApiKey.objects.get(user=request.user).key
        return render(request, 'home/home.html', {'pipelines': pipelines,
                                                  'gpt_token': gpt_token})
    else:
        return redirect(amo_register)


@login_required
@csrf_exempt
def get_stages_by_pipeline(request):
    form_dict = json.loads(request.body.decode('utf-8'))
    if 'pipeline' not in form_dict.keys() or not form_dict['pipeline'].isdigit():
        messages.warning(request, 'Некорректный запрос!')
        return redirect(home)

    pipeline = form_dict['pipeline']
    selected_mode = Pipelines.objects.get(user=request.user, p_id=pipeline).chosen_work_mode
    disabled_mode = 'With database' if selected_mode == 'Standart' else 'Standart'
    stages = list(
        Statuses.objects.all().filter(pipeline_id_p_id=pipeline, is_exists=True).order_by('order_number').values())

    return JsonResponse({
        'stages': stages,
        'selected_mode': selected_mode,
        'disabled_mode': disabled_mode
    })


@login_required
@csrf_exempt
def set_stage_by_pipeline(request):
    d = dict(request.GET.items())
    status = Statuses.objects.get(pipeline_id_id=d['pipeline'], status_id=d['status'])
    status.is_active = False if status.is_active else True
    status.save()
    messages.success(request, 'Статус обновлен!')
    return redirect(home)


@login_required
def update_mode(request):
    d = dict(request.GET.items())
    pipeline = Pipelines.objects.get(id=d['pipeline'])
    pipeline.chosen_work_mode = 'Standart' if pipeline.chosen_work_mode == 'With database' else 'With database'
    pipeline.save()
    messages.success(request, 'Режим работы изменен!')
    return redirect(home)


@login_required
def update_token(request):
    d = dict(request.GET.items())

    instance = GptApiKey.objects.filter(user=request.user).first()

    if instance:
        inst = GptApiKey.objects.get(user=request.user)
        inst.key = d['token']
        inst.save()
    else:
        GptApiKey(
            user=request.user,
            key=d['token']
        ).save()

    messages.success(request, 'Обновление токена прошло успешно!')
    return redirect(home)


@login_required
def db_mode(request):
    d = dict(request.GET.items())
    pipeline = d['pipeline']
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        # Optional: Save the file to a model (if you have one)
        file_instance = UploadedFile(file=uploaded_file)
        file_instance.save()

        # Write the uploaded file to the server
        file_path = uploaded_file.name
        pipeline = Pipelines.objects.get(user=request.user, p_id=pipeline)
        pipeline.filename = file_path
        pipeline.save()
        with open("uploads/" + file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        messages.success(request, 'Файл успешно загружен!')
        return redirect(home)
    pipeline = Pipelines.objects.get(user=request.user, p_id=pipeline)
    has_file = True if pipeline.filename != '' else False

    first_row_data = []
    second_row_data = []
    if has_file:
        workbook = openpyxl.load_workbook('uploads/' + pipeline.filename)
        sheet = workbook.active
        for row in sheet.iter_rows(min_row=1, max_row=2, values_only=True):
            if not first_row_data:
                first_row_data = list(row)
            else:
                second_row_data = list(row)
    rules = pipeline.work_rule
    rules_view = []
    for k in first_row_data:
        if k in rules.keys():
            rules_view.append({'t': k, 'v': rules[k]})
        else:
            rules_view.append({'t': k, 'v': ''})
    print(rules_view)
    return render(request, 'home/db_mode.html',
                  {'filename': pipeline.filename,
                   'has_file': has_file,
                   'names': first_row_data,
                   'items': second_row_data,
                   'rules': rules_view})


@login_required
def syncronize_amo(request):
    amo_connect = AmoConnect.objects.get(user=request.user)
    amo_auth.update_pipelines(amo_connect.host, amo_connect.email, amo_connect.password, amo_connect.user)
    messages.success(request, 'Воронки синхронизированы!')
    return redirect(home)


@login_required
def default_mode(request):
    d = dict(request.GET.items())
    instance = Pipelines.objects.get(user=request.user, id=d['pipeline'])
    if request.method == 'GET':
        form = GptDefaultMode(initial=
                              {'context': instance.text,
                               'voice_message_detection': instance.voice,
                               'max_tokens': instance.tokens,
                               'temperature': instance.temperature,
                               'model': instance.model,
                               'fine_tunel_model_id': instance.ftmodel
                               })
        return render(request, 'home/default_mode.html', {'form': form})
    else:
        form = GptDefaultMode(request.POST)
        if form.is_valid():
            messages.success(request, 'Настройки обновлены!')
            context = form.cleaned_data.get('context')
            voice_message_detection = form.cleaned_data.get('voice_message_detection')
            max_tokens = form.cleaned_data.get('max_tokens')
            temperature = form.cleaned_data.get('temperature')
            model = form.cleaned_data.get('model')
            fine_tunel_model_id = form.cleaned_data.get('fine_tunel_model_id')
            instance.text = context
            instance.voice = voice_message_detection
            instance.tokens = max_tokens
            instance.temperature = temperature
            instance.model = model
            instance.ftmodel = fine_tunel_model_id
            instance.save()
        else:
            messages.warning(request, 'Не удалось обновить!')

        return redirect(home)


@login_required
def amo_register(request):
    if request.method == 'POST':
        form = AmoRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            host = form.cleaned_data.get('host')
            password = form.cleaned_data.get('password')
            account_chat_id = form.cleaned_data.get('account_chat_id')
            status = amo_auth.try_auth(host, email, password, 3)
            amo_auth.update_pipelines(host, email, password, request.user)

            instance = AmoConnect.objects.filter(user=request.user).first()
            if status:
                if instance:
                    instance = AmoConnect.objects.get(user=request.user)
                    instance.email = email
                    instance.host = host
                    instance.password = password
                    instance.account_chat_id = account_chat_id
                    instance.save()
                else:
                    AmoConnect(
                        email=email,
                        host=host,
                        password=password,
                        account_chat_id=account_chat_id,
                        user=request.user
                    ).save()
                messages.success(request, 'Интеграция произведена успешно!')
                return redirect(home)
            else:
                messages.warning(request, 'Проверьте данные! Ошибка интеграции.')

        else:
            messages.info(request, "Неккоректно заполнена форма!")
    else:
        messages.info(request, "Для начала работы необходимо подключить аккаунт Amocrm.")
        form = AmoRegisterForm()
    return render(request, 'home/connect_service.html', {'form': form})


def main(request):
    return render(request, 'home/main.html')


def tomorrow(request):
    messages.info(request, 'Дата запуска раздела: 04.10.2023')
    return render(request, 'home/404.html')


def profile(request):
    messages.info(request, 'Дата запуска раздела: 04.10.2023')
    return render(request, 'home/404.html')


@login_required()
@csrf_exempt
def update_db_rules(request):
    data = json.loads(request.body.decode('utf-8'))
    pipeline = data['currentUrl'].split('?pipeline=')[1]
    pipeline_obj = Pipelines.objects.get(p_id=pipeline, user=request.user)
    del data['currentUrl']
    pipeline_obj.work_rule = data
    pipeline_obj.save()
    messages.success(request, "Данные обновлены!")
    return 'ok'
