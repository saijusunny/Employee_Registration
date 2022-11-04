from django.db import models
from ntpath import join
from django.contrib.auth.models import User


# Create your models here.
class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    pic = models.ImageField(upload_to="uploads", default='e.png')
    mobile = models.CharField(unique=True, max_length=10)
    email = models.EmailField()
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    datetime = models.DateTimeField(auto_now=True)

