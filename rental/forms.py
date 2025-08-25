from django import forms
from .models import RentalHouse, RentalApplication

class RentalHouseForm(forms.ModelForm):
    class Meta:
        model = RentalHouse
        fields = [
           'name','description', 'monthly_rent', 'security_deposit', 
            'furnishing_style', 'bedroom', 'bathroom', 'location', 
            'rules', 'amenities'
        ]
        
class RentalApplicationForm(forms.ModelForm):
    class Meta:
        model = RentalApplication
        fields = ['move_in_date', 'lease_duration_months']