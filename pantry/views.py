from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *


def index(request):
    return render(request, "pantry/index.html")

def all_items(request):
    item_list = Item.objects.all()
    context = {
        "item_list": item_list,
    }
    return render(request, "pantry/all_items.html",context)


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, "pantry/detail.html", {"item": item})


def new_item(request):
    if request.method == "POST":
        form = NewItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/pantry/items")
    else: 
        form = NewItemForm()
    
    return render(request, "pantry/new_item.html", {"form": form})