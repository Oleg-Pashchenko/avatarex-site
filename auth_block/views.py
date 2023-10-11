from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from home.views import home
from .forms import UserRegisterForm, UserLoginForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, f'Создан аккаунт {username}!')
            form.clean()
            return redirect(home)
        else:
            messages.warning(request, "Ошибка заполнения формы!")
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if not form.is_valid():
            messages.warning(request, 'Некорректно заполнена форма!')
        else:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            if username and password:
                user = authenticate(request, username=username, password=password)
                if not user:
                    messages.warning(request, 'Ошибка входа!')
                else:
                    messages.success(request, 'Вход успешен!')
                    login(request, user)
                    return redirect(home)
    else:
        form = UserLoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout(request):
    pass
