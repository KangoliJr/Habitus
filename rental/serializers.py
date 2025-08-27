from rest_framework import serializers
from .models import RentalHouse, RentalApplication, LeaseAgreement, Images

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['images',]
        

class RentalHouseSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    class Meta:
        model = RentalHouse
        fields = [
            'id', 'landlord', 'description', 'monthly_rent', 
            'security_deposit', 'furnishing_style', 'bedroom', 
            'bathroom', 'location', 'rules', 'amenities','images'
        ]
class RentalApplicationSerializer(serializers.ModelSerializer):      
    house_id = serializers.IntegerField(source='house.id')
    tenant_name = serializers.CharField(source='tenant.username', read_only=True)
    class Meta:
        model = RentalApplication
        fields = ['id', 'landlord', 'description', 'monthly_rent', 
            'security_deposit', 'furnishing_style', 'bedroom', 
            'bathroom', 'location', 'rules', 'amenities','images',
        ]

class LeaseAgreementSerializer(serializers.ModelSerializer):
    application_id = serializers.CharField(source='application.id')
    tenant_name = serializers.CharField(source='tenant_user.username', read_only=True)
    landlord_name = serializers.CharField(source='landlord_user.username', read_only=True)

    class Meta:
        model = LeaseAgreement
        fields = ['__all__']