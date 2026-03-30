from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.core import views

app_name = "core"

urlpatterns = [
    path("", views.home_redirect, name="home"),
    path("login/", views.RoleAwareLoginView.as_view(), name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page="core:login"),
        name="logout",
    ),
    path("impersonate/start/", views.impersonation_start, name="impersonation_start"),
    path("impersonate/stop/", views.impersonation_stop, name="impersonation_stop"),
]
