from django import forms

class NewItem(forms.Form):
    item_name = forms.CharField(label="Item name", max_length=512)