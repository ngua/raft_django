from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('convert/', views.convert_currency, name='convert')
]
