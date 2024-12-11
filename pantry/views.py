from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, ugly.")

def sup(request):
    name = request.GET.get("name")
    response = "guy"

    if name != None:
        response = name

    return HttpResponse("Hi " + response + " : )")