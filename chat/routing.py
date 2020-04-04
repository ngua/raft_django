from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/chat/<str:uid>/', consumers.CustomerChatConsumer),
    path('ws/chat/admin/<str:uid>/', consumers.AdminChatConsumer),
]
