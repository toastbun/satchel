import json
from pprint import pprint
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from base.utils import ModelEncoder
from pantry.api import *
from pantry.models import *
from pantry.forms import *
from pantry.view_functions.food_items_views import *
from pantry.view_functions.grocery_list_views import *
from pantry.view_functions.ingredients_views import *
from scripts.import_csvs import import_csvs


def index(request):
    context = {
        "theme": request.session.get("theme"),
        "dark_mode": request.session.get("theme") == "dark",
        "page_name": "pantry_index"
    }

    return render(request, "pantry/index.html", context)


def reset_database(request):
    import_csvs()

    return redirect(reverse("pantry:ingredients"))


def get_grocery_types(request):
    if request.method != "POST":
        print(f"views.get_grocery_types | Handle this case.")

        return HttpResponse(json.dumps({"success": False}))
    
    """
    expecting:

    {
        names: true,

    }
    """
    
    request_body = json.loads(request.body)
    names_only = request_body.get("names")

    grocery_types = get_all_grocery_types(names=names_only)

    return HttpResponse(json.dumps(grocery_types))


def get_food_substitutes(request):
    if request.method != "POST":
        print(f"views.get_food_substitutes | Handle this case.")

        return HttpResponse(json.dumps({"success": False}))
    
    """
    expecting:

    {
        names: true,
    }
    """
    
    request_body = json.loads(request.body)
    names_only = request_body.get("names")

    food_substitutes = get_all_food_substitutes(names=names_only)

    return HttpResponse(json.dumps(food_substitutes))


def search_ingredient_names(request):
    if request.method != "POST":
        return redirect(reverse("pantry:ingredients"))

    request_body = json.loads(request.body)
    search_term = request_body.get("search_term")

    queryset_results = Ingredient.objects.filter(name__startswith=search_term.lower()).order_by("name")
    response = [i.name for i in queryset_results]

    return HttpResponse(json.dumps(response))