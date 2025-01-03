from django import forms
from django.forms import ModelForm
from .models import *

class NewItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name"]