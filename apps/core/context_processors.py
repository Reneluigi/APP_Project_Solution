def impersonation(request):
    return {
        "is_impersonating": getattr(request, "is_impersonating", False),
    }
