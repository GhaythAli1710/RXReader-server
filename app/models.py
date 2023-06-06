from django.db import models


# Create your models here.
class test(models.Model):
    string = models.CharField(max_length=10)
