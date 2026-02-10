from rest_framework import serializers
from kyc.models import DocumentUpload
import os


class DocumentUploadSerializer(serializers.ModelSerializer):
    """Serializer for document uploads"""

    file = serializers.FileField()

    class Meta:
        model = DocumentUpload
        fields = ['id', 'document_type', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

    def validate_file(self, value):
        # Max 5MB
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 5MB")

        valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
        ext = os.path.splitext(value.name)[1].lower()

        if ext not in valid_extensions:
            raise serializers.ValidationError(
                f"Only {', '.join(valid_extensions)} files are allowed"
            )

        return value
