from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
app_name = 'airbnb'

router = DefaultRouter()
router.register(r'houses', views.AirbnbHouseViewSet, basename='airbnb-houses')
router.register(r'images', views.ImagesViewSet, basename='images')
router.register(r'bookings', views.BookingViewSet, basename='bookings')
app_name = 'airbnb'
urlpatterns = [
    path('', views.airbnb_house_list, name='airbnb_house_list'),
    path('<int:house_id>/', views.airbnb_house_detail, name='airbnb_house_detail'),
    path('houses/add/', views.add_airbnb_house, name='add_airbnb_house'),
    # crud
    path('houses/<int:pk>/edit/', views.edit_airbnb_house, name='edit_airbnb_house'),
    path('houses/<int:pk>/delete/', views.delete_airbnb_house, name='delete_airbnb_house'),
    # url router
    path('api/', include(router.urls)),
]
