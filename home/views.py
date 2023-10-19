import json
import os

import gdown
import openpyxl

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from . import amo_auth
from .forms import AmoRegisterForm, GptDefaultMode
from .models import AmoConnect, Pipelines, Statuses, GptApiKey, UploadedFile


@login_required
def home(request):
    instance = AmoConnect.objects.filter(user=request.user).first()

    current_pipeline = '' if 'current_pipeline' not in request.GET.dict() else request.GET.dict()['current_pipeline']
    if instance:
        # amo_auth.update_pipelines(instance.host, instance.email, instance.password, request.user)
        pipelines = Pipelines.objects.all().filter(user=request.user, is_exists=True).order_by('order_number')

        gpt_token_instance = GptApiKey.objects.filter(user=request.user).first()
        if not gpt_token_instance:
            gpt_token = ''
        else:

            gpt_token = GptApiKey.objects.get(user=request.user).key
        print(current_pipeline)
        return render(request, 'home/home.html', {'pipelines': pipelines,
                                                  'gpt_token': gpt_token,
                                                  'current_pipeline': current_pipeline})
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
        Statuses.objects.all().filter(pipeline_id__p_id=pipeline, is_exists=True).order_by('order_number').values())

    return JsonResponse({
        'stages': stages,
        'selected_mode': selected_mode,
        'disabled_mode': disabled_mode
    })


@login_required
@csrf_exempt
def set_stage_by_pipeline(request):
    d = dict(request.GET.items())
    status = Statuses.objects.get(pipeline_id__p_id=d['pipeline'], status_id=d['status'])
    status.is_active = False if status.is_active else True
    status.save()
    messages.success(request, 'Статус обновлен!')
    return redirect(f'/home/?current_pipeline={d["pipeline"]}')


@login_required
def update_mode(request):
    d = dict(request.GET.items())
    print(d)
    pipeline = Pipelines.objects.get(p_id=d['pipeline'])
    if d['mode'] != 'Standart' and d['mode'] != 'With database':
        messages.warning(request, "Ошибка обновления режима работы!")
    else:
        pipeline.chosen_work_mode = d['mode']
        pipeline.save()
        messages.success(request, 'Обновление режима работы прошло успешно!')
    return redirect(f'/home/?current_pipeline={d["pipeline"]}')


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
    if has_file and pipeline.filename:
        if not os.path.exists('uploads/' + pipeline.filename):
            try:
                download_url = pipeline.file_link
                print(download_url)
                output_path = f"uploads/{pipeline.filename}"
                gdown.download(download_url, output_path, quiet=True)
            except Exception as e:
                print(e)
                messages.warning(request, 'Не удалось сохранить данные!')

        workbook = openpyxl.load_workbook('uploads/' + pipeline.filename)
        sheet = workbook.active
        for row in sheet.iter_rows(min_row=1, max_row=2, values_only=True):
            if not first_row_data:
                first_row_data = list(row)
            else:
                second_row_data = list(row)
    rules = pipeline.work_rule
    if rules is None:
        rules = {}
    rules_view = []
    for k in first_row_data:
        if k in rules.keys():
            rules_view.append({'t': k, 'v': rules[k]})
        else:
            rules_view.append({'t': k, 'v': ''})
    print(rules_view)
    return render(request, 'home/db_mode.html',
                  {'filename': pipeline.filename,
                   'file_link': pipeline.file_link,
                   'has_file': has_file,
                   'names': first_row_data,
                   'items': second_row_data,
                   'rules': rules_view,
                   'pipeline': pipeline.p_id,
                   'hi_message': pipeline.hi_message,
                   'openai_error_message': pipeline.openai_error_message,
                   'db_error_message': pipeline.db_error_message,
                   'success_message': pipeline.success_message,
                   'view_rule': pipeline.view_rule
                   })


@login_required
def syncronize_amo(request):
    amo_connect = AmoConnect.objects.get(user=request.user)
    amo_auth.update_pipelines(amo_connect.host, amo_connect.email, amo_connect.password, amo_connect.user)
    messages.success(request, 'Воронки синхронизированы!')
    return redirect(home)


@login_required
def default_mode(request):
    d = dict(request.GET.items())
    instance = Pipelines.objects.get(user=request.user, p_id=d['pipeline'])
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
            instance = AmoConnect.objects.filter(email=email).first()
            if status:
                if instance:
                    user_email = User.objects.get(id=instance.id).email
                    messages.warning(request,
                                     f"Ошибка. Данный аккаунт Amocrm уже привязан к другому аккаунту "
                                     f"Avatarex! ({user_email})")
                    return redirect(amo_register)
                else:
                    amo_auth.update_pipelines(host, email, password, request.user)
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
    messages.info(request, 'Дата запуска раздела: 18.10.2023')
    return render(request, 'home/404.html')


def profile(request):
    messages.info(request, 'Дата запуска раздела: 18.10.2023')
    return render(request, 'home/404.html')


@login_required()
@csrf_exempt
def update_db_rules(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    pipeline = data['currentUrl'].split('?pipeline=')[1]
    pipeline_obj = Pipelines.objects.get(p_id=pipeline, user=request.user)
    del data['currentUrl']
    pipeline_obj.hi_message = data['hi_message']
    pipeline_obj.db_error_message = data['db_error_message']
    pipeline_obj.openai_error_message = data['openai_error_message']
    pipeline_obj.success_message = data['success_message']
    pipeline_obj.view_rule = data['view_rule']
    pipeline_obj.work_rule = data
    pipeline_obj.save()
    messages.success(request, "Данные обновлены!")
    return 'ok'


@login_required()
@csrf_exempt
def update_db_file(request):
    pipeline = request.GET.dict()['pipeline']

    import gdown

    google_drive_url = request.POST.dict()['filename']
    file_id = google_drive_url.split("/")[-2]

    try:
        download_url = f"https://drive.google.com/uc?id={file_id}"
        output_path = f"uploads/{file_id}.xlsx"
        gdown.download(download_url, output_path, quiet=True)
    except:
        messages.warning(request, 'Не удалось сохранить данные!')
        return redirect(home)
    pipeline = Pipelines.objects.get(user=request.user, p_id=pipeline)
    pipeline.filename = output_path.split('/')[1]
    pipeline.file_link = download_url
    pipeline.save()
    messages.success(request, 'Данные обновлены!')
    return redirect(home)

