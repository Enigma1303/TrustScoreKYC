from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema

from kyc.models import KYCApplication
from kyc.models import StatusHistory
from kyc.models import ReviewerComment
from kyc.serializers import (
    KYCApplicationSerializer,
    KYCApplicationListSerializer,
    DocumentUploadSerializer,
    StatusHistorySerializer,
    ReviewerCommentSerializer
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
        if self.action == 'list':
            return KYCApplicationListSerializer
        return KYCApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "document_type": {
                        "type": "string"
                    },
                    "file": {
                        "type": "string",
                        "format": "binary"
                    }
                },
                "required": ["document_type", "file"]
            }
        },
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
    


    @action(detail=True, methods=['get'],url_path='current-status')
    def status(self,request,pk=None):
        application=self.get_object()
        return Response({application.current_status})
    
    @action(detail=True, methods=['get'], url_path='history')
    def history(self,request,pk=None):
        application=self.get_object()
        history_records=application.statushistory.all()
        serializer=StatusHistorySerializer(history_records,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    ALLOWED_TRANSITIONS = {
    "SUBMITTED": ["IN_REVIEW"],
    "IN_REVIEW": ["APPROVED", "REJECTED"],
    "APPROVED": [],
    "REJECTED": [],
}

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
       application = self.get_object()

       if not hasattr(request.user, "role") or request.user.role != "ADMIN":
          return Response(
            {"error": "Only admins can change status."},
            status=status.HTTP_403_FORBIDDEN
        )

       new_status = request.data.get("new_status")

       if not new_status:
        return Response( {"error": "new_status is required."},status=status.HTTP_400_BAD_REQUEST )

       old_status = application.current_status
       if new_status == old_status:
           return Response({"error": "Application already in this status."},status=status.HTTP_400_BAD_REQUEST)

       allowed_next_status = self.ALLOWED_TRANSITIONS.get(old_status, [])
       if new_status not in allowed_next_status:
        return Response(
            {
                "error": f"Cannot change status from {old_status} to {new_status}."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

       StatusHistory.objects.create(
                application=application,
                old_status=old_status,
                new_status=new_status,
                 changed_by=request.user
    )

       application.current_status = new_status
       application.save()

       return Response(
        {
            "message": "Status updated successfully.",
            "old_status": old_status,
            "current_status": application.current_status
        },
        status=status.HTTP_200_OK
    )


    @action(detail=True,methods=["get"],url_path="reviewcomments")
    def list_comments(self,request,pk=None):
        application=self.get_object()
        comments=application.comments.all()
        serializer=ReviewerCommentSerializer(comments,many=True)

        return Response(serializer.data)

    @action(detail=True,methods=["post"],url_path="add-reviewcomment")
    def add_comment(self,request,pk=None):
        application=self.get_object()
        #verify he is admin 
        if not hasattr(request.user,"role") or request.user.role !="ADMIN":
            return Response("Only Admins are authorized to add comment",status=status.HTTP_403_FORBIDDEN)
        comment=request.data.get("comment_text")
        
        #check comment is not empty
        if not comment:
           return Response({"error": "comment_text is required."},status=status.HTTP_400_BAD_REQUEST)
        
        comment_obj= ReviewerComment.objects.create(
            application=application,
            reviewer=request.user, 
            comment_text=comment,
        )
        serializer=ReviewerCommentSerializer(comment_obj)
        return Response(serializer.data,status=status.HTTP_201_CREATED)










    

    
    

