from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.student import Student
from app.models.class_model import Class
from app.models.attendance import Attendance

report_bp = Blueprint("reports", __name__)


def _require_lecturer():
    if not current_user.is_authenticated or not current_user.is_lecturer():
        flash("Access restricted to lecturers.", "danger")
        return redirect(url_for("auth.login"))
    return None


@report_bp.route("/")
@login_required
def index():
    guard = _require_lecturer()
    if guard:
        return guard

    lec     = current_user.lecturer
    classes = lec.classes.all()
    return render_template("lecturer/reports_index.html", classes=classes)


@report_bp.route("/<int:class_id>")
@login_required
def class_report(class_id):
    guard = _require_lecturer()
    if guard:
        return guard

    lec = current_user.lecturer
    cls = Class.query.get_or_404(class_id)

    if cls.lecturer_id != lec.id:
        flash("You do not have access to this class report.", "danger")
        return redirect(url_for("reports.index"))

    students = Student.query.all()
    rows = []
    for stu in students:
        records = (
            Attendance.query
            .filter_by(student_id=stu.id, class_id=class_id)
            .order_by(Attendance.date)
            .all()
        )
        total   = len(records)
        present = sum(1 for r in records if r.status == "present")
        absent  = total - present
        rate    = round(present / total * 100, 1) if total else 0.0
        rows.append({
            "student": stu,
            "total":   total,
            "present": present,
            "absent":  absent,
            "rate":    rate,
            "at_risk": rate < 80,
            "records": records,
        })

    rows.sort(key=lambda r: (not r["at_risk"], r["rate"]))

    return render_template(
        "lecturer/class_report.html",
        cls=cls,
        rows=rows,
        avg=cls.average_attendance(),
        sessions=cls.total_sessions(),
    )
