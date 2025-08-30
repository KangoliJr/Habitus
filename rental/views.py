from django.shortcuts import render,redirect, get_object_or_404
from . models import RentalHouse, RentalApplication, LeaseAgreement, Images
from django.contrib.auth.decorators import login_required
from .forms import RentalApplicationForm
from django.contrib import messages
from rest_framework import viewsets, filters
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import RentalHouseSerializer, RentalApplicationSerializer, LeaseAgreementSerializer, ImagesSerializer
from .permissions import IsLandlordOrReadOnly, IsLandlordOrTenant
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.

# T-views
def rental_property_list(request):
    houses  = RentalHouse.objects.filter(is_available=True)
    return render(request, 'rental/rental_properties_list.html', {'houses': houses})

def rental_property_detail(request, house_id):
    house = get_object_or_404(RentalHouse, id=house_id)
    return render(request, 'rental/rental_property_detail.html', {'house': house})

@login_required
def my_applications(request):
    applications = RentalApplication.objects.filter(tenant=request.user)
    return render(request, 'rental/my_applications.html', {'applications': applications})
@login_required
def submit_application(request, house_id):
    house = get_object_or_404(RentalHouse, id=house_id)
    if request.method == 'POST':
        form = RentalApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.tenant = request.user
            application.house = house
            application.save()
            messages.success(request, "Your application has been submitted.")
            return redirect('rental:my_applications')
    else:
        form = RentalApplicationForm()
    
    return render(request, 'rental/submit_application.html', {'form': form, 'house': house})
# API Views
class RentalHouseViewSet(viewsets.ModelViewSet):
    queryset = RentalHouse.objects.all()
    serializer_class = RentalHouseSerializer
    permission_classes = [IsLandlordOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['furnishing_style', 'bedroom', 'bathroom', 'location']
    search_fields = ['name', 'location', ]
    ordering_fields = ['monthly_rent', 'name']
    
    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)
    
class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    permission_classes = [IsLandlordOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_create(self, serializer):
        house_id = self.kwargs['house_pk']
        house = RentalHouse.objects.get(pk=house_id)
        serializer.save(house=house)
        
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.profile.is_landlord:
            return Images.objects.filter(house__landlord=self.request.user)
        return Images.objects.filter(house__is_available=True)
    
class RentalApplicationViewSet(viewsets.ModelViewSet):
    queryset = RentalApplication.objects.all()
    serializer_class = RentalApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        house_id = self.kwargs['house_pk']
        house = RentalHouse.objects.get(pk=house_id)
        serializer.save(tenant=self.request.user, house=house)
        
    def  get_queryset(self):
        user = self.request.user
        if user.profile.is_landlord:
            return RentalApplication.objects.filter(house__landlord=user)
        else:
            return RentalApplication.objects.filter(tenant=user)

class LeaseAgreementViewSet(viewsets.ModelViewSet):
    queryset = LeaseAgreement.objects.all()
    serializer_class = LeaseAgreementSerializer
    permission_classes = [IsLandlordOrTenant]
    
    def perform_create(self, serializer):
        application_id = self.kwargs['application_pk']
        application = RentalApplication.objects.get(pk=application_id)
        serializer.save(application=application)
        
    def get_queryset(self):
        user = self.request.user
        if user.profile.is_landlord:
            return LeaseAgreement.objects.filter(application__house__landlord=user)
        else:
            return LeaseAgreement.objects.filter(application__tenant=user)
