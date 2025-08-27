from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.owned_house_list, name='owned_house_list'),
    path('add/', views.add_owned_house, name='add_owned_house'),
    path('<int:house_id>/edit/', views.edit_owned_house, name='edit_owned_house'),
]
