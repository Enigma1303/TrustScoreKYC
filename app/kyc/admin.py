from django.contrib import admin
from .models import (
    KYCApplication,
    DocumentUpload,
    StatusHistory,
    ReviewerComment
)

@admin.register(KYCApplication)
class KYCApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "current_status", "trust_score", "risk_level", "created_at")
    list_filter = ("current_status", "risk_level")
    search_fields = ("user__email",)
    ordering = ("-created_at",)

@admin.register(StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("application", "old_status", "new_status", "changed_by", "changed_at")
    list_filter = ("new_status",)

@admin.register(ReviewerComment)
class ReviewerCommentAdmin(admin.ModelAdmin):
    list_display = ("application", "reviewer", "created_at")
    search_fields = ("reviewer__email",)


