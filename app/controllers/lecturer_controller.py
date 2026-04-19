from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.lecturer import Lecturer
from app.models.student import Student
from app.models.class_model import Class
from app.models.attendance import Attendance

lecturer_bp = Blueprint("lecturer", __name__)


def _require_lecturer():
    if not current_user.is_authenticated or not current_user.is_lecturer():
        flash("Access restricted to lecturers.", "danger")
        return redirect(url_for("auth.login"))
    return None


@lecturer_bp.route("/")
@lecturer_bp.route("/dashboard")
@login_required
def dashboard():
    guard = _require_lecturer()
    if guard:
        return guard

    lec = current_user.lecturer
    classes = lec.classes.all()

    stats = {
        "total_classes":  len(classes),
        "total_sessions": sum(c.total_sessions() for c in classes),
        "avg_attendance": round(
            sum(c.average_attendance() for c in classes) / len(classes), 1
        ) if classes else 0,
        "at_risk_count": _count_at_risk(classes),
    }
    return render_template("lecturer/dashboard.html", lec=lec, classes=classes, stats=stats)


@lecturer_bp.route("/record", methods=["GET", "POST"])
@login_required
def record_attendance():
    guard = _require_lecturer()
    if guard:
        return guard

    lec      = current_user.lecturer
    classes  = lec.classes.all()
    students = Student.query.all()

    if request.method == "POST":
        class_id     = request.form.get("class_id", type=int)
        session_date = request.form.get("session_date")

        if not class_id or not session_date:
            flash("Please select a class and date.", "warning")
            return redirect(url_for("lecturer.record_attendance"))

        try:
            session_date = date.fromisoformat(session_date)
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for("lecturer.record_attendance"))

        for stu in students:
            status = request.form.get(f"status_{stu.id}", "absent")
            Attendance.record(stu.id, class_id, session_date, status)

        db.session.commit()
        flash("Attendance saved successfully!", "success")
        return redirect(url_for("lecturer.dashboard"))

    today = date.today().isoformat()
    return render_template(
        "lecturer/record_attendance.html",
        classes=classes,
        students=students,
        today=today,
    )


@lecturer_bp.route("/records")
@login_required
def view_records():
    guard = _require_lecturer()
    if guard:
        return guard

    lec      = current_user.lecturer
    classes  = lec.classes.all()
    students = Student.query.all()

    class_id   = request.args.get("class_id",   type=int)
    student_id = request.args.get("student_id", type=int)
    status     = request.args.get("status",     "")

    query = Attendance.query.join(Class).filter(Class.lecturer_id == lec.id)
    if class_id:
        query = query.filter(Attendance.class_id == class_id)
    if student_id:
        query = query.filter(Attendance.student_id == student_id)
    if status in ("present", "absent"):
        query = query.filter(Attendance.status == status)

    records = query.order_by(Attendance.date.desc()).all()

    return render_template(
        "lecturer/view_records.html",
        classes=classes,
        students=students,
        records=records,
        selected_class=class_id,
        selected_student=student_id,
        selected_status=status,
    )


def _count_at_risk(classes):
    at_risk = set()
    for cls in classes:
        for stu in Student.query.all():
            if stu.is_at_risk(cls.id):
                at_risk.add(stu.id)
    return len(at_risk)
