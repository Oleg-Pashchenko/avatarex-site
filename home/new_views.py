import json

import openpyxl
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from home import misc, tinkoff
from home.forms import GptDefaultMode
from home.models import Pipelines
from home.wrappers import sub_active_required


@login_required
def database_mode(request):
    d = dict(request.GET.items())
    pipeline = d['pipeline']
    pipeline = Pipelines.objects.get(user=request.user, p_id=pipeline)
    db_mode = pipeline.search_mode

    return render(request, 'home/modes/database_mode.html',
                  {
                      'pipeline_id': pipeline.p_id,
                      'results_count': db_mode.results_count,
                      'youtube_video': 'https://www.youtube.com/embed/HSpYul7FYzw?si=UzabLVRlrN-83k12',

                      'file_link': db_mode.database_link,
                      'upload_file_inputs': [
                          {'action': f'/api/v1/update-mode-file-link/?pipeline_id={pipeline.p_id}&mode_name='
                                     f'search&redirect_url=/database-mode/?pipeline={pipeline.p_id}',
                           'text': 'Ссылка на базу данных', 'file_link': db_mode.database_link},
                      ],
                      'search_rules': misc.get_search_rules(file_id=db_mode.database_file_id,
                                                            search_rules=db_mode.search_rules),
                      'qualification_rules': db_mode.qualification,
                      'bounded_situations': db_mode.mode_messages,
                      'view_rule': db_mode.view_rule
                  })


@sub_active_required
@login_required
def knowledge_mode(request):
    qualification = [
        {
            'order': 1,
            'field_name': 'Имя',
            'question': 'Как вас зовут?',
            'additional_questions': [
                {
                    'order': 1,
                    'question': 'Скажите пожалуйста',
                    'time_number': 25,
                    'time_type': 'days',

                },
                {
                    'order': 2,
                    'question': 'Скажите пожалуйста',
                    'time_number': 10,
                    'time_type': 'hours',

                }
            ]
        },
        {
            'order': 2,
            'field_name': 'Дата',
            'question': 'Когда вы родились?',
            'additional_questions': [
                {
                    'order': 1,
                    'question': 'Привет',
                    'time_number': 1,
                    'time_type': 'hours',

                },
                {
                    'order': 2,
                    'question': 'Пока',
                    'time_number': 2,
                    'time_type': 'hours',

                }
            ]
        }
    ]

    d = dict(request.GET.items())
    pipeline = d['pipeline']
    pipeline = Pipelines.objects.get(user=request.user, p_id=pipeline)
    knowledge_mode = pipeline.knowledge_mode
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

    return render(request, 'home/modes/knowledge_mode.html',
                  {
                      'form': form,
                      'youtube_video': 'https://www.youtube.com/embed/HSpYul7FYzw?si=UzabLVRlrN-83k12',
                      'pipeline_id': pipeline.p_id,
                      'qualification_rules': qualification,

                      'file_link': knowledge_mode.database_link,
                      'upload_file_inputs': [
                          {'action': f'/api/v1/update-mode-file-link/?pipeline_id={pipeline.p_id}&mode_name='
                                     f'knowledge&redirect_url=/knowledge-mode/?pipeline={pipeline.p_id}',
                           'text': 'Ссылка на базу знаний', 'file_link': knowledge_mode.database_link},
                      ],
                      'bounded_situations': knowledge_mode.mode_messages,
                  })


@login_required
def prompt_mode(request):
    qualification = [
        {
            'order': 1,
            'field_name': 'Имя',
            'question': 'Как вас зовут?',
            'additional_questions': [
                {
                    'order': 1,
                    'question': 'Скажите пожалуйста',
                    'time_number': 1,
                    'time_type': 'days',

                },
                {
                    'order': 2,
                    'question': 'Скажите пожалуйста',
                    'time_number': 1,
                    'time_type': 'hours',

                }
            ]
        },
        {
            'order': 2,
            'field_name': 'Дата',
            'question': 'Когда вы родились?',
            'additional_questions': [
                {
                    'order': 1,
                    'question': 'Привет',
                    'time_number': 1,
                    'time_type': 'hours',

                },
                {
                    'order': 2,
                    'question': 'Пока',
                    'time_number': 2,
                    'time_type': 'hours',

                }
            ]
        }
    ]

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
            print(request.POST)
            instance.prompt_mode.qualification.qualification_finished = request.POST.get('qualificationFinished')
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
                                                           'youtube_video': 'https://www.youtube.com/embed/HSpYul7FYzw?si=UzabLVRlrN-83k12',
                                                           'qualification_rules': qualification
                                                           })


@login_required
def database_and_knowledge_mode(request):
    d = dict(request.GET.items())
    pipeline = d['pipeline']
    pipeline = Pipelines.objects.get(user=request.user, p_id=pipeline)
    d_k_mode = pipeline.knowledge_and_search_mode

    return render(request, 'home/modes/database_and_knowledge_mode.html',
                  {
                      'youtube_video': 'https://www.youtube.com/embed/HSpYul7FYzw?si=UzabLVRlrN-83k12',
                      'pipeline_id': pipeline.p_id,
                      'file_link': d_k_mode.search_mode.database_link,
                      'results_count': d_k_mode.search_mode.results_count,
                      'qualification_rules': d_k_mode.search_mode.qualification,

                      'upload_file_inputs': [
                          {'action': f'/api/v1/update-mode-file-link/?pipeline_id={pipeline.p_id}&mode_name='
                                     f'knowledge-and-search-update-search&redirect_url=/database-and-knowledge-mode/?pipeline={pipeline.p_id}',
                           'text': 'Ссылка на базу данных', 'file_link': d_k_mode.search_mode.database_link},

                          {'action': f'/api/v1/update-mode-file-link/?pipeline_id={pipeline.p_id}&mode_name='
                                     f'knowledge-and-search-update-knowledge&redirect_url=/database-and-knowledge-mode/?pipeline={pipeline.p_id}',
                           'text': 'Ссылка на базу знаний', 'file_link': d_k_mode.knowledge_mode.database_link}
                      ],
                      'search_rules': misc.get_search_rules(file_id=d_k_mode.search_mode.database_file_id,
                                                            search_rules=d_k_mode.search_mode.search_rules),
                      'bounded_situations': d_k_mode.search_mode.mode_messages,
                      'view_rule': d_k_mode.search_mode.view_rule
                  })


@login_required
def payment(request):
    # Here execute update method
    tinkoff.update(request.user.id)
    new_user = tinkoff.is_user_new(request.user.id)  # или False

    if request.method == 'POST':
        b = json.loads(request.body)
        period = b.get('period', None)
        if period is None:
            return render(request, 'home/payment.html')

        if str(period) == '1':
            if new_user:
                sum1 = 3000
            else:
                sum1 = 9000
        else:
            sum1 = 95000
        url = tinkoff.create_payment(sum1, request.user.id, int(period))
        return JsonResponse({'url': url})

    count, transactions = tinkoff.get_person_info(request.user.id)

    user = {'new_user': new_user}
    return render(request, 'home/payment.html',
                  {'transaction': transactions,
                   'user': user,
                   'days': f'{count} дней' if count != 0 else '',
                   'sub_type': 'Pro' if count != 0 else ''

                   })


def about(request):
    return render(request, 'home/about.html')


def faq(request):
    return render(request, 'home/faq.html')


def conf_policy(request):
    return render(request, 'home/conf_policy.html')

def events(request):
    return render(request, 'home/events.html')
