# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'mobile_number', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(
        write_only=True,
        min_length=4,
        max_length=6,
        validators=[
            RegexValidator(regex=r'^\d{4,6}$', message="PIN must be numeric and 4-6 digits long.")
        ]
    )

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'mobile_number', 'email', 'pin')

    def create(self, validated_data):
        pin = validated_data.pop('pin')
        user = User.objects.create(**validated_data)
        user.set_password(pin)  # Store the PIN as the password
        user.save()
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="Mobile Number")
    pin = serializers.CharField(label="PIN", write_only=True, min_length=4, max_length=6)

    def validate(self, attrs):
        username = attrs.get('username')
        pin = attrs.get('pin')

        if username and pin:
            user = authenticate(request=self.context.get('request'), username=username, password=pin)
            if not user:
                raise serializers.ValidationError(
                    {"detail": "Invalid mobile number or PIN."},
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                {"detail": "Both username and PIN are required."},
                code='authorization'
            )

        attrs['user'] = user
        return attrs

