from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'user'

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='create'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('me/profile/', views.UserProfileView.as_view(), name='profile'),
    path('me/address/', views.AddressView.as_view(), name='address'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
