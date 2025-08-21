from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Realtor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    photo = models.ImageField(upload_to='realtors/%Y/%m/%d/', blank=True)
    description = models.TextField(blank=True)
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    
    hire_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name