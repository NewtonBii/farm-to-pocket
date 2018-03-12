from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=30, null=True)
    type_of_user = models.CharField(max_length=2, null=True)
    phonenumber = models.CharField(max_length=20, null=True)
    level = models.IntegerField(null=True)
    location = models.CharField(max_length=50)
    nearest_town = models.CharField(max_length=50)

    @classmethod
    def requested_users(cls, user_type):
        '''
        Method that gets list of farmers for buyer and vice versa
        '''
        if user_type == '1':
            requested_type = '2'
        else:
            requested_type = '1'

        found_users = User.objects.filter(type_of_user=requested_type)
        return found_users


class Product(models.Model):
    name = models.CharField(max_length=100)
    type_of_product = models.CharField(max_length=2, null=True)
    quantity = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    user = models.ForeignKey(User, null=True, on_delete = models.CASCADE)

    @classmethod
    def requested_products(cls, product_type):
        '''
        Method that gets list of farmers for buyer and vice versa
        '''
        if product_type == '1':
            requested_type = '2'
        else:
            requested_type = '1'

        found_products = Product.objects.filter(type_of_product=requested_type)
        return found_products


class session_levels(models.Model):
	session_id = models.CharField(max_length=25,primary_key=True)
	phonenumber= models.CharField(max_length=25,null=True)
	level = models.IntegerField(null=True)
