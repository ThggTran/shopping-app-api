from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile, Address, UserActivityLog, UserRole
from rest_framework import serializers

from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'date_joined', 'is_staff', 'is_active', 'is_superuser','last_login']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5},
                        'date_joined': {'read_only': True},
                        'is_staff': {'read_only': True},
                        'is_active': {'read_only': True},
                        'is_superuser': {'read_only': True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'full_name', 'phone', 'address_line', 'city', 'province', 'postal_code', 'is_default']
        extra_kwargs = {'id': {'read_only': True},
                        'is_default': {'read_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id','avatar','gender','date_of_birth','loyalty_point']
        extra_kwargs = {'id': {'read_only': True}}

  

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        token['is_staff'] = user.is_staff
        return token