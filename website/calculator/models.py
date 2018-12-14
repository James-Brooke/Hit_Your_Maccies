from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=200)
    cal = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    sfat = models.IntegerField(default=0)
    tfat = models.IntegerField(default=0)
    chol = models.IntegerField(default=0)
    salt = models.IntegerField(default=0)
    carb = models.IntegerField(default=0)
    fbr = models.IntegerField(default=0)
    sgr = models.IntegerField(default=0)
    pro = models.IntegerField(default=0)
    category = models.CharField(max_length=200)
