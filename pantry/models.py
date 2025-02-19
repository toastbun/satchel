from django.db import models
from django.utils.translation import gettext_lazy as _

from pantry.enums import *


class Location(models.Model):
    name = models.CharField(max_length=512, unique=True, null=False)
    room = models.CharField(max_length=64, null=False, default=Rooms.KITCHEN, choices=Rooms.choices)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(room__in=Rooms.values),
                name="room_exists",
            )
        ]


class GroceryType(models.Model):
    name = models.CharField(max_length=512, unique=True, null=False)

    def __str__(self):
        return self.name


class PackagingType(models.Model):
    name = models.CharField(max_length=512, unique=True, null=False)

    def __str__(self):
        return self.name


class FoodSubstitute(models.Model):
    name = models.CharField(max_length=512, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    grocery_type = models.ForeignKey(GroceryType, on_delete=models.SET_NULL, related_name="grocery_type_items", null=True)
    substitute_key = models.ForeignKey(FoodSubstitute, on_delete=models.SET_NULL, null=True, default=None, related_name="food_substitute_ingredients")

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingredient_items")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name="location_items", null=True)
    packaging_type = models.ForeignKey(PackagingType, on_delete=models.SET_NULL, related_name="packaging_type_items", null=True)
    multi_use = models.BooleanField(default=False, choices=((True, "Yes"), (False, "No")))
    amount_left = models.CharField(max_length=64, null=True, default=AmountsLeft.HIGH, choices=AmountsLeft.choices)
    quantity = models.PositiveSmallIntegerField(default=1)
    date_expires = models.DateField(null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.ingredient.name

    def get_substitutes(self):
        substitute_key = self.ingredient.substitute_key

        return substitute_key
    
    def set_location(self, ingredient_name, location_name, quantity):
        print(f"""Entered FoodItem.set_location | Moving {quantity} {ingredient_name} items to location "{location_name}".""")


class GroceryListItem(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingredient_grocery_list_items")


class IngredientTag(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingredient_tags")
    tag = models.CharField(max_length=64, null=False)