from pantry.models import Ingredient, Location, PackagingType


items = [
    {
        "ingredient": Ingredient.objects.filter(name="corn"),
        "location": Location.objects.filter(name="freezer"),
        "packaging_types": PackagingType.objects.filter(name="bag"),
        "date_expires": "2025-05-12"
    }, {
        "ingredient": Ingredient.objects.filter(name="corn"),
        "location": Location.objects.filter(name="freezer"),
        "packaging_types": PackagingType.objects.filter(name="bag"),
        "date_expires": "2025-05-12"
    }, {
        "ingredient": Ingredient.objects.filter(name="peas"),
        "location": Location.objects.filter(name="freezer"),
        "packaging_types": PackagingType.objects.filter(name="bag"),
        "date_expires": "2025-05-12"
    }, {
        "ingredient": Ingredient.objects.filter(name="peas"),
        "location": Location.objects.filter(name="freezer"),
        "packaging_types": PackagingType.objects.filter(name="bag"),
        "date_expires": "2025-05-19"
    }, {
        "ingredient": Ingredient.objects.filter(name="peas"),
        "location": Location.objects.filter(name="freezer"),
        "packaging_types": PackagingType.objects.filter(name="bag"),
        "date_expires": "2025-06-09"
    }, {
        "ingredient": Ingredient.objects.filter(name="fruit snacks"),
        "location": Location.objects.filter(name="cabinet"),
        "packaging_types": PackagingType.objects.filter(name="box"),
        "date_expires": "2025-05-12"
    }
]