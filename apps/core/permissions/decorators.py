from functools import wraps

from django.contrib.auth import get_user_model
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from apps.core.routing import home_url_for_user

from .helpers import get_real_user

User = get_user_model()


def super_admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        real_user = get_real_user(request)
        if not real_user.is_authenticated:
            return redirect_to_login(next=request.get_full_path())
        if real_user.role != User.Role.SUPER_ADMIN:
            raise PermissionDenied
        if getattr(request, "is_impersonating", False):
            return redirect(home_url_for_user(request.user))
        return view_func(request, *args, **kwargs)

    return _wrapped


def super_admin_real_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        real_user = get_real_user(request)
        if not real_user.is_authenticated:
            return redirect_to_login(next=request.get_full_path())
        if real_user.role != User.Role.SUPER_ADMIN:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(next=request.get_full_path())
        if request.user.role != User.Role.ADMIN:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped


def user_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(next=request.get_full_path())
        if request.user.role != User.Role.USER:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped
