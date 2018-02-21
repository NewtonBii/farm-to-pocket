from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30, null=True)
    phonenumber = models.CharField(max_length=20, null=True)
    location = models.CharField(max_length=30, null=True)
    level = models.IntegerField(null=True)
    
