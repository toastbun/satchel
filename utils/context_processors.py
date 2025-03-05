from django.conf import settings


def theme_context(request):
    default_theme = settings.THEME

    if not request.session.get("theme"):
        request.session["theme"] = default_theme

    return {
        "theme": request.session.get("theme"),
        "dark_mode": request.session.get("theme", default_theme)
    }


def navbar_is_active_context(request):
    if not request.session.get("navbar_is_active"):
        request.session["navbar_is_active"] = False

    return {
        "navbar_is_active": request.session.get("navbar_is_active")
    }