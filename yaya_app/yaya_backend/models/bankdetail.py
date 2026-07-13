from extensions import db

class BankDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(100))
    account_name = db.Column(db.String(100))
    account_number = db.Column(db.String(20))
    category = db.Column(db.String(50), default="Tithe") # New field: 'Tithe' or 'Project'