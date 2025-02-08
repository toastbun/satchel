from pantry.models import Ingredient, Location


items = [
    {
        "ingredient": Ingredient.objects.filter(name="corn"),
        "location": Location.objects.filter(name="snack cupboard"),
        "date_expires": "2025-05-12"
    }
]