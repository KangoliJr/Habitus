from django.contrib import admin
from .models import RentalHouse, RentalApplication, LeaseAgreement, Images

# Register your models here.
class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1

@admin.register(RentalHouse)
class RentalHouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'landlord', 'location', 'monthly_rent', 'security_deposit')
    list_filter = ('location', 'monthly_rent')
    search_fields = ('location', 'description')
    inlines = [ImagesInline,]
    

@admin.register(RentalApplication)
class RentalApplicationAdmin(admin.ModelAdmin):
    list_display = ('house', 'tenant', 'status')
    list_filter = ('status',)
    search_fields = ('location', 'move_in_date')

@admin.register(LeaseAgreement)
class LeaseAgreementAdmin(admin.ModelAdmin):
    list_display = ('application', 'tenant_user', 'landlord_user', 'is_signed_by_tenant')
    list_filter = ('is_signed_by_tenant',)