from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from lectures.models import Lecture


class Grade(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    comment = models.CharField(max_length=1000, blank=True, null=True)
    submission = models.FileField(upload_to='submissions/', null=True, blank=True)

    def __str__(self):
        return f'{self.student.username} - {self.lecture.name}'

    class Meta:
        permissions = (
            ('add_comment', 'Can add comment'),
            ('change_grade_value', 'Can change grade'),
        )
