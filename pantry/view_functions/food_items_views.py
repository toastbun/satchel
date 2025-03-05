from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from pantry.forms import NewFoodItemForm
from pantry.models import FoodItem, Ingredient, PackagingType


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