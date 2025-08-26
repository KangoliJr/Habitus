from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
router.register(r'houses', views.RentalHouseViewSet, basename='rental_house')
router.register(r'applications', views.RentalApplicationViewSet, basename='rental_application')
router.register(r'agreements', views.LeaseAgreementViewSet, basename='lease_agreement')
app_name = 'rental'

urlpatterns = [
    # T-urls
    path('', views.rental_property_list, name='rental_properties_list'),
    path('house/', views.rental_property_detail, name='rental_property_detail'),
    path('my-applications/', views.my_applications, name='my_applications'),
    
    # API urls
    path('api/', include(router.urls)),
]

