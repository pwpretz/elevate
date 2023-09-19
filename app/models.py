from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.
class Code(models.Model):
    code = models.TextField()
    cnic = models.IntegerField()
    password = models.CharField(max_length=10000)

class change(models.Model):
    code = models.TextField()
    new = models.TextField()

class User(AbstractUser):
    cnic = models.IntegerField()
    manage = models.TextField()

class Property(models.Model):
    ownerCnic = models.IntegerField()
    owner = models.TextField()
    reg = models.CharField(max_length=100000)
    app = models.CharField(max_length=100000)
    name = models.CharField(max_length=100000)
    floor = models.CharField(max_length=100000)
    type = models.CharField(max_length=100000)
    size = models.CharField(max_length=100000)
    price = models.IntegerField()
    discount = models.IntegerField()
    fprice = models.IntegerField()
    location = models.CharField(max_length=10000)
    unit = models.CharField(max_length=10000)

class Inv(models.Model):
    name = models.CharField(max_length=100000)
    floor = models.CharField(max_length=100000)
    type = models.CharField(max_length=100000)
    size = models.CharField(max_length=100000)
    price = models.IntegerField()
    location = models.CharField(max_length=10000)
    unit = models.CharField(max_length=10000)
    
class PaymentPlan(models.Model):
    property = models.IntegerField()
    type = models.CharField(max_length=10000)
    date = models.CharField(max_length=10000)
    amount = models.TextField()
    is_paid = models.CharField(max_length=1000)

class UserDetails(models.Model):
    cnic = models.IntegerField()
    fullName = models.TextField()
    name = models.TextField()
    email = models.TextField()
    address = models.CharField(max_length=10000)
    phone = models.IntegerField()
    occ = models.TextField()
    nat = models.TextField()
    nominee = models.ForeignKey('Nominee', on_delete=models.CASCADE)

class Nominee(models.Model):
    name = models.TextField()
    address = models.CharField(max_length=10000)
    cnic = models.IntegerField()
    relation = models.TextField()

class Projects(models.Model):
    name = models.TextField()
    location = models.TextField()

class Popup(models.Model):
    type = models.TextField()
    url = models.TextField()
    