#! /usr/bin/env

import os
import sys


ROOT_PATH = os.getcwd()


# reset database
os.system("dropdb satcheldb")
os.system("createdb satcheldb")
os.system(f"rm {ROOT_PATH}/pantry/migrations/00*.py")
os.system("python3 manage.py makemigrations")
os.system("python3 manage.py migrate")


from data.ingredients import ingredients
from data.food_items import food_items
from data.food_substitutes import food_substitutes
from data.locations import locations
from data.packaging_types import packaging_types
from pantry.enums import *
from pantry.models import *



# the order of this dictionary matters because some tables need to be created before others due to their field references.
# for example, Location and Ingredient records need to exist by the time Item records reference them upon creation.
data = {
    Location: locations,
    PackagingType: packaging_types,
    FoodSubstitute: food_substitutes,
    Ingredient: ingredients,
    FoodItem: food_items,
}

[model.objects.all().delete() for model in data]

for model in data:
    for record in data[model]:
        new_record = model()

        for field_name, field_value in record.items():
            if type(field_value) is models.query.QuerySet:
                # single records are referenced using QuerySets in the data files
                # this is because QuerySets are not evaluated until the moment they are accessed
                # and the records don't exist yet when the data files are imported.
                # TODO -- if the time comes where QuerySets are used as field values, re-evaluate this system.
                field_value = field_value[0]

            setattr(new_record, field_name, field_value)

        new_record.save()
    
    total_records = model.objects.count()

    print(f"{model.__name__}: {total_records}")