from django.urls import path
from . import views
from .views import add_property
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', views.realtor_register, name='realtor_create'),
    path('add/',views.add_property, name='add_property'),
    path('realtor_login/',views.realtor_login, name='realtor_login'),
    path('realtor_dashboard', views.realtor_dashboard, name='realtor_dashboard'),
    path('approve_enquiry/<int:enquiry_id>/', views.approve_enquiry,name='approve_enquiry'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)