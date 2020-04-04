from django.contrib import admin
from chat.admin import admin_site
from .models import Contact


@admin.register(Contact, site=admin_site)
class ContactAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
