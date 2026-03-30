from django.contrib.auth import get_user_model

User = get_user_model()

SESSION_IMPERSONATE_USER_KEY = "impersonate_user_id"


class ImpersonationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        real_user = getattr(request, "user", None)
        request.real_user = real_user
        request.is_impersonating = False

        if real_user is not None and real_user.is_authenticated:
            target_id = request.session.get(SESSION_IMPERSONATE_USER_KEY)
            if target_id is not None and real_user.role == User.Role.SUPER_ADMIN:
                try:
                    target = User.objects.select_related("company").get(
                        pk=target_id,
                        is_active=True,
                    )
                except (User.DoesNotExist, ValueError, TypeError):
                    request.session.pop(SESSION_IMPERSONATE_USER_KEY, None)
                else:
                    request.user = target
                    request.is_impersonating = True
            elif target_id is not None:
                request.session.pop(SESSION_IMPERSONATE_USER_KEY, None)

        return self.get_response(request)
