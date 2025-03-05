import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from base.utils import ModelEncoder
from pantry.forms import NewIngredientForm
from pantry.models import FoodItem, FoodSubstitute, GroceryType, Ingredient


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