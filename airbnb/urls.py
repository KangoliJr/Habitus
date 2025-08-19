from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/houses', views.AirbnbHouseViewSet, basename='airbnb-houses')

urlpatterns = [
    path('houses/', views.airbnb_house_list_page, name='airbnb_house_list_page'),
    path('houses/add/', views.add_airbnb_house, name='add_airbnb_house'),
    path('', include(router.urls)),
]
