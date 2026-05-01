from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., "Lagos Province 1"
    location = db.Column(db.String(100))               # e.g., "Lagos"
    stream_url = db.Column(db.String(255))             # YouTube/Facebook Live link
    
    # Relationships
    posts = db.relationship('Post', backref='branch', lazy=True)
    jobs = db.relationship('Job', backref='branch', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Critical for the Branch Filtering logic:
    is_global = db.Column(db.Boolean, default=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Critical for the Branch Filtering logic:
    is_global = db.Column(db.Boolean, default=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)
    
    # Relationship to applications
    applications = db.relationship('Application', backref='job', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    
    # Filtering fields
    is_global = db.Column(db.Boolean, default=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)

class Testimony(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=True) # For Anonymous option
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    resume_filename = db.Column(db.String(255))  # Stores the name of the file
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)

class Manual(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    filename = db.Column(db.String(100), nullable=False) # Stores the name of the PDF file
    category = db.Column(db.String(50)) # e.g., 'Leadership', 'Study', 'Protocol'

class Branch(db.Model):
    __tablename__ = 'branch'
    __table_args__ = {'extend_existing': True} # Add this line!

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    # ... your other columns ...