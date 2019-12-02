from django.db import models

class FoodModel(models.Model):
    name  = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    type  = models.CharField(max_length=20)