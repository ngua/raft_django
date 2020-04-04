from django.contrib.admin import AdminSite
from django.shortcuts import render
from .models import Room


class ChatAdminSite(AdminSite):
    def chat_view(self, request):
        rooms = Room.objects.all()
        context = {'rooms': rooms}
        return render(
            request,
            'admin/chat.html',
            context=context
        )

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        urls += [
            path('live-chat/', self.admin_view(self.chat_view))
        ]
        return urls


admin_site = ChatAdminSite()
