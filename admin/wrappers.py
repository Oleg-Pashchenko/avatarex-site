from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from home.models import AmoConnect
from home.tinkoff import get_person_info


def admin_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_success = request.session.get('admin_auth', False)
        if auth_success:
            return view_func(request, *args, **kwargs)
        else:

            messages.warning(request, 'Пожалуйста, оплатите подписку!')
            return redirect('/admin/')

    return _wrapped_view