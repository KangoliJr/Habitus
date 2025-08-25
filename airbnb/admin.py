from django.contrib import admin
from .models import AirbnbHouse, Booking, Images
# Register your models here.
class ImageInline(admin.TabularInline):
    model = Images
    extra = 1 
    
    
class BookingInLine(admin.TabularInline):
    model = Booking
    extra = 1
    fields = ('customer', 'house', 'is_confirmed' )
    
@admin.register(AirbnbHouse)
class AirbnbHouseAdmin(admin.ModelAdmin):
    list_display = ('host', 'name', 'location', 'price', 'bedroom', 'bathroom')
    search_fields = ('price', 'bedroom', 'bathroom', 'location', 'is_available')
    inlines = [ImageInline, BookingInLine]