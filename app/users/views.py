from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .serializers import SignupSerializer
from rest_framework import generics,permissions


class SignupView(generics.CreateAPIView):
    """Signup view with overiding permission classes"""

    serializer_class=SignupSerializer
    permission_classes=[permissions.AllowAny]


    def perform_create(self, serializer):
        user = serializer.save()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


