from django.db import models
from datetime import datetime
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class Realtor(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    description = models.TextField(blank=True)
    phone = models.IntegerField() 
    email = models.CharField(max_length=50)
    # group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
    hire_date = models.DateTimeField(default=datetime.now, blank=True,null=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='realtors_realtor',null=True)
    is_mvp = models.BooleanField(default=False) 

    def __str__(self):
        return self.name

class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='properties/')  # Add the image field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title