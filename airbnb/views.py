from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets,filters
from .models import AirbnbHouse, Booking
from .forms import AirbnbHouseForm
from .serializers import AirbnbHouseSerializer, BookingSerializer
from .permissions import IsHostOrReadOnly
from django.contrib import messages
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AirbnbHouseFilter
from django.http import HttpResponseForbidden
from rest_framework.permissions import IsAuthenticated


# Create your views here.
"""
Here we are going to show the html page for showing the houses
"""
def airbnb_house_list(request):
    houses = AirbnbHouse.objects.all()
    context = {
        'houses': houses,
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'airbnb/airbnb_house_list.html', context)
def airbnb_house_detail(request, house_id):
    house = get_object_or_404(AirbnbHouse, id=house_id)
    return render(request, 'airbnb/airbnb_house_detail.html', {'house': house})

"""
Handles a form for adding a new house. 
if you are a host
 """

@login_required
def add_airbnb_house(request):

    if not request.user.is_host:
        messages.error(request, "Be a host to add a new house unit.")
        return redirect('home')  
    
    if request.method == 'POST':
        form = AirbnbHouseForm(request.POST)
        if form.is_valid():
            house = form.save(commit=False)
            house.host = request.user
            house.save()
            messages.success(request, "house created successfully.")
            return redirect('airbnb_house_list_page')
    else:
        form = AirbnbHouseForm()
    
    return render(request, 'airbnb/add_house.html', {'form': form})
@login_required
def edit_airbnb_house(request, pk):
    house = get_object_or_404(AirbnbHouse, pk=pk)
    if house.host != request.user:
        messages.error(request, "You do not have permission to edit this listing.")
        return redirect('airbnb:airbnb_house_list_page')

    if request.method == 'POST':
        form = AirbnbHouseForm(request.POST, request.FILES, instance=house)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing updated successfully.")
            return redirect('airbnb:airbnb_house_list_page')
    else:
        form = AirbnbHouseForm(instance=house)

    return render(request, 'airbnb/edit_house.html', {'form': form, 'house': house})

@login_required
def delete_airbnb_house(request, pk):
    house = get_object_or_404(AirbnbHouse, pk=pk)
    if house.host != request.user:
        return HttpResponseForbidden("You are not allowed to delete this house unit.")

    if request.method == 'POST':
        house.delete()
        messages.success(request, "house unit deleted successfully.")
        return redirect('airbnb:airbnb_house_list_page')
    
    return render(request, 'airbnb/delete_confirm.html', {'house': house})

"""
    API endpoint for handling all house-related actions.
    - Public can view (list, retrieve).
    - Hosts can create, update, and delete.
    """
class AirbnbHouseViewSet(viewsets.ModelViewSet):
    queryset = AirbnbHouse.objects.all()
    serializer_class = AirbnbHouseSerializer
    permission_classes = [IsHostOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AirbnbHouseFilter
    search_fields = ['name', 'location', 'description']
    ordering_fields = ['price', 'name', 'location']
    def get_queryset(self):
        if self.request.query_params.get('my_listings'):
            return self.queryset.filter(host=self.request.user)
        return self.queryset
    
    def perform_create(self, serializer):
        serializer.save(host=self.request.user)
        
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(customer=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)