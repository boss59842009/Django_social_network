from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def user_is_owner_required(object, redirect_url='info-profile'):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            owner = object(*args, **kwargs)
            if request.user != owner.user:
                return redirect(redirect_url, pk=owner.pk)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
