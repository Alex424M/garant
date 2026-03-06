from django.contrib import admin
from .models import Property, Image, Application


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'deal_type', 'property_type')
    inlines = [ImageInline]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'property', 'created_at')
