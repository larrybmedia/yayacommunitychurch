from datetime import datetime
from extensions import db

class Stream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(500), nullable=False)  # The link to YouTube/Zoom/Mixlr
    is_live = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())