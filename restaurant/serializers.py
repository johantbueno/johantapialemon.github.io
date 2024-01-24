from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Menu, Booking, MenuItem, Category

class menuSerializer(serializers.ModelSerializer):
    class Meta:
        model= Menu
        fields= '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model= Booking
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class MenuItemSerializer(serializers.ModelSerializer):
    # Additional fields for serialization
    image = serializers.ImageField(allow_null=False)
    menu_item_description = serializers.CharField(max_length=1000, default='')

    class Meta:
        model = MenuItem
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = ['slug', 'title']
