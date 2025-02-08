from django import forms
from .models import *


class NewIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            "name",
            "temperature_controlled"
        ]

    def clean_name(self):
        return self.cleaned_data["name"].lower()

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "ingredient",
            "location",
            "date_expires"
        ]