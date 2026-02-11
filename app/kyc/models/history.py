from django.db import models 
from .application import KYCApplication

class StatusHistory(models.Model):
    application=models.ForeignKey(KYCApplication,on_delete=models.CASCADE,related_name='statushistory')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by=models.CharField(max_length=255)
    changed_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Application {self.application.id}: {self.old_status} → {self.new_status}"
