import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse


def index(request):
    context = {
        "theme": request.session.get("theme"),
        "dark_mode": request.session.get("theme") == "dark",
    }

    return render(request, "home.html", context=context)



def switch_theme(request):
    response = {
        "message": "Invalid request."
    }

    if request.method == "POST":
        requested_theme = request.session.get("theme")

        if not requested_theme:
            request.session["theme"] = "light"
        else:
            request.session["theme"] = "light" if requested_theme == "dark" else "dark"
        
        response = {
            "message": "Success"
        }

    return HttpResponse(json.dumps(response))


def toggle_navbar(request):
    if request.method != "POST":
        return redirect(reverse(""))
    
    request_body = json.loads(request.body)
    navbar_is_active = request_body.get("active")

    request.session["navbar_is_active"] = navbar_is_active

    return HttpResponse(json.dumps({"message": "Success"}))