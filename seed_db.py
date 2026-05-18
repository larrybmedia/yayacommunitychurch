import pandas as pd
from app import app, db
from models import Admin, Branch 

def seed_parishes(file_path):
    df = pd.read_csv(file_path)
    print("CSV Columns found:", df.columns.tolist()) 
    for index, row in df.iterrows():
        # Updated to 'Name' to match your CSV header
        existing = Branch.query.filter_by(name=row['Name']).first()
        if not existing:
            # Updated to 'Name' and 'Location' to match your CSV headers
            new_branch = Branch(name=row['Name'], location=row['Location'])
            db.session.add(new_branch)
    db.session.commit() # Important: This saves the changes!

if __name__ == '__main__':
    with app.app_context():
        print("Creating database tables...")
        db.create_all() 
        
        # --- CREATING MULTIPLE ADMINS ---
        
        # Define a list of admins you want to create
        admins_to_create = [
            {"user": "admin_main", "pass": "YAYA2026"},
            {"user": "pastor_office", "pass": "Lagos2024"},
            {"user": "secretary_user", "pass": "SecurePass789"}
        ]

        for account in admins_to_create:
            # Check if this specific username already exists
            existing = Admin.query.filter_by(username=account["user"]).first()
            
            if not existing:
                print(f"Creating admin user: {account['user']}...")
                new_admin = Admin(username=account["user"])
                new_admin.set_password(account["pass"])
                db.session.add(new_admin)
            else:
                print(f"Admin '{account['user']}' already exists. Skipping.")

        db.session.commit()
        
        # --- SEEDING PARISHES ---
        print("Seeding parishes...")
        seed_parishes('parishes.csv')
        print("All done!")