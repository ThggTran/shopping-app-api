from rest_framework import generics, permissions
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers import (UserSerializer, CustomTokenObtainPairSerializer, 
                                UserProfileSerializer, AddressSerializer)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserProfileView(generics.CreateAPIView,
                      generics.RetrieveUpdateAPIView):
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class AddressView(generics.CreateAPIView,
                      generics.RetrieveUpdateAPIView):
    
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.addresses.all()
    
    def get(self, request, *args, **kwargs):
        addresses = self.get_object()
        serializer = self.get_serializer(addresses, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=201)



    
