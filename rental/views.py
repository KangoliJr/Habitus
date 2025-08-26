from django.shortcuts import render
from . models import RentalHouse

# Create your views here.

# T-views
def rental_property_list(request):
    houses  = RentalHouse.objects.filter(is_available=True)
    return render(request, 'rental/rental_properties_list.html', {'houses': houses})
