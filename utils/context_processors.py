from django.conf import settings


def theme_context(request):
    default_theme = settings.THEME

    if not request.session.get("theme"):
        request.session["theme"] = default_theme

    return {
        "theme": request.session.get("theme"),
        "dark_mode": request.session.get("theme", default_theme)
    }