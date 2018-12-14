from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=200, default='default')
    cal = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    sfat = models.FloatField(default=0)
    tfat = models.FloatField(default=0)
    chol = models.FloatField(default=0)
    salt = models.FloatField(default=0)
    carb = models.FloatField(default=0)
    fbr = models.FloatField(default=0)
    sgr = models.FloatField(default=0)
    pro = models.FloatField(default=0)
    category = models.CharField(max_length=200, default='default')
