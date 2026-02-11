from django.db import models 
from .application import KYCApplication
from django.conf import settings

class ReviewerComment(models.Model):

    application=models.ForeignKey(KYCApplication,on_delete=models.CASCADE,related_name='comments')
    reviewer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name="reviewer")
    comment_text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.reviewer} on Application {self.application.id}"
    
    
    
    
