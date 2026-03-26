from django.urls import path
from . import views

urlpatterns = [
    path("student-login/", views.student_login, name="student_login"),
    path("", views.exam_list, name="exam_list"),
    path("<int:exam_id>/", views.start_exam, name="start_exam"),
    path("<int:exam_id>/submit/", views.submit_exam, name="submit_exam"),
    path("lecturer/login/", views.lecturer_login, name="lecturer_login"),
    path("lecturer/dashboard/", views.lecturer_dashboard, name="lecturer_dashboard"),
    path("student/logout/", views.student_logout, name="student_logout"),
    path("lecturer/logout/", views.lecturer_logout, name="lecturer_logout"),
]
