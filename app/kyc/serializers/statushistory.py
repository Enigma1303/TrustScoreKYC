from rest_framework import serializers
from kyc.models import StatusHistory

class StatusHistorySerializer(serializers.ModelSerializer):
      
      class Meta:
            model=StatusHistory

            fields=["id","old_status","new_status","changed_by","created_at"]

            read_only_fields=["id","old_status","new_status","changed_by","created_at"]
