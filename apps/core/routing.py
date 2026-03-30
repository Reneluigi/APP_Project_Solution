from django.urls import reverse

from apps.core.models import CustomUser


def home_url_for_user(user: CustomUser) -> str:
    if user.role == CustomUser.Role.SUPER_ADMIN:
        return reverse("dashboard:superadmin")
    if user.role == CustomUser.Role.ADMIN:
        return reverse("dashboard:company_admin")
    return reverse("dashboard:user_app")
