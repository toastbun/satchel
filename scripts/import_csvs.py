#! /usr/bin/env

import csv
import json
import os
import sys
from django.conf import settings
from django.db.models.base import ModelBase
from django.db.models.fields import BooleanField, PositiveSmallIntegerField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from pprint import pprint

from data import csvs
from pantry import models


ROOT_PATH = os.getcwd()

RESPONSES_POSITIVE = ["true", "yes", "t", "y", "1"]
RESPONSES_NEGATIVE = ["false", "no", "f", "n", "0"]


# reset database
os.system("dropdb satcheldb")
os.system("createdb satcheldb")
os.system(f"rm {ROOT_PATH}/pantry/migrations/00*.py")
os.system("python3 manage.py makemigrations")
os.system("python3 manage.py migrate")


def get_models_to_import():
    model_import_map = {
        "models": [],
        "models_with_foreign_keys": []
    }

    for value in models.__dict__.values():
        if type(value) == ModelBase:
            if not any([type(field) == ForeignKey for field in value._meta.get_fields()]):
                model_import_map["models"].append(value.__name__)

                continue

            model_import_map["models_with_foreign_keys"].append({
                "name": value.__name__,
                "related_models": list(set([field.related_model.__name__ for field in value._meta.get_fields() if type(field) == ForeignKey]))
            })

    for model_info in model_import_map["models_with_foreign_keys"]:
        import_order_indices = [model_import_map["models"].index(i) for i in model_info["related_models"] if i in model_import_map["models"]]

        if not import_order_indices:
            model_import_map["models"].append(model_info["name"])
        else:
            last_index_of_related_model = max(import_order_indices)
            model_import_map["models"].insert(last_index_of_related_model + 1, model_info["name"])
    
    return model_import_map["models"]


def save_records_from_sheet(reader, model):
    model_fields = [i for i in model._meta.fields if i.name != "id"]
    model_field_names = [i.name for i in model_fields]

    for row in reader:
        if any([field_value in model_field_names for field_value in row]):
            print(f"Skipping header row for {model.__name__}: {row}")

            continue

        model_record = {}

        for index in range(len(row)):
            field = model_fields[index]
            field_value = row[index]
            field_type = field.get_internal_type()

            if field_type == "ForeignKey":
                if field_value:
                    try:
                        model_record[field.name] = field.related_model.objects.get(name=field_value)
                    except Exception as e:
                        raise Exception(str(e))
                else:
                    model_record[field.name] = None
            else:
                # convert csv fields to required django model data type
                if field_type == "BooleanField":
                    if str(field_value).lower() in RESPONSES_POSITIVE:
                        field_value = True
                    elif str(field_value).lower() in RESPONSES_NEGATIVE:
                        field_value = False
                    else:
                        field_value = None
                elif field_type == "PositiveSmallIntegerField":
                    if field_value:
                        field_value = int(field_value) if str(field_value).isnumeric() else None
                    else:
                        field_value = None
                elif not field_value:
                    field_value = None

                model_record[field.name] = field_value

        model(**model_record).save()


def import_data_from_csv(model_name):
    data_import_path = f"{settings.BASE_DIR}/data/csvs/{model_name.lower()}_input.csv"
    data_import_path_alt = f"{settings.BASE_DIR}/data/csvs/{model_name.lower()}_input - Sheet1.csv"

    try:
        with open(data_import_path, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",", quotechar="|")

            save_records_from_sheet(reader=reader, model=getattr(models, model_name))
    except FileNotFoundError:
        try:
            with open(data_import_path_alt, newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter=",", quotechar="|")

                save_records_from_sheet(reader=reader, model=getattr(models, model_name))
        except FileNotFoundError:
            error_message = f"""Skipping data import for model "{model_name}"; could not find file at path "{data_import_path}"."""

            raise FileNotFoundError(error_message)
    except Exception as e:
        error_message = f"An unknown error occurred: {str(e)}"

        raise Exception(error_message)


def main():
    models_to_import = get_models_to_import()

    for model_name in models_to_import:
        try:
            import_data_from_csv(model_name=model_name)
        except FileNotFoundError as fnfe:
            print(str(fnfe))
            
            continue
        except Exception as e:
            print(str(e))

            raise e

main()