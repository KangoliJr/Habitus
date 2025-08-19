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
    fields = ('customer', 'house', 'check_in_date', 'check_out_date','is_confirmed')
    
@admin.register(AirbnbHouse)
class AirbnbHouseAdmin(admin.ModelAdmin):
    list_display = ('host','description', 'price', 'bedroom', 'bathroom', 'location', 'furnishing_style','amenities','rules')
    search_fields = ('price', 'bedrooms', 'bathroom', 'location', 'is_available')
    inlines = [ImageInline, CheckdatesInline, BookingInLine]