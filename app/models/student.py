"""
MODEL: Student
Stores student profile data.  Linked 1-to-1 with User.
"""
from app import db


class Student(db.Model):
    __tablename__ = "students"

    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    name    = db.Column(db.String(100), nullable=False)
    email   = db.Column(db.String(120), unique=True, nullable=False)
    course  = db.Column(db.String(50),  nullable=False)

    # relationships
    user        = db.relationship("User",       back_populates="student")
    attendances = db.relationship("Attendance", back_populates="student", lazy="dynamic")

    def attendance_rate(self, class_id: int = None) -> float:
        """Return percentage of sessions attended (0-100)."""
        q = self.attendances
        if class_id:
            q = q.filter_by(class_id=class_id)
        total   = q.count()
        present = q.filter_by(status="present").count()
        return round((present / total * 100), 1) if total else 0.0

    def is_at_risk(self, class_id: int = None, threshold: float = 80.0) -> bool:
        return self.attendance_rate(class_id) < threshold

    def __repr__(self) -> str:
        return f"<Student {self.name} ({self.course})>"
