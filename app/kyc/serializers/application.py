from rest_framework import serializers 
from kyc.models.application import KYCApplication
from .document import DocumentUploadSerializer


class KYCApplicationSerializer(serializers.ModelSerializer):
    """
    Docstring for KYCApplicationSerializer
    """

    documents = DocumentUploadSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model=KYCApplication

        fields=[
            "id","user_email","current_status","trust_score",
            "risk_level","documents","created_at","updated_at"
                ]
        read_only_fields=[
                  "id","current_status","trust_score",
                  "risk_level","created_at","updated_at"      
                ]
        
class KYCApplicationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing applications"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    document_count = serializers.IntegerField(source='documents.count', read_only=True)
    
    class Meta:
        model= KYCApplication
        fields = [
            'id',
            'user_email',
            'current_status',
            'trust_score',
            'risk_level',
            'document_count',
            'created_at'
        ]