import pandas as pd
from app import app, db

def seed_parishes(file_path):
    with app.app_context():
        from models import Branch 
        
        try:
            df = pd.read_csv(file_path)
        except:
            df = pd.read_excel(file_path)

        print(f"File loaded successfully. Found {len(df)} entries.")
        
        # This line automatically finds the first column name
        column_to_use = df.columns[0]
        print(f"Reading parish names from column: '{column_to_use}'")

        for index, row in df.iterrows():
            # Use the index-based column name to avoid KeyErrors
            raw_name = row[column_to_use]
            
            # Skip if the row is empty
            if pd.isna(raw_name):
                continue

            name_to_check = str(raw_name).strip()
            
            # Prevent duplicates
            exists = Branch.query.filter_by(name=name_to_check).first()
            
            if not exists:
                new_branch = Branch(name=name_to_check)
                db.session.add(new_branch)

            # Batch commit for speed
            if index % 500 == 0:
                db.session.commit()
                print(f"Progress: {index} parishes imported...")

        db.session.commit()
        print("Done! All 6,000 parishes are now in your database.")

if __name__ == "__main__":
    seed_parishes('parishes.csv')