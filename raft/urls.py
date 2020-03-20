from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('estimate/', views.estimate, name='estimate'),
    path('contact/', views.ContactView.as_view(), name='contact')
]
