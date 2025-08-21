from django.urls import path

from . import views

urlpatterns = [
    path('listings', views.index, name='listings'),
    path('listing/<int:listing_id>/', views.listing, name='listing'),
    path('search', views.search, name='search'),
    path('add/', views.add_property, name='add_property'),
    path('enquiry/<int:listing_id>/', views.enquiry_form, name='enquiry'),
    path('admin/enquiries', views.enquiry_list_view, name='enquiry_list'),
    # path('send-enquiry/', views.send_enquiry, name='send_enquiry'),
]
