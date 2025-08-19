from django import forms
from .models import AirbnbHouse

class AirbnbHouseForm(forms.ModelForm):
    class Meta:
        model = AirbnbHouse
        fields = [
            'house_id', 'description', 'price', 'furnishing_style',
            'bedroom', 'bathroom', 'location', 'rules', 'amenities'
        ]