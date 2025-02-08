from django.db import models


class Rooms(models.TextChoices):
    KITCHEN = "kitchen"
    BASEMENT = "basement"