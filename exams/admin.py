from django.contrib import admin
from .models import Exam, ExamResult, Department, Student, Lecturer

admin.site.register(Exam)
admin.site.register(ExamResult)
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Lecturer)
