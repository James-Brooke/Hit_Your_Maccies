from django.db import models

class Food(models.Model):
    item = models.CharField(max_length=200),
    cal = models.IntegerField(),
    fat = models.IntegerField(),
    sfat = models.IntegerField(),
    tfat = models.IntegerField(),
    chol = models.IntegerField(),
    salt = models.IntegerField(),
    carb = models.IntegerField(),
    fbr = models.IntegerField(),
    sgr = models.IntegerField(),
    pro = models.IntegerField(),
    category = models.CharField(max_length=200)
