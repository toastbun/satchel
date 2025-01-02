from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import *

def index(request):
    item_list = Item.objects.all()
    context = {
        "item_list": item_list,
    }
    return render(request, "pantry/index.html",context)


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, "pantry/detail.html", {"item": item})

def newitem(request):
    return render(request, "pantry/newitem.html")