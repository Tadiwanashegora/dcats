"""
MODEL: User
Stores login credentials and role for both lecturers and students.
Implements Flask-Login's UserMixin interface.
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role     = db.Column(db.String(10), nullable=False)   # "lecturer" | "student"

    # one-to-one back-references
    lecturer = db.relationship("Lecturer", back_populates="user", uselist=False)
    student  = db.relationship("Student",  back_populates="user", uselist=False)

    # ── helpers ────────────────────────────────────────────────────────────────
    def set_password(self, raw: str) -> None:
        self.password = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password, raw)

    def is_lecturer(self) -> bool:
        return self.role == "lecturer"

    def is_student(self) -> bool:
        return self.role == "student"

    def __repr__(self) -> str:
        return f"<User {self.username} ({self.role})>"
