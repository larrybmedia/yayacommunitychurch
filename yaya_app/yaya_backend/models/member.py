from extensions import db
from datetime import datetime


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(150), nullable=False)

    gender = db.Column(db.String(20))

    date_of_birth = db.Column(db.Date)

    email = db.Column(db.String(120), unique=True)

    phone = db.Column(db.String(20))

    address = db.Column(db.Text)

    occupation = db.Column(db.String(150))

    marital_status = db.Column(db.String(30))

    baptism_status = db.Column(db.String(30))

    worker = db.Column(db.Boolean, default=False)

    department = db.Column(db.String(100))

    status = db.Column(db.String(30), default="Active")

    joined_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    branch_id = db.Column(
        db.Integer,
        db.ForeignKey("branches.id"),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Member {self.full_name}>"