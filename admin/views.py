from django.shortcuts import render

from home.models import Pipelines


def enter_secret_code_page(request):
    return render(request, 'admin/enter_secret_code.html')


def subscriptions(request):
    return render(request, 'admin/subscriptions.html')


def translations(request):
    return render(request, 'admin/translations.html')


def user(request):
    d = dict(request.GET.items())
    pipeline = d['pipeline']
    pipeline = Pipelines.objects.get(user=request.user, p_id=pipeline)
    knowledge_mode = pipeline.knowledge_mode
    return render(request, 'admin/user.html', {
        'pipeline_id': pipeline.p_id,
        'file_link': knowledge_mode.database_link,
        'upload_file_inputs': [
            {'action': f'/api/v1/update-mode-file-link/?pipeline_id={pipeline.p_id}&mode_name='
                       f'knowledge&redirect_url=/knowledge-mode/?pipeline={pipeline.p_id}',
             'text': 'Ссылка на базу знаний', 'file_link': knowledge_mode.database_link},
        ], })

    """
        return render(request, 'admin/user.html', {
            'upload_file_inputs': [
                {'action': 'Fff',
                 'text': 'Ссылка на базу данных', 'file_link': 'FF'},
            ],
        })
    """


def users(request):
    return render(request, 'admin/users.html')
