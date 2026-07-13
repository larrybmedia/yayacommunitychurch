from extensions import db
from datetime import datetime

# =========================
# JOBS
# =========================
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    is_global = db.Column(db.Boolean, default=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=True)

    # NEW (production control)
    is_approved = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id'))

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

class Application(db.Model):

    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(
        db.Integer,
        db.ForeignKey('job.id'),
        nullable=False
    )

    user_name = db.Column(
        db.String(100),
        nullable=False
    )

    user_email = db.Column(
        db.String(100),
        nullable=False
    )

    resume_filename = db.Column(
        db.String(255)
    )

    date_applied = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
