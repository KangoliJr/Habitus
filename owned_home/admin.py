from django.contrib import admin
from .models import OwnedHouse, Images, HousePurchase
# Register your models here.

class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1
@admin.register(OwnedHouse)   
class OwnedHouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'price')
    list_filter = ('location', 'furnishing_style', 'bedroom')
    search_fields = ('name', 'location', 'price')
    inlines = [ImagesInline]