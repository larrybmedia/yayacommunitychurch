import os
from flask import Flask
from models import db, Branch
from routes.main import main as main_blueprint

app = Flask(__name__)

# --- CONFIGURATION ---
# Use an absolute path for the database to avoid "table not found" errors
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'platform.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yaya_platform_secret_key'

# Define and create the path for resume uploads
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads', 'resumes')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- DATABASE INITIALIZATION ---
db.init_app(app)

# --- BLUEPRINT REGISTRATION ---
app.register_blueprint(main_blueprint)

# --- CONTEXT PROCESSOR ---
# This makes 'branches' available in the dropdown of every single page (base.html)
@app.context_processor
def inject_branches():
    from models import Branch  # Ensure you import your Branch model
    return dict(branches=Branch.query.all())

# --- APP STARTUP ---
if __name__ == "__main__":
    with app.app_context():
        # This creates your platform.db and all tables defined in models.py
        db.create_all()  
    app.run(debug=True)