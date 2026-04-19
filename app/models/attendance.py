"""
MODEL: Attendance
Records a single student's status for one class session (date).
"""
from app import db
from datetime import date as date_type


class Attendance(db.Model):
    __tablename__ = "attendance"
    __table_args__ = (
        db.UniqueConstraint("student_id", "class_id", "date", name="uq_attendance"),
    )

    id         = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    class_id   = db.Column(db.Integer, db.ForeignKey("classes.id"),  nullable=False)
    date       = db.Column(db.Date,    nullable=False, default=date_type.today)
    status     = db.Column(db.String(10), nullable=False, default="absent")  # "present"|"absent"

    # relationships
    student   = db.relationship("Student", back_populates="attendances")
    class_obj = db.relationship("Class",   back_populates="attendances")

    @staticmethod
    def record(student_id: int, class_id: int, session_date: date_type, status: str):
        """Upsert an attendance record (create or update)."""
        record = Attendance.query.filter_by(
            student_id=student_id,
            class_id=class_id,
            date=session_date,
        ).first()
        if record:
            record.status = status
        else:
            record = Attendance(
                student_id=student_id,
                class_id=class_id,
                date=session_date,
                status=status,
            )
            db.session.add(record)
        return record

    def __repr__(self) -> str:
        return f"<Attendance student={self.student_id} class={self.class_id} {self.date} {self.status}>"
