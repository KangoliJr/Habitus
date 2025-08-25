import django_filters
from .models import AirbnbHouse

class AirbnbHouseFilter(django_filters.FilterSet):
    location = django_filters.CharFilter(lookup_expr='icontains')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    
    class Meta:
        model = AirbnbHouse
        fields = [
            'location', 
            'bedroom', 
            'bathroom', 
            'furnishing_style',
            'price',
        ]