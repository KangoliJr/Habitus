from django.contrib import admin
from .models import AirbnbHouse, Booking, Checkdates, Images
# Register your models here.
class ImageInline(admin.TabularInline):
    model = Images
    extra = 1 
    
class CheckdatesInline(admin.TabularInline):
    model = Checkdates
    extra = 1
    fields = ('checkin', 'checkout', 'booking',)
    
class BookingInLine(admin.TabularInline):
    model = Booking
    extra = 1
    fields = ('customer', 'house', 'is_confirmed' )
    
@admin.register(AirbnbHouse)
class AirbnbHouseAdmin(admin.ModelAdmin):
    list_display = ('host', 'name', 'location', 'price', 'bedroom', 'bathroom')
    search_fields = ('price', 'bedroom', 'bathroom', 'location', 'is_available')
    inlines = [ImageInline, CheckdatesInline, BookingInLine]