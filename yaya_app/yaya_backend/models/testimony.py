from extensions import db, mail
from flask import current_app
from flask_mail import Message

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
        db.ForeignKey('branches.id'),
        nullable=True)

    is_approved = db.Column(
        db.Boolean,
        default=False
    )