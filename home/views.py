import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import AmoRegisterForm, GptDefaultMode, GptDatabaseMode

pipelines = [{'id': 1, 'name': 'test', 'stages':
    [{'id': 1, 'name': 'test1', 'active': True}, {'id': 2, 'name': 'test2', 'active': True}]},
             {'id': 2, 'name': 'test2', 'stages':
                 [{'id': 3, 'name': 'test3', 'active': False}, {'id': 4, 'name': 'test4', 'active': True}]
              }]


@login_required
def home(request):
    return render(request, 'home/home.html', {'pipelines': pipelines})


@login_required
@csrf_exempt
def get_stages_by_pipeline(request):
    form_dict = json.loads(request.body.decode('utf-8'))
    if 'pipeline' not in form_dict.keys() or not form_dict['pipeline'].isdigit():
        messages.warning(request, 'Некорректный запрос!')
        return render(request, 'home/home.html', {'pipelines': pipelines})

    pipeline = form_dict['pipeline']
    print(pipeline)
    stages = []
    for p in pipelines:
        if p['id'] == int(pipeline):
            stages = p['stages']
            break
    return JsonResponse({
        'stages': stages
    })


@login_required
@csrf_exempt
def save_home(request):
    pass


@login_required
def db_mode(request):
    form = GptDatabaseMode()
    return render(request, 'home/db_mode.html', {'form': form})


@login_required
def default_mode(request):
    form = GptDefaultMode()
    return render(request, 'home/default_mode.html', {'form': form})


@login_required
def amo_register(request):
    messages.info(request, "Для начала работы необходимо подключить аккаунт Amocrm.")
    form = AmoRegisterForm()
    return render(request, 'home/connect_service.html', {'form': form})


def main(request):
    return render(request, 'home/main.html')


def tomorrow(request):
    messages.info(request, 'Дата запуска раздела: 04.10.2023')
    return render(request, 'home/404.html')


def profile(request):
    pass
