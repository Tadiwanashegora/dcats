from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.models.lecturer import Lecturer
from app.models.student import Student

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return _redirect_by_role(current_user)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {username}!", "success")
            return _redirect_by_role(user)
        flash("Invalid username or password. Please try again.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


# ── REGISTER STUDENT ───────────────────────────────────────────────────────────
@auth_bp.route("/register/student", methods=["GET", "POST"])
def register_student():
    if current_user.is_authenticated:
        return _redirect_by_role(current_user)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        course   = request.form.get("course", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm", "")

        # Validation
        if not all([username, name, email, course, password, confirm]):
            flash("All fields are required.", "warning")
            return redirect(url_for("auth.register_student"))

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register_student"))

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "warning")
            return redirect(url_for("auth.register_student"))

        if User.query.filter_by(username=username).first():
            flash(f"Student number '{username}' is already registered.", "danger")
            return redirect(url_for("auth.register_student"))

        if Student.query.filter_by(email=email).first():
            flash(f"Email '{email}' is already registered.", "danger")
            return redirect(url_for("auth.register_student"))

        u = User(username=username, role="student")
        u.set_password(password)
        db.session.add(u)
        db.session.flush()

        stu = Student(user_id=u.id, name=name, email=email, course=course)
        db.session.add(stu)
        db.session.commit()

        login_user(u)
        flash(f"Account created! Welcome, {name}!", "success")
        return redirect(url_for("student.dashboard"))

    return render_template("auth/register_student.html")


# ── REGISTER LECTURER ──────────────────────────────────────────────────────────
@auth_bp.route("/register/lecturer", methods=["GET", "POST"])
def register_lecturer():
    if current_user.is_authenticated:
        return _redirect_by_role(current_user)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm", "")

        if not all([username, name, email, password, confirm]):
            flash("All fields are required.", "warning")
            return redirect(url_for("auth.register_lecturer"))

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register_lecturer"))

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "warning")
            return redirect(url_for("auth.register_lecturer"))

        if User.query.filter_by(username=username).first():
            flash(f"Username '{username}' is already taken.", "danger")
            return redirect(url_for("auth.register_lecturer"))

        if Lecturer.query.filter_by(email=email).first():
            flash(f"Email '{email}' is already registered.", "danger")
            return redirect(url_for("auth.register_lecturer"))

        u = User(username=username, role="lecturer")
        u.set_password(password)
        db.session.add(u)
        db.session.flush()

        lec = Lecturer(user_id=u.id, name=name, email=email)
        db.session.add(lec)
        db.session.commit()

        login_user(u)
        flash(f"Account created! Welcome, {name}!", "success")
        return redirect(url_for("lecturer.dashboard"))

    return render_template("auth/register_lecturer.html")


def _redirect_by_role(user):
    if user.is_lecturer():
        return redirect(url_for("lecturer.dashboard"))
    return redirect(url_for("student.dashboard"))
