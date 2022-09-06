from django.shortcuts import render
from rest_framework import generics, permissions
from . import serializers
from .models import Category
# Create your views here.

class CategoryListView(generics.ListAPIView):
    queryset=Category.objects.all()
    permission_classes=(permissions.AllowAny,)
    serializer_class=serializers.CategorySerializer
