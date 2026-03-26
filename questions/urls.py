from django.urls import path
from . import views

urlpatterns = [
    path(
        "lecturer/add/<int:exam_id>/",
        views.add_question,
        name="add_question",
    ),
    path(
        "upload/<int:exam_id>/", views.upload_questions_csv, name="upload_questions_csv"
    ),
]
