from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *


def index(request):
    return render(request, "pantry/index.html")

def allitems(request):
    item_list = Item.objects.all()
    context = {
        "item_list": item_list,
    }
    return render(request, "pantry/allitems.html",context)


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, "pantry/detail.html", {"item": item})


def newitem(request):
    # Item.objects.all().delete()
    if request.method == "POST":
        form = NewItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/pantry/items")
    else: 
        form = NewItemForm()
    
    return render(request, "pantry/newitem.html", {"form": form})