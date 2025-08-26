from django.shortcuts import render, get_object_or_404
from . models import RentalHouse, RentalApplication, LeaseAgreement
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import RentalHouseSerializer, RentalApplicationSerializer, LeaseAgreementSerializer
from .permissions import IsLandlordOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


# Create your views here.

# T-views
def rental_property_list(request):
    houses  = RentalHouse.objects.filter(is_available=True)
    return render(request, 'rental/rental_properties_list.html', {'houses': houses})

def rental_property_detail(request):
    house = get_object_or_404(RentalHouse)
    return render(request, 'rental/rental_property_detail.html', {'house': house})

@login_required
def my_applications(request):
    applications = RentalApplication.objects.filter(tenant=request.user)
    return render(request, 'rental/my_applications.html', {'applications': applications})

# API Views
class RentalHouseViewSet(viewsets.ModelViewSet):
    queryset = RentalHouse.objects.all()
    serializer_class = RentalHouseSerializer
    permission_classes = [IsLandlordOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)
        
class RentalApplicationViewSet(viewsets.ModelViewSet):
    queryset = RentalApplication.objects.all()
    serializer_class = RentalApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)
        
    def get_queryset(self):
        return RentalApplication.objects.filter(tenant=self.request.user)
    
class LeaseAgreementViewSet(viewsets.ModelViewSet):
    queryset = LeaseAgreement.objects.all()
    serializer_class = LeaseAgreementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LeaseAgreement.objects.filter(tenant=self.request.user)