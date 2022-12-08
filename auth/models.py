from django.contrib.auth.models import User
from django.db import models


class SecurityQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.question}"
