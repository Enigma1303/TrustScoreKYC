from django.db import models
from django.conf import settings

class KYCApplication(models.Model):
    """
    Represents a KYC application submitted by a user

    """
    class Status(models.TextChoices):
        SUBMITTED = 'SUBMITTED', 'Submitted'
        IN_REVIEW = 'IN_REVIEW', 'In Review'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    class RiskLevel(models.TextChoices):
        LOW = 'LOW', 'Low Risk'
        MEDIUM = 'MEDIUM', 'Medium Risk'
        HIGH = 'HIGH', 'High Risk'  


    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='kyc_application')
    current_status= models.CharField(max_length=20,choices=Status.choices,default=Status.SUBMITTED)
    trust_score=models.IntegerField(default=0)
    risk_level=models.CharField(max_length=20,choices=RiskLevel.choices,default=RiskLevel.HIGH)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"KYC-{self.id} | {self.user.email} | {self.current_status}"

