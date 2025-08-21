from django.contrib import admin
from .models import Listing
from .models import Enquiry


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published',
                    'price', 'list_date', 'realtor')
    list_display_links = ('id', 'title')
    list_filter = ('realtor',)
    list_editable = ('is_published',)
    search_fields = ('title', 'description', 'city',
                     'state', 'zipcode', 'address', 'price')
    list_per_page = 25


admin.site.register(Listing, ListingAdmin)

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('listing', 'customer', 'realtor', 'contact_date')
    list_filter = ('contact_date',)
    search_fields = ('listing__title', 'customer__username', 'realtor__name')

admin.site.register(Enquiry, EnquiryAdmin)
