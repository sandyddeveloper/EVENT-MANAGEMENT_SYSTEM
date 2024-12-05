from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_attendee'] = user.is_attendee
        token['is_organizer'] = user.is_organizer
        return token

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'is_attendee', 'is_organizer']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
