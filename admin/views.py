from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from admin.wrappers import admin_auth_required
from home.models import Pipelines, AvatarexSettings, AmoRegisterTry


def enter_secret_code_page(request):
    if request.method == 'POST':
        password = request.POST.dict()['password']
        if password == '991155':
            request.session['admin_auth'] = True
            return redirect('/admin/users')
    return render(request, 'admin/enter_secret_code.html')


def subscriptions(request):
    return render(request, 'admin/subscriptions.html')


def translations(request):
    return render(request, 'admin/translations.html')

@admin_auth_required

def auth_try(request):
    return render(request, 'admin/auth_try.html', {'attempts': AmoRegisterTry.objects.all()})


@admin_auth_required
def user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    pipelines = Pipelines.objects.filter(user=User.objects.get(id=user_id))
    return render(request, 'admin/user.html', {'user': user, 'pipelines': pipelines})

@admin_auth_required
def users(request):
    all_users = User.objects.all()

    return render(request, 'admin/users.html', {'users': all_users})

@admin_auth_required
def widget(request):
    settings = AvatarexSettings.objects.get(id=2)
    if request.method == 'POST':
        d = request.POST.dict()
        settings.knowledge_link = d['knowledge_link']
        settings.context = d['context']
        settings.api_token = d['api_token']
        settings.error_message = d['error_message']
        settings.save()

    return render(request, 'admin/widget.html', {"settings": settings})
