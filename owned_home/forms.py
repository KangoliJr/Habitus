from django import forms
from .models import OwnedHouse, HousePurchase

class OwnedHouseForm(forms.ModelForm):
    class Meta:
        model = OwnedHouse
        fields = [
            'name', 'description', 'price', 
            'furnishing_style', 'bedroom', 'bathroom', 
            'location', 'rules', 'amenities'
        ]
        
class HousePurchaseForm(forms.ModelForm):
    class Meta:
        model = HousePurchase
        fields = []