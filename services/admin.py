from django.contrib import admin
from chat.admin import admin_site
from .models import Category, Service


admin_site.register(Category)


@admin.register(Service, site=admin_site)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    exclude = ('contacts',)

    class Meta:
        ordering = ('-category',)
