import time
import requests
from django.contrib import messages

from .models import *


def try_auth(host, mail, password, repeat, mode='test'):
    if repeat == 0:
        return False
    host2 = host.replace('https://', '').replace('/', '')
    try:
        session = requests.Session()
        response = session.get(host)
        session_id = response.cookies.get('session_id')
        csrf_token = response.cookies.get('csrf_token')
        headers = {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': f'session_id={session_id}; '
                      f'csrf_token={csrf_token};'
                      f'last_login={mail}',
            'Host': host.replace('https://', '').replace('/', ''),
            'Origin': host,
            'Referer': host,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
        payload = {
            'csrf_token': csrf_token,
            'password': password,
            'temporary_auth': "N",
            'username': mail}

        response = session.post(f'{host}oauth2/authorize', headers=headers, data=payload)
        access_token = response.cookies.get('access_token')
        refresh_token = response.cookies.get('refresh_token')
        headers['access_token'], headers['refresh_token'] = access_token, refresh_token
        payload = {'request[chats][session][action]': 'create'}
        headers['Host'] = host2
        response = session.post(f'{host}ajax/v1/chats/session', headers=headers, data=payload)
        token = response.json()['response']['chats']['session']['access_token']
    except Exception as e:
        time.sleep(3)
        return try_auth(host, mail, password, repeat - 1, mode)
    if mode != 'test':
        return token, session, headers

    return True


def update_pipelines(host, mail, password, user):
    print(host, mail, password, user)
    token, session, headers = try_auth(host, mail, password, 1, 'work')
    if host[-1] == '/':
        host = host[:-1]
    if host[0] != 'h':
        host = 'https://' + host
    response = session.get(f'{host}/ajax/v1/pipelines/list',
                           headers=headers).json()['response']['pipelines']
    ids, s_ids = set(), set()

    existing_pipelines = {pipeline.p_id: pipeline for pipeline in Pipelines.objects.filter(user=user)}

    for v in response.values():
        id = v['id']
        name, sort, statuses = v['name'], v['sort'], v['statuses']

        if id in existing_pipelines:
            # Обновляем существующий pipeline
            pipeline = existing_pipelines[id]
            pipeline.name = name
            pipeline.order_number = sort
            pipeline.save()
            print(f'Updated pipeline {name}')
        else:
            # Создаем новый pipeline
            q1 = ModeQualification.objects.create()
            q2 = ModeQualification.objects.create()
            q3 = ModeQualification.objects.create()
            q4 = ModeQualification.objects.create()
            q5 = ModeQualification.objects.create()

            mm1 = ModeMessages.objects.create()
            mm2 = ModeMessages.objects.create()
            mm3 = ModeMessages.objects.create()
            mm4 = ModeMessages.objects.create()

            prompt_mode = PromptMode.objects.create(qualification=q1)
            search_mode = SearchMode.objects.create(qualification=q2, mode_messages=mm1)
            search_mode2 = SearchMode.objects.create(qualification=q3, mode_messages=mm2)
            knowledge_mode = KnowledgeMode.objects.create(qualification=q4, mode_messages=mm3)
            knowledge_mode2 = KnowledgeMode.objects.create(qualification=q5, mode_messages=mm4)
            knowledge_and_search_mode = SearchAndKnowledgeMode.objects.create(search_mode=search_mode2,
                                                                              knowledge_mode=knowledge_mode2)

            pipeline = Pipelines.objects.create(
                p_id=id,
                name=name,
                order_number=sort,
                user=user,
                prompt_mode=prompt_mode,
                search_mode=search_mode,
                knowledge_mode=knowledge_mode,
                knowledge_and_search_mode=knowledge_and_search_mode
            )
            print(f'Created pipeline {name}')
        existing_statuses = {status.status_id: status for status in Statuses.objects.filter(pipeline_id=pipeline)}
        print(existing_statuses)
        for s in statuses.values():
            s_id = s['id']
            s_name, s_sort = s['name'], s['sort']
            s_ids.add(s_id)
            if s_id in existing_statuses:
                status = existing_statuses[s_id]
                status.name = s_name
                status.order_number = s_sort
                status.save()
                print(f'Updated status {s_name}')
            else:
                status = Statuses.objects.create(
                    status_id=s_id,
                    name=s_name,
                    order_number=s_sort,
                    pipeline_id=pipeline
                )
                print(f'Created status {s_name}')

    for id in ids:
        pipeline = Pipelines.objects.all().get(id=id)
        pipeline.is_exists = False
        pipeline.save()
        print(f'Pipeline {pipeline.name} disabled!')

        for s in s_ids:
            status = Statuses.objects.all().get(status_id=s, pipeline_id=id)
            status.is_exists = False
            status.save()
            print(f"Status {status.name} disabled!")
