from pantry.models import *


# # first method
# corn = Item(name="cheese")
# corn.save()

# second method
# Item.objects.create(name="black beans")

all_items = Item.objects.all()
print(all_items)