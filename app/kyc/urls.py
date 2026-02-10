from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kyc.views import KYCApplicationViewSet

router = DefaultRouter()
router.register(r'applications', KYCApplicationViewSet, basename='kyc-application')

urlpatterns = [
    path('', include(router.urls)),
]
