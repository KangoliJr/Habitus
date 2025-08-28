from django.shortcuts import render, redirect, get_object_or_404
from .models import OwnedHouse, HousePurchase
from django.contrib.auth.decorators import login_required
from .forms import OwnedHouseForm, HousePurchaseForm
from rest_framework import viewsets
from .serializers import OwnedHouseSerializer, HousePurchaseSerializier
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
# Create your views here.
#  T-views
def owned_house_list(request):
    houses = OwnedHouse.objects.filter(is_for_sale=True)
    return render(request, 'owned_home/owned_house_list.html', {'houses': houses})

def owned_house_detail(request, house_id):
    house = get_object_or_404(OwnedHouse,  id=house_id)
    return render(request, 'owned_home/owned_house_detail.html', {'house': house})

@login_required
def add_owned_house(request):
    if request.method == 'POST':
        form = OwnedHouseForm(request.POST)
        if form.is_valid():
            owned_house = form.save(commit=False)
            owned_house.owner = request.user
            owned_house.save()
            return redirect('owned_home:owned_house_list')
        else:
            form = OwnedHouseForm()
        return render(request,'owned_home/add_owned_house.html', {'form': form})
    
@login_required
def edit_owned_house(request, house_id):
    owned_house = get_object_or_404(OwnedHouse, id=house_id, owner=request.user)
    if request.method =='POST':
        form = OwnedHouseForm(request.POST, instance=owned_house)
        if form.is_valid():
            form.save()
            return redirect('owned_home:owned_house_detail', house_id=house_id)
    else:
        form = OwnedHouseForm(instance=owned_house)
    return render(request, 'owned_home/edit_owned_house.html', {'form': form, 'owned_house': owned_house})
    
@login_required
def delete_owned_house(request, house_id):
    owned_house = get_object_or_404(OwnedHouse, id=house_id, owner=request.user)
    if request.method == 'POST':
        owned_house.delete()
        return redirect('owned_home:owned_house_list')
    return render(request, 'owned_home/delete_confirm.html', {'owned_house': owned_house})

@login_required
def submit_purchase(request, house_id):
    house = get_object_or_404(OwnedHouse, id=house_id)
    if request.method == 'POST':
        form = HousePurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.house = house
            purchase.buyer = request.user
            purchase.purchase_price = house.price
            purchase.save()
            return redirect('owned_home:owned_house_list')
        else:
           form = HousePurchaseForm()
        return render(request, 'owned_home/submit_purchase.html', {'form': form, 'house': house})
            
# API Views
class OwnedHouseViewSet(viewsets.ModelViewSet):
    queryset = OwnedHouse.objects.all()
    serializer_class = OwnedHouseSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class HousePurchaseViewSet(viewsets.ModelViewSet):
    queryset = HousePurchase.objects.all()
    serializer_class = HousePurchaseSerializier
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return HousePurchase.objects.filter(buyer=self.request.user)
        return HousePurchase.objects.name()
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)