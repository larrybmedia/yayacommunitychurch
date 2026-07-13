from extensions import db


class Branch(db.Model):
    __tablename__ = "branches"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(200),
        nullable=False,
        unique=True
    )

    address = db.Column(db.String(300))

    pastor = db.Column(db.String(150))

    state = db.Column(db.String(100))

    country = db.Column(db.String(100))

    users = db.relationship(
        "User",
        backref="branch",
        lazy=True
    )

    def __repr__(self):
        return self.name