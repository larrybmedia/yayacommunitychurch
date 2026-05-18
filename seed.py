from app import app, db
from models import Branch, Job, Post, Event

def seed_data():
    with app.app_context():
        # 1. Clear existing data (Optional - use with caution!)
        db.drop_all()
        db.create_all()

        print("Creating branches...")
        b1 = Branch(name="Lagos Central", location="Lagos", stream_url="https://youtube.com/live/example1")
        b2 = Branch(name="Abuja Glory Tabernacle", location="Abuja", stream_url="https://facebook.com/live/example2")
        b3 = Branch(name="Port Harcourt Victory", location="Rivers", stream_url="")
        
        db.session.add_all([b1, b2, b3])
        db.session.commit() # Commit to get IDs

        print("Creating news posts...")
        p1 = Post(title="National Youth Convention 2026", 
                  content="Join us for the annual convention at the Redemption Camp. Theme: Beyond Limits.", 
                  is_global=True)
        
        p2 = Post(title="Lagos Youth Vigil", 
                  content="This Friday at the Central Parish. Don't miss it!", 
                  is_global=False, 
                  branch_id=b1.id)
        
        db.session.add_all([p1, p2])

        print("Creating job opportunities...")
        j1 = Job(title="Graphic Designer", 
                 company="Kingdom Media", 
                 description="Looking for a creative mind to handle social media designs.", 
                 is_global=True)
        
        j2 = Job(title="Accountant", 
                 company="Local Logistics Firm", 
                 description="Required for a firm based in Abuja. Must be ICAN certified.", 
                 is_global=False, 
                 branch_id=b2.id)

        db.session.add_all([j1, j2])

        print("Creating events...")
        e1 = Event(title="National Sports Festival", date="May 20, 2026", time="08:00 AM", is_national=True)
        
        db.session.add_all([e1])

        db.session.commit()
        print("Database seeded successfully! You can now run 'python app.py'")

if __name__ == "__main__":
    seed_data()