from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Exam(models.Model):
    title = models.CharField(max_length=200)
    total_marks = models.IntegerField(default=100)
    duration = models.IntegerField(help_text="Duration in minutes")

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True
    )

    departments = models.ManyToManyField(Department, related_name="exams", blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Student(models.Model):
    full_name = models.CharField(max_length=200)
    matric_number = models.CharField(max_length=50, unique=True)

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="students"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.matric_number})"


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1)
    marks = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    score = models.IntegerField()
    total_marks = models.IntegerField()
    percentage = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("exam", "student")  # ✅ PREVENT RETAKE

    def __str__(self):
        return f"{self.student.matric_number} - {self.exam.title}"


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.user.username
