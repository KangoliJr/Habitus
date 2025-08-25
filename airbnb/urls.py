from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
app_name = 'airbnb'

router = DefaultRouter()
router.register(r'houses', views.AirbnbHouseViewSet, basename='airbnb-houses')
app_name = 'airbnb'
urlpatterns = [
    path('houses/', views.airbnb_house_list_page, name='airbnb_house_list_page'),
    path('houses/add/', views.add_airbnb_house, name='add_airbnb_house'),
    # crud
    path('houses/<int:pk>/edit/', views.edit_airbnb_house, name='edit_airbnb_house'),
    path('houses/<int:pk>/delete/', views.delete_airbnb_house, name='delete_airbnb_house'),
    # url router
    path('api/', include(router.urls)),
]
