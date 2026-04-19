from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.class_model import Class
from app.models.attendance import Attendance

student_bp = Blueprint("student", __name__)


def _require_student():
    if not current_user.is_authenticated or not current_user.is_student():
        flash("Access restricted to students.", "danger")
        return redirect(url_for("auth.login"))
    return None


@student_bp.route("/")
@student_bp.route("/dashboard")
@login_required
def dashboard():
    guard = _require_student()
    if guard:
        return guard

    stu     = current_user.student
    classes = Class.query.all()

    summary = []
    for cls in classes:
        records = (
            Attendance.query
            .filter_by(student_id=stu.id, class_id=cls.id)
            .order_by(Attendance.date.desc())
            .all()
        )
        total   = len(records)
        present = sum(1 for r in records if r.status == "present")
        rate    = round(present / total * 100, 1) if total else 0.0
        summary.append({
            "class":   cls,
            "total":   total,
            "present": present,
            "absent":  total - present,
            "rate":    rate,
            "at_risk": rate < 80,
            "records": records[:5],
        })

    overall_rate = (
        round(sum(s["rate"] for s in summary) / len(summary), 1)
        if summary else 0.0
    )

    return render_template(
        "student/dashboard.html",
        stu=stu,
        summary=summary,
        overall_rate=overall_rate,
    )


@student_bp.route("/attendance/<int:class_id>")
@login_required
def view_attendance(class_id):
    guard = _require_student()
    if guard:
        return guard

    stu     = current_user.student
    cls     = Class.query.get_or_404(class_id)
    records = (
        Attendance.query
        .filter_by(student_id=stu.id, class_id=class_id)
        .order_by(Attendance.date.desc())
        .all()
    )
    total   = len(records)
    present = sum(1 for r in records if r.status == "present")
    rate    = round(present / total * 100, 1) if total else 0.0

    return render_template(
        "student/view_attendance.html",
        stu=stu,
        cls=cls,
        records=records,
        total=total,
        present=present,
        absent=total - present,
        rate=rate,
        at_risk=rate < 80,
    )
