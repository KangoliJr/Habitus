from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'api/users', views.UserViewSet)
router.register(r'api/profiles', views.ProfileViewSet)
"""
DRF enpoints for the router
Normal django urls
authentication views for the login and logging out
DRf api urls
"""


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('dashboard/', views.user_profile_view, name='user_profile_dashboard'),
    path('profile/', views.user_profile_view, name='user_profile_view'), 
    path('profile/edit/', views.user_profile_edit, name='user_profile_edit'),
    path('profile/upgrade-role/', views.upgrade_role, name='upgrade_role'),

    path('', include(router.urls)), 
    path('api/upgrade-role/', views.RoleUpgradeAPIView.as_view(), name='api_upgrade_role'),
    path('api/register/', views.RegistrationAPIView.as_view(), name='api_register'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

