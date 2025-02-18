import json
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from base.utils import ModelEncoder
from pantry.models import *
from pantry.forms import *


def index(request):
    context = {
        "dark_mode": request.session.get("theme") == "dark",
        "page_name": "pantry_index"
    }

    return render(request, "pantry/index.html", context)


def search_food_substitutes(request):
    if request.method == "POST":
        request_body = json.loads(request.body)
        search_term = request_body.get("search_term")

        queryset_results = FoodSubstitute.objects.filter(name__startswith=search_term.lower())
        response_data = [i.name for i in queryset_results]

        return HttpResponse(json.dumps(response_data))
    else:
        return redirect(reverse("pantry:ingredients"))


def ingredients(request):
    context = {
        "dark_mode": request.session.get("theme") == "dark",
        "page_name": "ingredients",
        "ingredients_list": Ingredient.objects.all(),
        "food_substitutes_list": FoodSubstitute.objects.all(),
        "food_items_list": FoodItem.objects.all(),
    }

    if request.POST:
        form = NewIngredientForm(request.POST)

        if form.is_valid():
            form.save()

            context["form"] = NewIngredientForm()

            return render(request, "pantry/ingredients.html", context)
        else:
            return HttpResponseRedirect(f"""/pantry/ingredients?food_substitute={request.POST.get("food_substitute")}""")
    else:
        if food_substitute := request.GET.get("food_substitute"):
            context["form"] = NewIngredientForm({"food_substitute": food_substitute})
        else:
            context["form"] = NewIngredientForm()

    return render(request, "pantry/ingredients.html", context)


def show_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)

    context = {
        "dark_mode": request.session.get("theme") == "dark",
        "ingredient": ingredient
    }

    return render(request, "pantry/show_ingredient.html", context=context)


def delete_ingredient(request):
    request_body = json.loads(request.body)

    response = {"success": False}

    record_id = request_body.get("record_id")

    if not type(record_id) == str or not record_id.isnumeric():
        error_message = f"views.delete_ingredient | Request body does not contain a valid record_id: {request_body}"
        print(error_message)

        response["message"] = error_message

        return HttpResponse(json.dumps(response))
    
    Ingredient.objects.get(pk=int(record_id)).delete()

    return HttpResponse(json.dumps(
        {
            "success": True,
            "updated_records_list": [ModelEncoder().encode(ingredient) for ingredient in Ingredient.objects.all()]
        }
    ))


def food_items(request):
    context = {
        "dark_mode": request.session.get("theme") == "dark",
        "page_name": "food_items",
        "ingredients_list": Ingredient.objects.all(),
        "food_items_list": FoodItem.objects.all(),
    }

    if request.POST:
        form = NewFoodItemForm(request.POST)

        if form.is_valid():
            form.save()

            context["form"] = NewFoodItemForm()
        else:
            context["form"] = form

            return HttpResponseRedirect(reverse("pantry:food_items"))
        
        return HttpResponseRedirect(reverse("pantry:food_items"))
    else:
        context["form"] = NewFoodItemForm()
    
    return render(request, "pantry/food_items.html", context)


def show_food_item(request, food_item_id):
    food_item = get_object_or_404(FoodItem, pk=food_item_id)

    context = {
        "dark_mode": request.session.get("theme") == "dark",
        "food_item": food_item
    }

    return render(request, "pantry/show_food_item.html", context=context)
