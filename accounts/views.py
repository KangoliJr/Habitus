from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework import  generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

# Create your views here.
class UserView(generics.CreateAPIView):
    queryset = UserSerializer.objects.all()