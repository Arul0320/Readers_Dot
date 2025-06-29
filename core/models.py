from django.db import models
from django.contrib.auth.models import User
import random
import string

class Paragraph(models.Model):
    content = models.TextField()
    otp = models.CharField(max_length=6, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.otp:
            # Generate a 6-digit OTP
            self.otp = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Paragraph {self.id} - OTP: {self.otp}"

class StudentResult(models.Model):
    student_name = models.CharField(max_length=100)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def score_percentage(self):
        if self.total_questions > 0:
            return round((self.score / self.total_questions) * 100)
        return 0

    def __str__(self):
        return f"{self.student_name} - Score: {self.total_questions}"