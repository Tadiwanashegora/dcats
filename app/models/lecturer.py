"""
MODEL: Lecturer
Stores lecturer profile data.  Linked 1-to-1 with User.
"""
from app import db


class Lecturer(db.Model):
    __tablename__ = "lecturers"

    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    name    = db.Column(db.String(100), nullable=False)
    email   = db.Column(db.String(120), unique=True, nullable=False)

    # relationships
    user    = db.relationship("User",       back_populates="lecturer")
    classes = db.relationship("Class",      back_populates="lecturer", lazy="dynamic")

    def total_classes(self) -> int:
        return self.classes.count()

    def __repr__(self) -> str:
        return f"<Lecturer {self.name}>"
