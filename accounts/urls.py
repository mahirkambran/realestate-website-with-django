from django.urls import path

from . import views

urlpatterns = [
    path('customerlogin', views.customerlogin, name='customerlogin'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
  

    path('customer_register', views.customer_register, name='customer_register'),
    # path('realtor_register', views.realtor_register, name='realtor_register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('managelistings',views.managelistings,name='managelistings'),
    path('edit-listing/<int:listing_id>/', views.edit_listing, name='edit_listing'),
    path('delete-listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    path('managecontacts',views.managecontacts,name='managecontacts'),
    path('managerealtors',views.managerealtors,name='managerealtors'),
    path('addnew_realtor',views.addnew_realtor,name='addnew_realtor'),
    path('edit-realtor/<int:id>/', views.edit_realtor, name='edit_realtor'),
    path('delete-realtor/<int:id>/', views.delete_realtor, name='delete_realtor'),
]

