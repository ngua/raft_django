from django.contrib import admin
from .models import Category, Service


admin.site.register(Category)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    exclude = ('contacts',)

    class Meta:
        ordering = ('-category',)
