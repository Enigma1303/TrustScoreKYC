from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    SignupView,
    CustomTokenObtainPairView,
)

urlpatterns = [
    # Auth
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
