import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render


def index(request):
    context = {
       "dark_mode": request.session.get("theme") == "dark",
    }

    return render(request, "home.html", context=context)



def switch_theme(request):
    if request.method == "POST":
        if not request.session.get("theme"):
            request.session["theme"] = "light"
        else:
            request.session["theme"] = "light" if request.session["theme"] == "dark" else "dark"

        return HttpResponse(json.dumps("Success!"))