from django.urls import path, include
from .import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'houses', views.OwnedHouseViewSet, basename='owned-house'),
router.register(r'purchases', views.HousePurchaseViewSet, basename='house-purchase'),

app_name = 'owned_home'

urlpatterns = [
    path('', views.owned_house_list, name='owned_house_list'),
    path('add/', views.add_owned_house, name='add_owned_house'),
    path('<int:house_id>/', views.owned_house_detail, name='owned_house_detail'),
    path('<int:house_id>/edit/', views.edit_owned_house, name='edit_owned_house'),
    path('<int:house_id>/purchase/', views.submit_purchase, name='submit_purchase'),
    path('<int:house_id>/delete/', views.delete_owned_house, name='delete_owned_house'),
     
    path('api/', include(router.urls)),
]
