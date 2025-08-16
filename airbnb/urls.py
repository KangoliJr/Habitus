from django.urls import path, include
from .views import AirbnbHouseListView

urlpatterns = [
    path('airbnbhouses/', AirbnbHouseListView.as_view(), name='airbnb-list'),
]
