from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.core.middleware import SESSION_IMPERSONATE_USER_KEY
from apps.core.models import CustomUser
from apps.core.permissions.decorators import super_admin_real_required
from apps.core.routing import home_url_for_user

from .forms import LoginForm


class RoleAwareLoginView(LoginView):
    template_name = "core/login.html"
    redirect_authenticated_user = True
    authentication_form = LoginForm

    def get_success_url(self) -> str:
        return home_url_for_user(self.request.user)


def home_redirect(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect(reverse("core:login"))
    return redirect(home_url_for_user(request.user))


@require_POST
@super_admin_real_required
def impersonation_start(request: HttpRequest) -> HttpResponse:
    raw_id = request.POST.get("user_id")
    try:
        user_id = int(raw_id)
    except (TypeError, ValueError):
        return redirect(reverse("dashboard:superadmin"))

    target = get_object_or_404(CustomUser, pk=user_id, is_active=True)
    request.session[SESSION_IMPERSONATE_USER_KEY] = target.pk
    return redirect(home_url_for_user(target))


@require_POST
@super_admin_real_required
def impersonation_stop(request: HttpRequest) -> HttpResponse:
    request.session.pop(SESSION_IMPERSONATE_USER_KEY, None)
    return redirect(reverse("dashboard:superadmin"))
