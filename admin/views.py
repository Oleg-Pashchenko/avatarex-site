from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from home.models import Pipelines


def enter_secret_code_page(request):
    return render(request, 'admin/enter_secret_code.html')


def subscriptions(request):
    return render(request, 'admin/subscriptions.html')


def translations(request):
    return render(request, 'admin/translations.html')


def user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    pipelines = Pipelines.objects.filter(user=User.objects.get(id=user_id))


    # Передаем данные в шаблон и отображаем страницу
    return render(request, 'admin/user.html', {'user': user, 'pipelines': pipelines, 'upload_file_inputs': [
        {'action': '',
         'text': 'Ссылка на базу знаний', 'file_link': 'nowledge_mode'},
    ]})


def users(request):
    all_users = User.objects.all()

    return render(request, 'admin/users.html', {'users': all_users})
