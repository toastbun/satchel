from django import forms
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from pantry.models import *


class DateInput(forms.DateInput):
    input_type = "date"


class NewIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "substitute_key"]
        widgets = {
            "name": forms.TextInput(),
            "substitute_key": forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super(NewIngredientForm, self).__init__(*args, **kwargs)

        self.fields["name"].label = ""  # remove input label
        self.fields["name"].widget.attrs.update({"placeholder": "Ingredient name"})  # add placeholder text to text input
        self.fields["name"].widget.attrs.update({"autofocus": "", "onfocus": "this.select()"})  # auto-focus text field when page loads
    
        self.fields["substitute_key"].label = ""  # remove input label
        self.fields["substitute_key"].widget.attrs.update({"placeholder": "Substitute key"})  # add placeholder text to text input
        self.fields["substitute_key"].widget.attrs.update({"class": "autocomplete"})  # make text input autocomplete


class NewFoodItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewFoodItemForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FoodItem
        fields = [
            "ingredient",
            "packaging_type",
            "location",
            "date_expires",
        ]
        widgets = {
            "date_expires": DateInput()
        }