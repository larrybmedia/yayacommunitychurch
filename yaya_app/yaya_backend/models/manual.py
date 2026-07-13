from extensions import db

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
