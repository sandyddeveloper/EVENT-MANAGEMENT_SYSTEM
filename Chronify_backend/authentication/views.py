from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.core.cache import cache
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer
import random

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'authentication/password_reset_email.html'
    subject_template_name = 'authentication/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')

class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = random.randint(100000, 999999)
        cache.set(email, otp, timeout=300)

        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'no-reply@example.com',
            [email]
        )
        return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        cached_otp = cache.get(email)

        if str(cached_otp) == str(otp):
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
