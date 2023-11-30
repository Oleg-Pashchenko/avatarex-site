import json

import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect
from home.models import Pipelines, GptApiKey
import gdown


@login_required
def update_mode(request: HttpRequest):
    data = json.loads(request.body.decode('utf-8'))

    url = data.get('currentUrl', None)
    pipeline_id = int(url.split('=')[1])
    mode = url.split('/')[-2]
    pipeline = Pipelines.objects.get(p_id=pipeline_id)

    know_prompt = data.get('knowledge-prompt', {})
    know_bound = data.get('knowledge-bounded', {})

    bounded_situations_fields = data.get('bounded_situations_fields', {})
    qualification_fields = data.get('qualification_fields', [])
    qualification_finished = data.get('qualificationFinished', None)
    prompt_data = data.get('prompt-data', {})

    print(mode, pipeline_id, data)
    return redirect('/home')


@login_required
def update_mode_file_link(request):
    """Get pipeline_id, mode_name, redirect urls params and filename string data"""
    info = request.POST.dict()

    pipeline_id = info['pipeline']
    mode_name = info['mode_name']
    redirect_url = ''

    google_drive_url = info['filename']
    file_id = google_drive_url.replace('https://docs.google.com/spreadsheets/d/', '')
    file_id = file_id.split('/')[0]
    try:
        download_url = f"https://drive.google.com/uc?id={file_id}"
        output_path = f"uploads/{file_id}.xlsx"
        gdown.download(download_url, output_path, quiet=True)
    except:
        return redirect(redirect_url)

    pipeline = Pipelines.objects.get(p_id=pipeline_id)
    if mode_name == 'search':
        pipeline.search_mode.database_file_id = file_id
        pipeline.search_mode.database_link = google_drive_url
    elif mode_name == 'knowledge':
        pipeline.knowledge_mode.database_file_id = file_id
        pipeline.knowledge_mode.database_link = google_drive_url
    elif mode_name == 'knowledge-and-search-update-knowledge':
        pipeline.knowledge_and_search_mode.knowledge_mode.database_link = file_id
        pipeline.knowledge_and_search_mode.knowledge_mode.database_link = google_drive_url
    elif mode_name == 'knowledge-and-search-update-search':
        pipeline.knowledge_and_search_mode.search_mode.database_file_id = file_id
        pipeline.knowledge_and_search_mode.search_mode.database_link = google_drive_url

    pipeline.search_mode.save()
    pipeline.knowledge_mode.save()
    pipeline.knowledge_and_search_mode.search_mode.save()
    pipeline.knowledge_and_search_mode.knowledge_mode.save()
    return redirect('/admin/users/')


@login_required
def prompt_mode_update(request):
    data = json.loads(request.body.decode('utf-8'))
    context = data['context']
    prompt_data = data.get('prompt-data', {})
    print(prompt_data)
    tokens_limit = int(data['tokens_limit'])
    temperature = float(data['temperature'])
    model = data['model']
    qualification_finished = data['qualificationFinished']
    qualification_fields = data['qualification_fields']
    print(qualification_finished, 'resp')
    pipeline_id = int(data['pipeline_id'])
    pipeline = Pipelines.objects.get(p_id=pipeline_id)
    pipeline.prompt_mode.context = context
    pipeline.prompt_mode.max_tokens = tokens_limit
    pipeline.prompt_mode.temperature = temperature
    pipeline.prompt_mode.model = model
    pipeline.prompt_mode.qualification.value = qualification_fields
    pipeline.prompt_mode.qualification.qualification_finished = qualification_finished
    pipeline.save()
    return redirect(f"/prompt-mode/?pipeline_id={pipeline_id}")


@login_required
def update_token(request):
    d = dict(request.GET.items())
    instance = GptApiKey.objects.filter(user=request.user).first()
    if instance:
        inst = GptApiKey.objects.get(user=request.user)
        inst.key = d['token']
        inst.save()
    else:
        GptApiKey(user=request.user, key=d['token']).save()


def widget(request):
    url = 'http://95.140.146.86:8083/widget-api'
    data = json.loads(request.body)
    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    print(response.text)
    return JsonResponse(response.json())
