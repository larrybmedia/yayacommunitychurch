import bcrypt
from flask_mail import Mail, Message
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# DATABASE
db = SQLAlchemy()

# MAIL
mail = Mail()


# =========================
# EMAIL NOTIFICATION
# =========================
def send_admin_notification(testimony):

    msg = Message(
        subject=f"New Testimony: {testimony.title}",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[current_app.config['MAIL_USERNAME']]
    )

    msg.body = f"""
A new testimony has been submitted.

Name: {testimony.name}

Title: {testimony.title}

Content:
{testimony.content}
"""

    mail.send(msg)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(200))
    admin_email = db.Column(db.String(150), unique=True)
    role = db.Column(db.String(20))  # admin / superadmin
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

# =========================
# BRANCH MODEL
# =========================
class Branch(db.Model):
    __tablename__ = 'branch'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    youtube_link = db.Column(db.String(255))  # Store the "embed" link here
    calendar_updates = db.Column(db.Text)    # Store events or updates
    # ADD THIS
    location = db.Column(db.String(200))

    # OPTIONAL livestream
    stream_url = db.Column(db.String(500))
    
    # This must exist for Admin to "talk" to it
    admins = db.relationship('Admin', backref='branch', lazy=True)
    # This must exist for Post to "talk" to it
    posts = db.relationship('Post', backref='branch', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))
    content = db.Column(db.Text)

    # ADD THIS
    is_global = db.Column(db.Boolean, default=False)

    branch_id = db.Column(
        db.Integer,
        db.ForeignKey('branch.id'),
        nullable=True
    )

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='admin')
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

# =========================
# JOBS
# =========================
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    is_global = db.Column(db.Boolean, default=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)

    # NEW (production control)
    is_approved = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id'))

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

# =========================
# EVENTS
# =========================
class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String(200), nullable=True, default='Main Auditorium')
    is_global = db.Column(db.Boolean, default=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)

    def __repr__(self):
        return f"<Event {self.title}>"


# =========================
# TESTIMONIES
# =========================
class Testimony(db.Model):

    __tablename__ = 'testimony'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    branch_id = db.Column(
        db.Integer, 
        db.ForeignKey('branch.id'), 
        nullable=True)

    is_approved = db.Column(
        db.Boolean,
        default=False
    )


# =========================
# JOB APPLICATIONS
# =========================
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


# =========================
# MANUALS
# =========================
class Manual(db.Model):

    __tablename__ = 'manual'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.String(255)
    )

    filename = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(50)
    )

    icon_class = db.Column(
        db.String(50),
        default="fa-file-pdf"
    )


# =========================
# ACTIVITY LOGS
# =========================
class ActivityLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    admin_name = db.Column(db.String(120))

    action = db.Column(db.String(255))

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

class Stream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(500), nullable=False)  # The link to YouTube/Zoom/Mixlr
    is_live = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

class BankDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(100))
    account_name = db.Column(db.String(100))
    account_number = db.Column(db.String(20))
    category = db.Column(db.String(50), default="Tithe") # New field: 'Tithe' or 'Project'
    
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(120))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    service_date = db.Column(db.DateTime, default=datetime.utcnow)

class LiveStream(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    url = db.Column(db.String(500), nullable=False)

    is_live = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# -----------------------------
# ANNOUNCEMENT MODEL
# -----------------------------
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))
    content = db.Column(db.Text)

    image = db.Column(db.String(255))
    video_file = db.Column(db.String(255))
    video = db.Column(db.String(500))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )