from django.shortcuts import render

from pantry.models import GroceryListItem


def grocery_list(request):
    grocery_list_items = GroceryListItem.objects.all()

    context = {
        "theme": request.session.get("theme"),
        "dark_mode": request.session.get("theme") == "dark",
        "grocery_list_items": grocery_list_items,
        "page_name": "grocery_list",
    }

    return render(request, "pantry/grocery_list.html", context=context)


def add_grocery_list_item(request):
    
    if request.method == "GET":
        grocery_list_items = GroceryListItem.objects.all()

        context = {
            "theme": request.session.get("theme"),
            "dark_mode": request.session.get("theme") == "dark",
            "grocery_list_items": grocery_list_items
        }

    return render(request, "pantry/grocery_list.html", context=context)