from django.shortcuts import render
from .serializers import AirbnbHouseSerializer
from .models import AirbnbHouse
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, permissions
# Create your views here.
class AirbnbHouseListView(generics.ListAPIView):
    queryset = AirbnbHouse.objects.all()
    serializer_class = AirbnbHouseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]