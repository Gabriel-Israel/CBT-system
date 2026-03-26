import csv
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Question
from exams.models import Exam

import csv
from io import TextIOWrapper
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from exams.models import Exam
from .forms import CSVUploadForm

from django.contrib import messages


@login_required
def add_question(request, exam_id):
    exam = Exam.objects.get(id=exam_id)

    if request.method == "POST":
        Question.objects.create(
            exam=exam,
            question_text=request.POST.get("question_text"),
            option_a=request.POST.get("option_a"),
            option_b=request.POST.get("option_b"),
            option_c=request.POST.get("option_c"),
            option_d=request.POST.get("option_d"),
            correct_answer=request.POST.get("correct_answer"),
            marks=request.POST.get("marks"),
            created_by=request.user,  # ✅ THIS IS THE KEY LINE
        )
        return redirect("add_question", exam_id=exam_id)

    return render(request, "questions/add_question.html", {"exam": exam})


@login_required
def upload_questions_csv(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    if exam.created_by != request.user:
        messages.error(
            request, "You are not allowed to upload questions for this exams."
        )
        return redirect("lecturer_dashboard")

    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")

        if not csv_file:
            messages.error(request, "No file selected.")
            return redirect(request.path)

        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded_file)

        count = 0
        for row in reader:
            if len(row) < 6:
                continue

            Question.objects.create(
                exam=exam,
                question_text=row[0],
                option_a=row[1],
                option_b=row[2],
                option_c=row[3],
                option_d=row[4],
                correct_answer=row[5],
                created_by=request.user,
            )
            count += 1

        messages.success(request, f"{count} questions uploaded successfully!")

        return redirect(request.path)

    return render(request, "questions/upload_csv.html", {"exam": exam})
