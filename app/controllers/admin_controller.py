"""
CONTROLLER: Admin
Handles creating students, lecturers, and courses.
Blueprint prefix: /admin
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.lecturer import Lecturer
from app.models.student import Student
from app.models.class_model import Class

admin_bp = Blueprint("admin", __name__)


def _require_lecturer():
    if not current_user.is_authenticated or not current_user.is_lecturer():
        flash("Access restricted to lecturers.", "danger")
        return redirect(url_for("auth.login"))
    return None


# ── GET /admin/ ────────────────────────────────────────────────────────────────
@admin_bp.route("/")
@login_required
def index():
    guard = _require_lecturer()
    if guard:
        return guard
    students  = Student.query.all()
    lecturers = Lecturer.query.all()
    courses   = Class.query.all()
    return render_template("admin/index.html",
                           students=students,
                           lecturers=lecturers,
                           courses=courses)


# ── ADD STUDENT ────────────────────────────────────────────────────────────────
@admin_bp.route("/students/add", methods=["GET", "POST"])
@login_required
def add_student():
    guard = _require_lecturer()
    if guard:
        return guard

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        course   = request.form.get("course", "").strip()
        password = request.form.get("password", "").strip()

        if not all([username, name, email, course, password]):
            flash("All fields are required.", "warning")
            return redirect(url_for("admin.add_student"))

        if User.query.filter_by(username=username).first():
            flash(f"Student number '{username}' already exists.", "danger")
            return redirect(url_for("admin.add_student"))

        if Student.query.filter_by(email=email).first():
            flash(f"Email '{email}' is already registered.", "danger")
            return redirect(url_for("admin.add_student"))

        u = User(username=username, role="student")
        u.set_password(password)
        db.session.add(u)
        db.session.flush()

        stu = Student(user_id=u.id, name=name, email=email, course=course)
        db.session.add(stu)
        db.session.commit()

        flash(f"Student '{name}' added successfully!", "success")
        return redirect(url_for("admin.index"))

    return render_template("admin/add_student.html")


# ── EDIT STUDENT ───────────────────────────────────────────────────────────────
@admin_bp.route("/students/edit/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    guard = _require_lecturer()
    if guard:
        return guard

    stu = Student.query.get_or_404(student_id)

    if request.method == "POST":
        stu.name   = request.form.get("name",   stu.name).strip()
        stu.email  = request.form.get("email",  stu.email).strip()
        stu.course = request.form.get("course", stu.course).strip()
        new_pw     = request.form.get("password", "").strip()
        if new_pw:
            stu.user.set_password(new_pw)
        db.session.commit()
        flash(f"Student '{stu.name}' updated.", "success")
        return redirect(url_for("admin.index"))

    return render_template("admin/edit_student.html", stu=stu)


# ── DELETE STUDENT ─────────────────────────────────────────────────────────────
@admin_bp.route("/students/delete/<int:student_id>", methods=["POST"])
@login_required
def delete_student(student_id):
    guard = _require_lecturer()
    if guard:
        return guard

    stu = Student.query.get_or_404(student_id)
    name = stu.name
    # delete attendance records first
    from app.models.attendance import Attendance
    Attendance.query.filter_by(student_id=stu.id).delete()
    db.session.delete(stu)
    db.session.delete(stu.user)
    db.session.commit()
    flash(f"Student '{name}' deleted.", "info")
    return redirect(url_for("admin.index"))


# ── ADD LECTURER ───────────────────────────────────────────────────────────────
@admin_bp.route("/lecturers/add", methods=["GET", "POST"])
@login_required
def add_lecturer():
    guard = _require_lecturer()
    if guard:
        return guard

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not all([username, name, email, password]):
            flash("All fields are required.", "warning")
            return redirect(url_for("admin.add_lecturer"))

        if User.query.filter_by(username=username).first():
            flash(f"Username '{username}' already exists.", "danger")
            return redirect(url_for("admin.add_lecturer"))

        if Lecturer.query.filter_by(email=email).first():
            flash(f"Email '{email}' is already registered.", "danger")
            return redirect(url_for("admin.add_lecturer"))

        u = User(username=username, role="lecturer")
        u.set_password(password)
        db.session.add(u)
        db.session.flush()

        lec = Lecturer(user_id=u.id, name=name, email=email)
        db.session.add(lec)
        db.session.commit()

        flash(f"Lecturer '{name}' added successfully!", "success")
        return redirect(url_for("admin.index"))

    return render_template("admin/add_lecturer.html")


# ── ADD COURSE ─────────────────────────────────────────────────────────────────
@admin_bp.route("/courses/add", methods=["GET", "POST"])
@login_required
def add_course():
    guard = _require_lecturer()
    if guard:
        return guard

    lecturers = Lecturer.query.all()

    if request.method == "POST":
        code        = request.form.get("code", "").strip().upper()
        course_name = request.form.get("course_name", "").strip()
        lecturer_id = request.form.get("lecturer_id", type=int)

        if not all([code, course_name, lecturer_id]):
            flash("All fields are required.", "warning")
            return redirect(url_for("admin.add_course"))

        if Class.query.filter_by(code=code).first():
            flash(f"Course code '{code}' already exists.", "danger")
            return redirect(url_for("admin.add_course"))

        cls = Class(code=code, course_name=course_name, lecturer_id=lecturer_id)
        db.session.add(cls)
        db.session.commit()

        flash(f"Course '{course_name}' added successfully!", "success")
        return redirect(url_for("admin.index"))

    return render_template("admin/add_course.html", lecturers=lecturers)


# ── DELETE COURSE ──────────────────────────────────────────────────────────────
@admin_bp.route("/courses/delete/<int:class_id>", methods=["POST"])
@login_required
def delete_course(class_id):
    guard = _require_lecturer()
    if guard:
        return guard

    cls = Class.query.get_or_404(class_id)
    name = cls.course_name
    from app.models.attendance import Attendance
    Attendance.query.filter_by(class_id=cls.id).delete()
    db.session.delete(cls)
    db.session.commit()
    flash(f"Course '{name}' deleted.", "info")
    return redirect(url_for("admin.index"))
