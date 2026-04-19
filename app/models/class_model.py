"""
MODEL: Class
Represents a course/module taught by a lecturer.
"""
from app import db


class Class(db.Model):
    __tablename__ = "classes"

    id          = db.Column(db.Integer, primary_key=True)
    code        = db.Column(db.String(20),  unique=True, nullable=False)
    course_name = db.Column(db.String(150), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey("lecturers.id"), nullable=False)

    # relationships
    lecturer    = db.relationship("Lecturer",   back_populates="classes")
    attendances = db.relationship("Attendance", back_populates="class_obj", lazy="dynamic")

    def total_sessions(self) -> int:
        """Count distinct session dates recorded for this class."""
        from sqlalchemy import func
        from app.models.attendance import Attendance
        result = (
            db.session.query(func.count(func.distinct(Attendance.date)))
            .filter(Attendance.class_id == self.id)
            .scalar()
        )
        return result or 0

    def average_attendance(self) -> float:
        """Return the average attendance rate across all students (0-100)."""
        from app.models.student import Student
        from app.models.attendance import Attendance

        students = (
            db.session.query(Student)
            .join(Attendance, Attendance.student_id == Student.id)
            .filter(Attendance.class_id == self.id)
            .distinct()
            .all()
        )
        if not students:
            return 0.0
        rates = [s.attendance_rate(self.id) for s in students]
        return round(sum(rates) / len(rates), 1)

    def __repr__(self) -> str:
        return f"<Class {self.code}: {self.course_name}>"
