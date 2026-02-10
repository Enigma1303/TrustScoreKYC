from django.db import models
from .application import KYCApplication

class DocumentUpload(models.Model):
    """
    Docstring for DocumentUpload
    """
    class DocumentType(models.TextChoices):
        ID_PROOF = 'ID_PROOF', 'ID Proof'
        SELFIE = 'SELFIE', 'Selfie with ID'
        ADDRESS_PROOF = 'ADDRESS_PROOF', 'Address Proof'
        PAN_CARD = 'PAN_CARD', 'PAN Card'
        BANK_STATEMENT = 'BANK_STATEMENT', 'Bank Statement'


    application=models.ForeignKey(KYCApplication,on_delete=models.CASCADE, related_name='documents')  
    document_type = models.CharField(max_length=20,choices=DocumentType.choices)
    file=models.FileField(upload_to='luc_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} - Application{self.application.id}"

 

