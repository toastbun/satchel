from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *


def index(request):
    return render(request, "pantry/index.html")

def all_items(request):
    print(f"Made it to all_items.")
    print(request.POST)

    item_list = Item.objects.all()

    context = {
        "item_list": item_list,
    }

    return render(request, "pantry/all_items.html", context)


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, "pantry/detail.html", {"item": item})


def new_item(request):
    if request.method != "POST":
        return HttpResponseRedirect(redirect_to="/pantry/items")

    print(f"\nIt's a POST.")
    print(request.POST)
    form = NewItemForm(request.POST)

    if form.is_valid():
        print(f"It's valid.")
        form.save()

        print(f"Redirecting to /items.")
        return HttpResponseRedirect("/pantry/items")
    else:
        print(f"It ain't valid.")

        return render(
            request,
            template_name="pantry/all_items.html",
            context={
                "form": form
            }
        )