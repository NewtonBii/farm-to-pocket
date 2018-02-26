from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30, null=True)
    phonenumber = models.CharField(max_length=20, null=True)
    location = models.CharField(max_length=30, null=True)
    level = models.IntegerField(null=True, default=0)

class session_levels(models.Model):
	  session_id = models.CharField(max_length=25,primary_key=True)
	  phonenumber= models.CharField(max_length=25,null=True)
	  level = models.IntegerField(null=True)
