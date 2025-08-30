from rest_framework import serializers
from .models import RentalHouse, RentalApplication, LeaseAgreement, Images
from django.contrib.auth import get_user_model
from datetime import timedelta
landlord_name = serializers.CharField(source='landlord.username', read_only=True)
User = get_user_model()
class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'image',]
        read_only_fields = ['house']
        

class RentalHouseSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    landlord_name = serializers.CharField(source='landlord.username', read_only=True)
    class Meta:
        model = RentalHouse
        fields = [
            'id', 'landlord_name', 'name', 'description', 'monthly_rent', 
            'security_deposit', 'furnishing_style', 'bedroom', 
            'bathroom', 'location', 'rules', 'amenities','images', 'is_available'
        ]
class RentalApplicationSerializer(serializers.ModelSerializer):      
    house_id = serializers.PrimaryKeyRelatedField(
        queryset=RentalHouse.objects.all(),
        source='house', write_only=True
    )
    house_name = serializers.CharField(source='house.name', read_only=True)
    tenant_name = serializers.CharField(source='tenant.username', read_only=True)
    check_out_date = serializers.SerializerMethodField()
    class Meta:
        model = RentalApplication
        fields = ['id', 'house_id', 'house_name', 'tenant_name','move_in_date', 'lease_duration_months','check_out_date', 'status']
        read_only_fields = ['status']
        
    def get_check_out_date(self, obj):
        return obj.check_out_date
 
class LeaseAgreementSerializer(serializers.ModelSerializer):
    queryset=RentalApplication.objects.all(),
    tenant_name = serializers.CharField(source='tenant.username', read_only=True)
    landlord_name = serializers.CharField(source='house.landlord.username', read_only=True)

    class Meta:
        model = LeaseAgreement
        fields = [
             'id', 'tenant_name', 'landlord_name',
            'start_date', 'end_date', 'is_signed_by_tenant', 'is_signed_by_landlord'
        ]
        
