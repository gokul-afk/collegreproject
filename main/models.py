from asyncio.windows_events import NULL
from django.db import models
import datetime
from django.contrib.auth.models import User
from distutils.command.upload import upload
from mptt.models import MPTTModel, TreeForeignKey


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_gender = models.CharField(max_length=150)
    user_mobile= models.CharField(max_length=255)
    address1 = models.TextField()
    address2 = models.TextField()
    address3 = models.TextField()

    def __str__(self):
        return self.user.username



class Category6(MPTTModel):
    name = models.CharField(max_length=50)
    dispname = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, default=1)
    
    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

class Products6(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category6, on_delete=models.CASCADE, default=NULL)
    description = models.CharField(
        max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/',default='0000000',)
    image1 = models.ImageField(upload_to='uploads/products/',default='0000000')
    def __str__(self):
        return self.name

class multimage(models.Model):
    product = models.ForeignKey(Products6,on_delete=models.CASCADE,null=True)
    multimage = models.ImageField(upload_to="multi/image",null=True,blank=True)
    





class Order(models.Model):
    product = models.ForeignKey(Products6,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(UserProfile,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.price,self.status

class Cart(models.Model):
    product = models.ForeignKey(Products6,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(UserProfile,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    def __str__(self):
        return self.price

class Wish(models.Model):
    product = models.ForeignKey(Products6, on_delete=models.CASCADE)
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    

