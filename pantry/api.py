from pantry.models import *


def get_all_grocery_types(names=False):
    all_grocery_types = GroceryType.objects.all().order_by("name")

    response_data = [i.name for i in all_grocery_types] if names else [i for i in all_grocery_types]
    response_data.insert(0, None)

    return response_data


def get_all_food_substitutes(names=False):
    all_food_substitutes = FoodSubstitute.objects.all().order_by("name")
    
    response_data = [i.name for i in all_food_substitutes] if names else [i for i in all_food_substitutes]
    response_data.insert(0, None)

    return response_data