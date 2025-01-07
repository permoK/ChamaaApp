# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'mobile_number', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('id', 'first_name','last_name', 'mobile_number', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
