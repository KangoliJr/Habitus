from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from .models import AirbnbHouse
from .forms import AirbnbHouseForm
from .serializers import AirbnbHouseSerializer
from .permissions import IsHostOrReadOnly



# Create your views here.
"""
Here we are going to show the html page for showing the houses
"""
def airbnb_house_list_page(request):
    houses = AirbnbHouse.objects.all()
    context = {
        'houses': houses,
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'airbnb/house_list.html', context)

"""
Handles a form for adding a new house. 
if you are a host
 """

@login_required
def add_airbnb_house(request):

    if not request.user.is_host:
        return redirect('home')  
    
    if request.method == 'POST':
        form = AirbnbHouseForm(request.POST)
        if form.is_valid():
            house = form.save(commit=False)
            house.host = request.user
            house.save()
            return redirect('airbnb_house_list_page')
    else:
        form = AirbnbHouseForm()
    
    return render(request, 'airbnb/add_house.html', {'form': form})

"""
    API endpoint for handling all house-related actions.
    - Public can view (list, retrieve).
    - Hosts can create, update, and delete.
    """
class AirbnbHouseViewSet(viewsets.ModelViewSet):
    queryset = AirbnbHouse.objects.all()
    serializer_class = AirbnbHouseSerializer
    permission_classes = [IsHostOrReadOnly]
    
    def perform_create(self, serializer):
        # Automatically set the host to the authenticated user.
        serializer.save(host=self.request.user)