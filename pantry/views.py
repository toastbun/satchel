import json
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from base.utils import ModelEncoder
from pantry.models import *
from pantry.forms import *


def index(request):
    context = {"page_name": "pantry_index"}

    return render(request, "pantry/index.html", context)


def ingredients(request):
    context = {
        "page_name": "ingredients",
        "ingredients_list": Ingredient.objects.all(),
        "items_list": Item.objects.all(),
    }

    if request.POST:
        form = NewIngredientForm(request.POST)

        if form.is_valid():
            form.save()

            context["form"] = NewIngredientForm()
        else:
            context["form"] = form

            return HttpResponseRedirect(reverse("pantry:ingredients"))
        
        return HttpResponseRedirect(reverse("pantry:ingredients"))
    else:
        context["form"] = NewIngredientForm()
    
    return render(request, "pantry/ingredients.html", context)


def detail_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)

    return render(request, "pantry/detail_ingredient.html", {"ingredient": ingredient})


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


def items(request):
    ingredients_list = Ingredient.objects.all()
    items_list = Item.objects.all()

    context = {
        "page_name": "items",
        "ingredients_list": ingredients_list,
        "items_list": items_list,
    }

    return render(request, "pantry/items.html", context)


def detail_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    return render(request, "pantry/detail_item.html", {"item": item})
