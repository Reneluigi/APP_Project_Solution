from django.urls import path

from apps.dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("superadmin/", views.superadmin_dashboard, name="superadmin"),
    path("company-admin/", views.company_admin_dashboard, name="company_admin"),
    path("app/", views.user_dashboard, name="user_app"),
]
