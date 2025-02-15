from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class NewIngredientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewIngredientForm, self).__init__(*args, **kwargs)

        # remove labels
        self.fields["name"].label = ""

        # add placeholder text to text inputs
        self.fields["name"].widget.attrs.update({"placeholder": "Ingredient name"})

        # auto-focus name field when page loads
        self.fields["name"].widget.attrs.update({"autofocus": "", "onfocus": "this.select()"})

    def clean_name(self):
        return self.cleaned_data["name"].lower()

    class Meta:
        model = Ingredient
        fields = [
            "name",
        ]
        labels = {
            "name": None,
        }


class NewItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewItemForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Item
        fields = [
            "ingredient",
            "packaging_type",
            "location",
            "date_expires",
        ]
        widgets = {
            "date_expires": DateInput()
        }