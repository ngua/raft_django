from django.contrib import admin
from .models import Category, Service, Contact


admin.site.register(Category)
admin.site.register(Service)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
