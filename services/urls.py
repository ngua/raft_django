from django.urls import path
from . import views


urlpatterns = [
    path('all/', views.services, name='services'),
    path('estimate/', views.EstimateView.as_view(), name='estimate'),
]
