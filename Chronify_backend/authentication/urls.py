from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    RegisterView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    SendOTPView,
    VerifyOTPView,
)
from rest_framework_simplejwt.views import TokenRefreshView
app_name = 'auth'
urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]
