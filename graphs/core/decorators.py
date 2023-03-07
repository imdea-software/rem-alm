from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

def verify_user_profile(view_func):
    def wrap(request, *args, **kwargs):
        try:
            if request.user.profile:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, "error/profile_error.html")
        except ObjectDoesNotExist:
            message = (f"El usuario: {request.user.username} ha intentado realizar una acción para la que no tiene permisos.")
            return render(request, "error/profile_error.html")

    return wrap