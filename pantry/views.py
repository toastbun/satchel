import json
from pprint import pprint
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from base.utils import ModelEncoder
from pantry.models import *
from pantry.forms import *
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


def search_ingredient_names(request):
    if request.method == "POST":
        request_body = json.loads(request.body)
        search_term = request_body.get("search_term")

        queryset_results = Ingredient.objects.filter(name__startswith=search_term.lower())
        response_data = [i.name for i in queryset_results]

        return HttpResponse(json.dumps(response_data))
    else:
        return redirect(reverse("pantry:ingredients"))


def ingredients(request):
    context = {
        "theme": request.session.get("theme"),
        "dark_mode": request.session.get("theme") == "dark",
        "page_name": "ingredients",
        "food_items_list": FoodItem.objects.all(),
        "food_substitutes_list": FoodSubstitute.objects.all(),
        "ingredients_list": Ingredient.objects.all().order_by("name"),
    }

    return render(request, "pantry/ingredients.html", context)


def add_ingredient(request):
    context = {
        "theme": request.session.get("theme"),
        "dark_mode": request.session.get("theme") == "dark",
        "page_name": "add_ingredient",
        "food_substitutes_list": FoodSubstitute.objects.all(),
        "food_items_list": FoodItem.objects.all(),
        "ingredients_list": Ingredient.objects.all().order_by("name"),
    }

    if request.POST:
        form = NewIngredientForm(request.POST)

        if form.is_valid():
            form.save()

            context["form"] = NewIngredientForm()

            return render(request, "pantry/add_ingredient.html", context)
        else:
            return HttpResponseRedirect(f"""/pantry/ingredients/add?ingredient_name={request.POST.get("name")}""")
    else:
        if ingredient_name := request.GET.get("ingredient_name"):
            context["form"] = NewIngredientForm({"name": ingredient_name})
        else:
            context["form"] = NewIngredientForm()

    return render(request, "pantry/add_ingredient.html", context)


def show_ingredient(request, ingredient_id):
    context = {
        "theme": request.session.get("theme"),
        "dark_mode": request.session.get("theme") == "dark",
        "page_name": "show_ingredient"
    }

    try:
        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    except Exception as e:
        if str(e) == "No Ingredient matches the given query.":
            context["page_name"] = "ingredients"
            context["food_items_list"] = FoodItem.objects.all()
            context["food_substitutes_list"] = FoodSubstitute.objects.all()
            context["ingredients_list"] = Ingredient.objects.all().order_by("name")

            # return render(request, "pantry/ingredients.html", context)
            return redirect(reverse("pantry:ingredients"), permanent=True)

    context["ingredient"] = ingredient

    return render(request, "pantry/show_ingredient.html", context=context)


def update_ingredient(request):
    if request.method != "POST":
        return redirect(reverse("pantry:ingredients"))

    ingredient_id = request.POST.get("ingredient_id")

    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)

    return show_ingredient(request, ingredient_id)


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
            "updated_records_list": [
                ModelEncoder().encode(ingredient) for ingredient in Ingredient.objects.all().order_by("name")
            ]
        }
    ))


def food_items(request):
    context = {
        "theme": request.session.get("theme"),
        "dark_mode": request.session.get("theme") == "dark",
        "page_name": "food_items",
        "food_items_list": FoodItem.objects.all().order_by("ingredient__name"),
        "ingredients_list": Ingredient.objects.all().order_by("name"),
        "packaging_types_exist": PackagingType.objects.count(),
    }

    if request.POST:
        print(request.POST)
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


def add_food_item(request):
    context = {
        "theme": request.session.get("theme"),
        "dark_mode": request.session.get("theme") == "dark",
        "page_name": "add_food_item",
        "food_items_list": FoodItem.objects.all().order_by("ingredient__name"),
        "ingredients_list": Ingredient.objects.all().order_by("name"),
    }

    if request.POST:
        request_data = {key: value for key, value in request.POST.items()}

        if selected_ingredient_name := request_data.get("ingredient"):
            try:
                request_data["ingredient"] = Ingredient.objects.get(name=selected_ingredient_name)
            except Ingredient.DoesNotExist:
                pass

        form = NewFoodItemForm(request_data)

        if form.is_valid():
            form.save()

            context["form"] = NewFoodItemForm()

            return HttpResponseRedirect(reverse("pantry:add_food_item"))
        else:
            context["form"] = form

        return render(request, "pantry/add_food_item.html", context)
    else:
        if ingredient_name := request.GET.get("ingredient_name"):
            context["form"] = NewFoodItemForm({"ingredient": ingredient_name})
        else:
            context["form"] = NewFoodItemForm()

    return render(request, "pantry/add_food_item.html", context)


def show_food_item(request, food_item_id):
    food_item = get_object_or_404(FoodItem, pk=food_item_id)

    context = {
        "theme": request.session.get("theme"),
        "dark_mode": request.session.get("theme") == "dark",
        "food_item": food_item
    }

    return render(request, "pantry/show_food_item.html", context=context)
