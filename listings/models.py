from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from realtors.models import Realtor



class Listing(models.Model):
    """Model definition for listing."""
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    garage = models.IntegerField(default=0)
    sqft = models.IntegerField()
    buildup_area = models.DecimalField(max_digits=5, decimal_places=1)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        """Meta definition for listing."""

        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'

    def __str__(self):
        """Unicode representation of listing."""
        return self.title


class Enquiry(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_enquiries', null=True)
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE, related_name='realtor_enquiries', null=True)
    message = models.TextField(null=True)
    contact_date = models.DateTimeField(default=datetime.now, blank=True,null=True)

    def __str__(self):
        return f"Enquiry by {self.customer.username} on {self.listing.title}"
    
    is_approved = models.BooleanField(default=False)  # Admin/Realtor can approve