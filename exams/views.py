import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Exam, ExamResult, Student, Department, Lecturer
from questions.models import Question
from exams.models import Student


def exam_list(request):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_login")

    student = Student.objects.get(id=student_id)
    exams = Exam.objects.filter(departments=student.department)

    return render(
        request,
        "exams/exam_list.html",
        {
            "exams": exams,
            "student": student,
        },
    )


def start_exam(request, exam_id):
    if "student_id" not in request.session:
        return redirect("student_login")
    exam = get_object_or_404(Exam, id=exam_id)

    # ✅ CORRECT PLACE
    questions = list(exam.question_set.all())
    random.shuffle(questions)

    context = {
        "exam": exam,
        "questions": questions,
        "exam_duration_minutes": exam.duration,
    }

    return render(request, "exams/start_exam.html", context)


def submit_exam(request, exam_id):
    if "student_id" not in request.session:
        return redirect("student_login")
    exam = get_object_or_404(Exam, id=exam_id)

    # get student from session
    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("student_login")
    student = Student.objects.get(id=student_id)

    # Prevent double submission
    if ExamResult.objects.filter(exam=exam, student=student).exists():
        return render(request, "exams/already_submitted.html", {"exam": exam})

    questions = exam.question_set.all()

    score = 0
    total_marks = exam.total_marks

    if request.method == "POST":
        for question in questions:
            selected = request.POST.get(f"question_{question.id}")
            if selected == question.correct_answer:
                score += question.marks

        percentage = (score / total_marks) * 100 if total_marks > 0 else 0
        # ✅ Grading logic (SAFE – no DB)
        if percentage >= 70:
            grade = "A"
            remark = "Excellent"
        elif percentage >= 60:
            grade = "B"
            remark = "Very Good"
        elif percentage >= 50:
            grade = "C"
            remark = "Good"
        elif percentage >= 45:
            grade = "D"
            remark = "Fair"
        else:
            grade = "F"
            remark = "Fail"

        result = ExamResult.objects.create(
            exam=exam,
            student=student,
            score=score,
            total_marks=total_marks,
            percentage=percentage,
        )

        # ✅ THIS IS THE MOST IMPORTANT PART
        return render(
            request,
            "exams/result.html",
            {
                "exam": exam,
                "result": result,
                "grade": grade,
                "remark": remark,
            },
        )


def student_login(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        matric_number = request.POST.get("matric_number")
        department_id = request.POST.get("department")

        if not department_id:
            return render(
                request,
                "exams/student_login.html",
                {
                    "error": "Please select a department",
                    "departments": Department.objects.all(),
                },
            )

        department = Department.objects.get(id=department_id)

        try:
            student = Student.objects.get(
                matric_number=matric_number, department=department, is_active=True
            )
        except Student.DoesNotExist:
            return render(
                request,
                "exams/student_login.html",
                {
                    "error": "Invalid matric number or department",
                    "departments": Department.objects.all(),
                    "full_name": full_name,
                    "matric_number": matric_number,
                    "department_id": department_id,
                },
            )
        request.session["student_id"] = student.id

        return redirect("exam_list")

    return render(
        request, "exams/student_login.html", {"departments": Department.objects.all()}
    )


def lecturer_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if hasattr(user, "lecturer"):
                login(request, user)
                return redirect("lecturer_dashboard")
            else:
                return render(
                    request,
                    "exams/lecturer_login.html",
                    {"error": "You are not authorized as a lecturer."},
                )
        else:
            return render(
                request,
                "exams/lecturer_login.html",
                {"error": "Invalid login details."},
            )

    return render(request, "exams/lecturer_login.html")


@login_required
def lecturer_dashboard(request):
    if not hasattr(request.user, "lecturer"):
        return redirect("lecturer_login")

    exams = Exam.objects.filter(created_by=request.user)
    return render(request, "exams/lecturer_dashboard.html", {"exams": exams})


def student_logout(request):
    logout(request)
    return redirect("student_login")


def lecturer_logout(request):
    logout(request)
    return redirect("lecturer_login")
