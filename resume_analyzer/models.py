from django.db import models

class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    predicted_role = models.CharField(max_length=100, blank=True, null=True)
    confidence_score = models.FloatField(default=0.0)
    score = models.IntegerField(default=0)
    extracted_skills = models.JSONField(default=list, blank=True)
    recommended_skills = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"Resume {self.id} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
