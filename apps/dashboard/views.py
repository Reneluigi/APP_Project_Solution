from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from apps.core.models import CustomUser
from apps.core.permissions.decorators import admin_required, super_admin_required, user_required
from apps.core.permissions.helpers import user_must_match_company


@super_admin_required
def superadmin_dashboard(request: HttpRequest) -> HttpResponse:
    users = (
        CustomUser.objects.select_related("company")
        .filter(is_active=True)
        .order_by("role", "username")
    )
    return render(
        request,
        "dashboard/superadmin_dashboard.html",
        {"users": users},
    )


@login_required
@admin_required
def company_admin_dashboard(request: HttpRequest) -> HttpResponse:
    company = request.user.company
    user_must_match_company(request.user, company.id if company else None)
    return render(
        request,
        "dashboard/company_admin_dashboard.html",
        {"company": company},
    )


@login_required
@user_required
def user_dashboard(request: HttpRequest) -> HttpResponse:
    company = request.user.company
    user_must_match_company(request.user, company.id if company else None)
    return render(
        request,
        "dashboard/user_dashboard.html",
        {"company": company},
    )
