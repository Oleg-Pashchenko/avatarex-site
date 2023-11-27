from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from home.models import AmoConnect
from home.tinkoff import get_person_info


def sub_active_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        owner_id = request.user.id  # Assuming the user ID is stored in 'request.user.id'
        days, _ = get_person_info(owner_id)

        if days > 0:
            # If subscription is active, proceed with the original view function
            return view_func(request, *args, **kwargs)
        else:
            instance = AmoConnect.objects.filter(user=request.user.id).first()
            if not instance:
                return redirect('/amo-register')
            else:
                messages.warning(request, 'Пожалуйста, оплатите подписку!')
                return redirect('/payment')

    return _wrapped_view