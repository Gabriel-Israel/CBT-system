from django.contrib.auth.models import User
from django.db import models
from exams.models import Exam
from django.conf import settings


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"groups_name": "Lecturer"}
    )
    question_text = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
        ],
    )

    marks = models.IntegerField(default=1)

    def get_correct_option_text(self):
        return getattr(self, f"option_{self.correct_answer.lower()}")

    def __str__(self):
        return self.question_text[:50]
