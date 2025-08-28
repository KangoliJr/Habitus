from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'profiles', views.ProfileViewSet, basename='profile')
app_name = 'accounts'

"""
Normal django urls
DRF enpoints for the router
authentication views for the login and logging out
DRf api urls
"""


traditional_urlpatterns = [
    # traditional
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html', success_url=reverse_lazy('homepage')), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.user_profile_view, name='user_profile_dashboard'),
    path('profile/', views.user_profile_view, name='user_profile_view'), 
    path('profile/edit/', views.user_profile_edit, name='user_profile_edit'),
    path('profile/upgrade-role/', views.upgrade_role, name='upgrade_role'),
]
api_urlpatterns = [
    # api
    path('register/', views.RegistrationAPIView.as_view(), name='api_register'),
    path('upgrade-role/', views.RoleUpgradeAPIView.as_view(), name='api_upgrade_role'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),
    path('', include(router.urls)), 
]

urlpatterns = [
    path('', include(traditional_urlpatterns)),
    path('api/', include(api_urlpatterns)),
]
