from django import forms
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from pantry.models import *


class DateInput(forms.DateInput):
    input_type = "date"

class NewIngredientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewIngredientForm, self).__init__(*args, **kwargs)

        self.fields["name"].label = ""
        self.fields["name"].widget.attrs.update({"placeholder": "Ingredient name"})
        self.fields["name"].widget.attrs.update({"autofocus": "", "onfocus": "this.select()"})

        self.fields["grocery_type"].required = False

        self.fields["substitute_key"].label = "Substitute category"  # remove input label
        self.fields["substitute_key"].required = False

    class Meta:
        model = Ingredient
        fields = ["name", "grocery_type", "substitute_key"]
        widgets = {
            "name": forms.TextInput(),
            "grocery_type": forms.Select(),
            "substitute_key": forms.Select()
        }


class NewFoodItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewFoodItemForm, self).__init__(*args, **kwargs)

        self.locations_exist = Location.objects.count()
        self.packaging_types_exist = PackagingType.objects.count()

        self.fields["ingredient"].label = ""
        self.fields["ingredient"].widget.attrs.update({"placeholder": "Ingredient name"})
        self.fields["ingredient"].widget.attrs.update({"autofocus": "", "onfocus": "this.select()"})
        self.fields["ingredient"].widget.attrs["class"] = "autocomplete"

        if self.packaging_types_exist:
            self.fields.append("packaging_type")
            self.fields["packaging_type"].required = False
    
    def clean_ingredient(self):
        print(f"\nEntered clean_ingredient.\n")
        ingredient_selection = self.cleaned_data["ingredient"]

        try:
            return Ingredient.objects.get(name=ingredient_selection)
        except Exception as e:
            raise forms.ValidationError("Ingredient does not exist.")

    def clean_date_expires(self):
        print(f"\nEntered clean_date_expires.")
        date_expires = self.cleaned_data["date_expires"]

        return date_expires

    class Meta:
        model = FoodItem
        fields = [
            "ingredient",
            "location",
            "multi_use",
            "quantity",
            "date_expires",
        ]
        widgets = {
            "ingredient": forms.TextInput(),
            "date_expires": DateInput()
        }