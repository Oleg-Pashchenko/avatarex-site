from django.shortcuts import render


def enter_secret_code_page(request):
    return render(request, 'admin/enter_secret_code.html')


def subscriptions(request):
    return render(request, 'admin/subscriptions.html')


def translations(request):
    return render(request, 'admin/translations.html')


def user(request):
    return render(request, 'admin/user.html')


def users(request):
    return render(request, 'admin/users.html')
