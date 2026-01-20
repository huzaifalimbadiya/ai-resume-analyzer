from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'predicted_role', 'score', 'uploaded_at')
    list_filter = ('predicted_role', 'uploaded_at')
    search_fields = ('predicted_role', 'extracted_skills')
    readonly_fields = ('uploaded_at', 'predicted_role', 'confidence_score', 'score', 'extracted_skills', 'recommended_skills')
