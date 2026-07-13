from datetime import datetime
from extensions import db

class LiveStream(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    url = db.Column(db.String(500), nullable=False)

    is_live = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
