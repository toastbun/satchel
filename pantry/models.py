from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=512, unique=True, null=False)
    def __str__(self):
        return self.name
