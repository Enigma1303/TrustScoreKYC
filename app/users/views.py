import logging
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    CustomTokenObtainPairSerializer,
    SignupSerializer
)

logger = logging.getLogger(__name__)


class SignupView(generics.CreateAPIView):
    """Signup view"""

    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        try:
            user = serializer.save()
            logger.info(
                f"New user registered with id={user.id} email={user.email}"
            )
        except Exception:
            logger.exception("User registration failed")
            raise


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)

            # Only log successful login
            if response.status_code == status.HTTP_200_OK:
                email = request.data.get("email")
                logger.info(f"Successful login for email={email}")

            return response

        except Exception:
            logger.exception("Authentication failed unexpectedly")
            raise
