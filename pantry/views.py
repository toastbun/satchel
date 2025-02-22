import json
from pprint import pprint
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from base.utils import ModelEncoder
from pantry.api import *
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

    print(f"NAMES_ONLY: {names_only}")

    print("GROCERY_TYPES:")
    print(grocery_types)

    return HttpResponse(json.dumps(grocery_types))


def get_food_substitutes(request):
    print(f"HIT FOOD SUBS")
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

    print(f"FOOD_SUBSTITUTES:")
    print(food_substitutes)

    return HttpResponse(json.dumps(food_substitutes))


def search_ingredient_names(request):
    if request.method == "POST":
        request_body = json.loads(request.body)
        search_term = request_body.get("search_term")

        queryset_results = Ingredient.objects.filter(name__startswith=search_term.lower()).order_by("name")
        response = [i.name for i in queryset_results]

        return HttpResponse(json.dumps(response))
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
    
    response = {
        "updated": []
    }
    
    request_body = json.loads(request.body)

    print("\n")
    print(f"REQUEST:")
    print(request_body)
    print("\n")

    ingredient_id = request_body.get("record_id")
    update_data = request_body.get("update_data")

    if not type(ingredient_id) == str or not ingredient_id.isnumeric():
        error_message = f"views.update_ingredient | Request body does not contain a valid ingredient_id: {request_body}"
        print(error_message)

        response["message"] = error_message

        return HttpResponse(json.dumps(response))
    
    ingredient_id = int(ingredient_id)

    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)

    for property, value in update_data.items():
        print(f"{property} before update: {getattr(ingredient, property)}")

        print(f"Value: {value} | Type: {type(value)}")

        if value == None or value == "null":
            setattr(ingredient, property, None)

            response["updated"].append({property: value})
        else:
            # set related fields manually
            if property == "grocery_type":
                setattr(ingredient, property, GroceryType.objects.get(name=value))
            elif property == "substitute_key":
                setattr(ingredient, property, FoodSubstitute.objects.get(name=value))
            else:
                setattr(ingredient, property, value)

        ingredient.save()

    print(f"UPDATED NAME TO: {ingredient.name}")
    print(f"UPDATED GROCERY TYPE TO: {ingredient.grocery_type}")
    print(f"UPDATED SUBSTITUTE KEY TO: {ingredient.substitute_key}")
    
    print(f"WOOOOO!!!!\n")
    print(response)

    return HttpResponse(json.dumps(response))


def delete_ingredient(request):
    if request.method != "POST":
        return redirect(reverse("pantry:ingredients"))
    
    response = {"success": False}

    request_body = json.loads(request.body)

    ingredient_id = request_body.get("record_id")

    if not type(ingredient_id) == str or not ingredient_id.isnumeric():
        error_message = f"views.delete_ingredient | Request body does not contain a valid ingredient_id: {request_body}"
        print(error_message)

        response["message"] = error_message

        return HttpResponse(json.dumps(response))
    
    ingredient_id = int(ingredient_id)
    
    Ingredient.objects.get(pk=ingredient_id).delete()

    return HttpResponse(json.dumps(
        {
            "success": True,
            "updated_ingredients_list": [
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
