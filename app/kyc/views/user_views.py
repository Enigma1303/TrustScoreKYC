from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema

from kyc.models import KYCApplication
from kyc.serializers import (
    KYCApplicationSerializer,
    KYCApplicationListSerializer,
    DocumentUploadSerializer
)


class KYCApplicationViewSet(viewsets.ModelViewSet):
    """KYC applications API"""

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'ADMIN':
            return KYCApplication.objects.all()
        return KYCApplication.objects.filter(user=user)

    def get_serializer_class(self):
        return (
            KYCApplicationListSerializer
            if self.action == 'list'
            else KYCApplicationSerializer
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        request=DocumentUploadSerializer,
        responses={201: DocumentUploadSerializer},
    )
    @action(
        detail=True,
        methods=['post'],
        url_path='upload-document',
        parser_classes=[MultiPartParser, FormParser],
    )
    def upload_document(self, request, pk=None):
        application = self.get_object()

        if application.current_status in ['APPROVED', 'REJECTED']:
            return Response(
                {'error': 'Application finalized'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DocumentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(application=application)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='documents')
    def list_documents(self, request, pk=None):
        documents = self.get_object().documents.all()
        serializer = DocumentUploadSerializer(documents, many=True)
        return Response(serializer.data)
