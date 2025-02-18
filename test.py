#! /usr/bin/env python3

from pantry.models import *


# # first method
# corn = FoodItem(name="cheese")
# corn.save()

# second method
# FoodItem.objects.create(name="black beans")

all_items = FoodItem.objects.all()
print(all_items)