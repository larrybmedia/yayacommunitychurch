from datetime import datetime
from extensions import db

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(120))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    service_date = db.Column(db.DateTime, default=datetime.utcnow)