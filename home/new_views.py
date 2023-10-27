import json
import os

import gdown
import openpyxl
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from home.forms import GptDefaultMode
from home.models import Pipelines


def download_file(filename, request) -> bool:
    file_id = filename.split("/")[-2]
    if not os.path.exists('uploads/' + file_id + '.xlsx'):
        try:
            download_url = filename
            output_path = f"uploads/{file_id}.xlsx"
            gdown.download(download_url, output_path, quiet=True)
        except Exception:
            messages.warning(request, 'Не удалось сохранить данные!')
            return False
    return True


@login_required
def database_mode(request):
    d = dict(request.GET.items())
    pipeline = d['pipeline']
    pipeline = Pipelines.objects.get(user=request.user, p_id=pipeline)
    db_mode = pipeline.search_mode

    first_row_data, second_row_data = [], []
    if db_mode.database_link != "":
        all_is_ok = download_file(db_mode.database_link, request)
        db_mode.database_link = ''
        db_mode.save()
        if all_is_ok:
            file_id = db_mode.database_link.split("/")[-2] + '.xlsx'
            workbook = openpyxl.load_workbook('uploads/' + file_id)
            sheet = workbook.active
            for row in sheet.iter_rows(min_row=1, max_row=2, values_only=True):
                if not first_row_data:
                    first_row_data = list(row)
                else:
                    second_row_data = list(row)

    rules = db_mode.search_rules
    rules_view = []
    for k in first_row_data:
        if k in rules.keys():
            rules_view.append({'t': k, 'v': rules[k]})
        else:
            rules_view.append({'t': k, 'v': ''})
    print(rules_view)
    return render(request, 'home/modes/database_mode.html',
                  {'filename': db_mode.database_link,
                   'names': first_row_data,
                   'items': second_row_data,
                   'rules': rules_view,
                   'pipeline': pipeline.p_id,
                   'mode_messages': db_mode.mode_messages,
                   'view_rule': db_mode.view_rule,
                   'results_count': db_mode.results_count
                   })


@login_required
def knowledge_mode(request):
    pass


@login_required
def database_and_knowledge_mode(request):
    pass


@login_required
def prompt_mode(request):
    d = dict(request.GET.items())
    instance = Pipelines.objects.get(user=request.user, p_id=d['pipeline'])
    model_id, fine_tuned_id = instance.prompt_mode.model, ''
    if 'gpt-3.5-turbo' not in model_id:
        fine_tuned_id = model_id
        model_id = 'gpt-3.5-turbo'

    form = GptDefaultMode(initial=
                          {'context': instance.prompt_mode.context,
                           'max_tokens': instance.prompt_mode.max_tokens,
                           'temperature': instance.prompt_mode.temperature,
                           'model': model_id,
                           'fine_tunel_model_id': fine_tuned_id
                           })

    if request.method == 'POST':
        form = GptDefaultMode(request.POST)
        if form.is_valid():
            field_names = request.POST.getlist('field-name')
            field_values = request.POST.getlist('field-value')
            fields = {}
            for field_index in range(len(field_names)):
                if field_names[field_index] != '':
                    fields[field_names[field_index]] = field_values[field_index]
            instance.prompt_mode.qualification.value = fields
            instance.prompt_mode.qualification.save()
            messages.success(request, 'Настройки обновлены!')
            context = form.cleaned_data.get('context')
            max_tokens = form.cleaned_data.get('max_tokens')
            temperature = form.cleaned_data.get('temperature')
            model = form.cleaned_data.get('model')
            fine_tunel_model_id = form.cleaned_data.get('fine_tunel_model_id')
            instance.prompt_mode.context = context
            instance.prompt_mode.max_tokens = max_tokens
            instance.prompt_mode.temperature = temperature

            if fine_tunel_model_id == '':
                instance.prompt_mode.model = model
            else:
                instance.prompt_mode.model = fine_tunel_model_id
            instance.prompt_mode.save()

        else:
            messages.warning(request, 'Не удалось обновить!')
    return render(request, 'home/modes/prompt_mode.html', {'form': form,
                                                           'qualification_rules': instance.prompt_mode.qualification
                                                           })


@login_required
def payment(request):
    return render(request, 'home/payment.html')
