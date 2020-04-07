"""raft_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from chat.admin import admin_site


urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('raft.urls')),
    path('services/', include('services.urls')),
    path('chat/', include('chat.urls')),
    path('i18n/', include('django.conf.urls.i18n'))
]


urlpatterns += i18n_patterns(
    path('', include('raft.urls')),
    path('services/', include('services.urls')),
    path('chat/', include('chat.urls')),
)
