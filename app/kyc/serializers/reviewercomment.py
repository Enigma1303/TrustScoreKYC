from rest_framework import serializers 
from kyc.models.comment import ReviewerComment

class ReviewerCommentSerializer(serializers.ModelSerializer):

    #adding this to print name 
    reviewer=serializers.StringRelatedField(read_only=True)
    class Meta:
        model = ReviewerComment
        fields= ["id","reviewer","comment_text","created_at"]
        read_only_fields=["id","reviewer","created_at"]