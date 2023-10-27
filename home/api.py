import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from home.models import Pipelines

import gdown


@login_required
def database_mode_update(request):
    data = json.loads(request.body.decode('utf-8'))

    qualification_fields = data['qualification_fields']
    bounded_situations_fields = data['bounded_situations_fields']
    database_mode_fields = data['database_mode_fields']
    view_rule = data['view_rule']
    result_count = int(data['result_count'])
    pipeline_id = int(data['pipeline_id'])

    pipeline = Pipelines.objects.get(p_id=pipeline_id)
    pipeline.search_mode.qualification.value = qualification_fields
    pipeline.search_mode.mode_messages.hi_message = bounded_situations_fields['hi_message']
    pipeline.search_mode.mode_messages.openai_error_message = bounded_situations_fields['openai_error_message']
    pipeline.search_mode.mode_messages.database_error_message = bounded_situations_fields['database_error_message']
    pipeline.search_mode.mode_messages.service_settings_error_message = bounded_situations_fields[
        'service_settings_error_message']
    pipeline.search_mode.search_rules = database_mode_fields
    pipeline.search_mode.view_rule = view_rule
    pipeline.search_mode.results_count = result_count
    pipeline.save()
    return redirect(f"/database-mode/?pipeline_id={pipeline_id}")


@login_required
def knowledge_mode_update(request):
    data = json.loads(request.body.decode('utf-8'))
    qualification_fields = data['qualification_fields']
    bounded_situations_fields = data['bounded_situations_fields']
    pipeline_id = int(data['pipeline_id'])
    pipeline = Pipelines.objects.get(p_id=pipeline_id)
    pipeline.knowledge_mode.qualification.value = qualification_fields
    pipeline.knowledge_mode.mode_messages.hi_message = bounded_situations_fields['hi_message']
    pipeline.knowledge_mode.mode_messages.openai_error_message = bounded_situations_fields['openai_error_message']
    pipeline.knowledge_mode.mode_messages.database_error_message = bounded_situations_fields['database_error_message']
    pipeline.knowledge_mode.mode_messages.service_settings_error_message = bounded_situations_fields[
        'service_settings_error_message']
    pipeline.save()
    return redirect(f"/knowledge-mode/?pipeline_id={pipeline_id}")


@login_required
def d_k_m_update(request):
    data = json.loads(request.body.decode('utf-8'))

    qualification_fields = data['qualification_fields']
    bounded_situations_fields = data['bounded_situations_fields']
    database_mode_fields = data['database_mode_fields']
    view_rule = data['view_rule']
    result_count = int(data['result_count'])
    pipeline_id = int(data['pipeline_id'])

    pipeline = Pipelines.objects.get(p_id=pipeline_id)
    pipeline.knowledge_and_search_mode.qualification.value = qualification_fields
    pipeline.knowledge_and_search_mode.mode_messages.hi_message = bounded_situations_fields['hi_message']
    pipeline.knowledge_and_search_mode.mode_messages.openai_error_message = bounded_situations_fields[
        'openai_error_message']
    pipeline.knowledge_and_search_mode.mode_messages.database_error_message = bounded_situations_fields[
        'database_error_message']
    pipeline.knowledge_and_search_mode.mode_messages.service_settings_error_message = bounded_situations_fields[
        'service_settings_error_message']
    pipeline.knowledge_and_search_mode.search_rules = database_mode_fields
    pipeline.knowledge_and_search_mode.view_rule = view_rule
    pipeline.knowledge_and_search_mode.results_count = result_count
    pipeline.save()
    return redirect(f"/database-and-knowledge-mode/?pipeline_id={pipeline_id}")


@login_required
def prompt_mode_update(request):
    data = json.loads(request.body.decode('utf-8'))
    context = data['context']
    tokens_limit = int(data['tokens_limit'])
    temperature = float(data['temperature'])
    model = data['model']
    qualification_fields = data['qualification_fields']

    pipeline_id = int(data['pipeline_id'])
    pipeline = Pipelines.objects.get(p_id=pipeline_id)
    pipeline.prompt_mode.context = context
    pipeline.prompt_mode.max_tokens = tokens_limit
    pipeline.prompt_mode.temperature = temperature
    pipeline.prompt_mode.model = model
    pipeline.prompt_mode.qualification.value = qualification_fields
    pipeline.save()
    return redirect(f"/prompt-mode/?pipeline_id={pipeline_id}")


@login_required
def database_mode_update_file_link(request):
    data = json.loads(request.body.decode('utf-8'))

    pipeline_id = data['pipeline_id']
    google_drive_url = request.POST.dict()['filename']
    file_id = google_drive_url.split("/")[-2]

    try:
        download_url = f"https://drive.google.com/uc?id={file_id}"
        output_path = f"uploads/{file_id}.xlsx"
        gdown.download(download_url, output_path, quiet=True)
    except:
        return redirect(f'/database-mode/?pipeline_id={pipeline_id}')

    pipeline = Pipelines.objects.get(p_id=pipeline_id)
    pipeline.search_mode.database_link = output_path.split('/')[1]
    pipeline.save()
    # messages.success(request, 'Данные обновлены!')
    return redirect(f'/database-mode/?pipeline_id={pipeline_id}')


@login_required
def knowledge_mode_update_file_link(request):
    data = json.loads(request.body.decode('utf-8'))

    pipeline_id = data['pipeline_id']
    google_drive_url = request.POST.dict()['filename']
    file_id = google_drive_url.split("/")[-2]

    try:
        download_url = f"https://drive.google.com/uc?id={file_id}"
        output_path = f"uploads/{file_id}.xlsx"
        gdown.download(download_url, output_path, quiet=True)
    except:
        return redirect(f'/database-mode/?pipeline_id={pipeline_id}')

    pipeline = Pipelines.objects.get(p_id=pipeline_id)
    pipeline.knowledge_mode.database_link = output_path.split('/')[1]
    pipeline.save()
    # messages.success(request, 'Данные обновлены!')
    return redirect(f'/database-mode/?pipeline_id={pipeline_id}')


@login_required
def d_k_m_update_database_link(request):
    pass


@login_required
def d_k_m_update_knowledge_link(request):
    pass


@login_required
def update_openai_key(request):
    pass


@login_required
def sync_amo_pipelines(request):
    pass


@login_required
def update_working_mode(request):
    pass


@login_required
def get_stages_by_pipeline(request):
    pass
