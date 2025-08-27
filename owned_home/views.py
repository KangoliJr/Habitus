from django.shortcuts import render, redirect, get_object_or_404
from .models import OwnedHouse, HousePurchase
from django.contrib.auth.decorators import login_required
from .forms import OwnedHouseForm, HousePurchaseForm
# Create your views here.
#  T-views
def owned_house_list(request):
    houses = OwnedHouse.objects.filter(is_available=True)
    return render(request, 'owned_home/owned_house_list.html', {'houses': houses})

def owned_house_detail(request):
    house = get_object_or_404(OwnedHouse)
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