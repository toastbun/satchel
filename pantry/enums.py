from django.db import models


class AmountsLeft(models.TextChoices):
    HIGH = "high"
    MED = "medium"
    LOW = "low"


class Rooms(models.TextChoices):
    KITCHEN = "kitchen"
    BASEMENT = "basement"
    OVERFLOW = "overflow"