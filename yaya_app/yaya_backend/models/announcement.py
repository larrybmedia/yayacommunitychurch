from datetime import datetime
from extensions import db


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
