from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name="default"):
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ── Configuration ──────────────────────────────────────────────────────────
    if config_name == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dcats.db"

    app.config["SECRET_KEY"] = "dcats-sps611s-secret-key"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── Extensions ─────────────────────────────────────────────────────────────
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    # ── User loader (required by Flask-Login) ──────────────────────────────────
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # ── Register Blueprints (Controllers) ──────────────────────────────────────
    from app.controllers.auth_controller import auth_bp
    from app.controllers.lecturer_controller import lecturer_bp
    from app.controllers.student_controller import student_bp
    from app.controllers.report_controller import report_bp
    from app.controllers.admin_controller import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(lecturer_bp, url_prefix="/lecturer")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(report_bp, url_prefix="/reports")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # ── Create tables and seed data ────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        _seed_database()

    return app


def _seed_database():
    """Populate demo data if the database is empty."""
    from app.models.user import User
    from app.models.lecturer import Lecturer
    from app.models.student import Student
    from app.models.class_model import Class
    from app.models.attendance import Attendance
    from datetime import date, timedelta

    if User.query.first():
        return  # already seeded

    # ── Lecturers ──────────────────────────────────────────────────────────────
    lecturers_data = [
        {"username": "staff01", "name": "Dr. Amupolo", "email": "amupolo@nust.na"},
        {"username": "staff02", "name": "Ms. Nghifindaka", "email": "nghifindaka@nust.na"},
    ]
    lecturers = []
    for ld in lecturers_data:
        u = User(username=ld["username"], role="lecturer")
        u.set_password("pass123")
        db.session.add(u)
        db.session.flush()
        lec = Lecturer(user_id=u.id, name=ld["name"], email=ld["email"])
        db.session.add(lec)
        db.session.flush()
        lecturers.append(lec)

    # ── Students ───────────────────────────────────────────────────────────────
    students_data = [
        {"username": "223010006", "name": "Philipus Nefuma",  "email": "philipus@nust.na",  "course": "BIT"},
        {"username": "222101717", "name": "Esther Gabriel",   "email": "esther@nust.na",    "course": "BIT"},
        {"username": "223081965", "name": "Elikana Joba",     "email": "elikana@nust.na",   "course": "BIT"},
        {"username": "221026916", "name": "Kelvin Gora",      "email": "kelvin@nust.na",    "course": "BIT"},
        {"username": "214021254", "name": "Markus NFT",       "email": "markus@nust.na",    "course": "BIT"},
    ]
    students = []
    for sd in students_data:
        u = User(username=sd["username"], role="student")
        u.set_password("pass123")
        db.session.add(u)
        db.session.flush()
        stu = Student(user_id=u.id, name=sd["name"], email=sd["email"], course=sd["course"])
        db.session.add(stu)
        db.session.flush()
        students.append(stu)

    # ── Classes ────────────────────────────────────────────────────────────────
    classes_data = [
        {"code": "SPS611S", "name": "Software Processes",    "lecturer": lecturers[0]},
        {"code": "DBS501S", "name": "Database Systems",      "lecturer": lecturers[0]},
        {"code": "NET401S", "name": "Network Fundamentals",  "lecturer": lecturers[1]},
    ]
    classes = []
    for cd in classes_data:
        cls = Class(
            code=cd["code"],
            course_name=cd["name"],
            lecturer_id=cd["lecturer"].id,
        )
        db.session.add(cls)
        db.session.flush()
        classes.append(cls)

    # ── Attendance records (last 8 sessions per class) ─────────────────────────
    import random
    random.seed(42)
    today = date.today()
    for cls in classes:
        for week in range(8):
            session_date = today - timedelta(days=(7 * week + 2))
            for stu in students:
                status = "present" if random.random() > 0.25 else "absent"
                att = Attendance(
                    student_id=stu.id,
                    class_id=cls.id,
                    date=session_date,
                    status=status,
                )
                db.session.add(att)

    db.session.commit()
