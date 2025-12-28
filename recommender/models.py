from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username

class Recommendation(models.Model):
    ACTIVITY_CHOICES = [
        ('IT', 'IT'),
        ('Education', 'Education'),
        ('Bank', 'Bank'),
        ('Medical', 'Medical'),
        ('Telecom', 'Telecom'),
        ('Other', 'Other')
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    activity_field = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    storage_needs = models.FloatField()
    supports_encryption = models.BooleanField()
    cpu_speed = models.FloatField()
    price_per_hour = models.FloatField()
    service_model_score = models.IntegerField()
    recommended_provider = models.CharField(max_length=100)
    provider_details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Cloud Recommendation"
        verbose_name_plural = "Cloud Recommendations"

    def __str__(self):
        return f"{self.name} → {self.recommended_provider}"