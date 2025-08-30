from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .import views

router = DefaultRouter()
router.register(r'houses', views.RentalHouseViewSet, basename='rental_house')
router.register(r'applications', views.RentalApplicationViewSet, basename='rental-applications')
router.register(r'agreements', views.LeaseAgreementViewSet, basename='lease-agreements')

houses_router = routers.NestedDefaultRouter(router, r'houses', lookup='house')
houses_router.register(r'images', views.ImagesViewSet, basename='house-images')
houses_router.register(r'applications', views.RentalApplicationViewSet, basename='house-applications')

applications_router = routers.NestedDefaultRouter(router, r'applications', lookup='application')
applications_router.register(r'agreements', views.LeaseAgreementViewSet, basename='application-agreements')
app_name = 'rental'

urlpatterns = [
    # T-urls
    path('', views.rental_property_list, name='rental_properties_list'),
    path('<int:house_id>/', views.rental_property_detail, name='rental_property_detail'),
    path('apply/<int:house_id>/', views.submit_application, name='submit_application'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('api/applications/', views.RentalApplicationListCreate.as_view(), name='rental-application-list-create'),
    path('api/applications/<int:pk>/', views.RentalApplicationRetrieve.as_view(), name='rental-application-retrieve'),
    path('api/agreements/', views.LeaseAgreementListCreate.as_view(), name='lease-agreement-list-create'),
    path('api/agreements/<int:pk>/', views.LeaseAgreementRetrieve.as_view(), name='lease-agreement-retrieve'),
    
    # API urls
    path('api/', include(router.urls)),
    path('api/', include(houses_router.urls)),
    path('api/', include(applications_router.urls)),
]

