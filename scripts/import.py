#! /usr/bin/env

import json
from pantry.models import Item

Item.objects.all().delete()

file = "data\items.json"

with open(file, 'r') as data:
    items = json.load(data)

for i in items:
    Item.objects.create(
        name=i["name"]
    )
#     new_item = Item(name=i.get("name"))
#     new_item.save()

# Item.objects.bulk_create(
#     [
#         Item(name=i.get("name")) for i in items
#     ]
# )