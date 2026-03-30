from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

User = get_user_model()


def get_real_user(request):
    return getattr(request, "real_user", request.user)


def resolve_company_id_for_user(user) -> int | None:
    if not user.is_authenticated:
        return None
    if user.role == User.Role.SUPER_ADMIN:
        return None
    return user.company_id


def user_must_match_company(user, company_id: int | None) -> None:
    if user.role == User.Role.SUPER_ADMIN:
        return
    if company_id is None or user.company_id != company_id:
        raise PermissionDenied
