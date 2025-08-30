from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views
app_name = 'airbnb'

router = DefaultRouter()
router.register(r'houses', views.AirbnbHouseViewSet, basename='airbnb-houses')
router.register(r'bookings', views.BookingViewSet, basename='bookings')


houses_router = routers.NestedDefaultRouter(router, r'houses', lookup='house')
houses_router.register(r'images', views.ImagesViewSet, basename='house-images')
houses_router.register(r'bookings', views.BookingViewSet, basename='house-bookings')

urlpatterns = [
    path('', views.airbnb_house_list, name='airbnb_house_list'),
    path('<int:house_id>/', views.airbnb_house_detail, name='airbnb_house_detail'),
    path('houses/add/', views.add_airbnb_house, name='add_airbnb_house'),
    # crud
    path('houses/<int:pk>/edit/', views.edit_airbnb_house, name='edit_airbnb_house'),
    path('houses/<int:pk>/delete/', views.delete_airbnb_house, name='delete_airbnb_house'),
    # url router
    path('api/', include(router.urls)),
    path('api/', include(houses_router.urls)),
]
