from django.contrib import admin
from .models import Item, Section


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['item_name', 'price']
    list_display = ['item_name', 'available_quantity', 'price']
    list_filter = ['item_name', 'available_quantity', 'price']


class SectionAdmin(admin.ModelAdmin):
    search_fields = ['section_name']
    list_display = ['section_name']
    list_filter = ['section_name']


admin.site.register(Section),
admin.site.register(Item, ItemAdmin)
