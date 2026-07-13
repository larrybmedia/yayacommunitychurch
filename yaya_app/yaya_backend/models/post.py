from extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))
    content = db.Column(db.Text)

    # ADD THIS
    is_global = db.Column(db.Boolean, default=False)

    branch_id = db.Column(
        db.Integer,
        db.ForeignKey('branches.id'),
        nullable=True
    )