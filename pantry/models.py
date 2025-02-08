from django.db import models
from pantry.enums import *


class Location(models.Model):
    name = models.CharField(max_length=512, unique=True, null=False)
    room = models.CharField(max_length=64, null=False, default=Rooms.KITCHEN, choices=Rooms.choices)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(room__in=Rooms.values),
                name="room_exists",
            )
        ]

class Ingredient(models.Model):
    name = models.CharField(max_length=512, unique=True, null=False)
    temperature_controlled = models.BooleanField(null=True)


class Item(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingredient_items")
    location = models.ForeignKey(Location,on_delete=models.CASCADE, related_name="location_items", null=True)
    date_expires = models.DateField(null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.ingredient.name