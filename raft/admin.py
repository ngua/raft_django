from django.contrib import admin
from .models import Category, Service, Contact


admin.site.register(Category)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    exclude = ('contacts',)

    class Meta:
        ordering = ('-category',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
