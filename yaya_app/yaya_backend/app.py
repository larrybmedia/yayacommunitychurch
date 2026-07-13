from dotenv import load_dotenv
import os
import humanize
from datetime import timedelta

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    jsonify
)

from flask_login import (
    LoginManager,
    login_required,
    login_user,
    current_user
)

from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash

# =========================================================
# CORE APPLICATION DEPENDENCIES & EXTENSIONS
# =========================================================
from models import (
    Branch,
    User,
    Admin,
    Manual,
    Job,
    Application,
    LiveStream,
    Announcement,
    Log,
    Testimony,
)

from extensions import (
    db,
    mail,
    login_manager,
    migrate,
    jwt,
)
from blueprints.main import main
from blueprints.admin import admin_bp
from blueprints.api import api_bp

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================
load_dotenv()

app = Flask(__name__)

# =========================================================
# SECURITY CONFIGURATION
# =========================================================
SERVER_KEY = os.getenv("SERVER_VERIFICATION_KEY")
SUPER_ADMIN_USERNAME = os.getenv("SUPER_ADMIN_USERNAME")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

@app.template_filter('humanize')
def humanize_filter(value):
    return humanize.naturaltime(value)

@app.context_processor
def inject_branches():
    return {
        "branches": Branch.query.order_by(Branch.name).all()
    }

# =========================================================
# DATABASE & SERVICE STORAGE CONFIGURATIONS
# =========================================================
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///yaya_local.db")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config["SERVER_VERIFICATION_KEY"] = SERVER_KEY

# Mail Configurations
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Directory Settings
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'resumes'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'manuals'), exist_ok=True)

# =========================================================
# HELPER ACTIONS & SYSTEM FUNCTIONS
# =========================================================
def create_superadmin():
    username = SUPER_ADMIN_USERNAME or "superadmin"
    password = SUPER_ADMIN_PASSWORD or "SuperAdmin@2026"

    admin = Admin.query.filter_by(username=username).first()
    if not admin:
        admin = Admin(
            username=username,
            password_hash=generate_password_hash(password),
            role="superadmin"
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Superadmin '{username}' initialized successfully.")

def reset_superadmin():
    username = SUPER_ADMIN_USERNAME or "superadmin"
    password = SUPER_ADMIN_PASSWORD or "SuperAdmin@2026"

    admin = Admin.query.filter_by(username=username).first()
    if admin:
        db.session.delete(admin)
        db.session.commit()

    new_admin = Admin(
        username=username,
        password_hash=generate_password_hash(password),
        role="superadmin"
    )
    db.session.add(new_admin)
    db.session.commit()
    print("Superadmin reset successful")

# =========================================================
# SYSTEM SERVICE BINDINGS & LIFECYCLE FORCING
# =========================================================
db.init_app(app)
mail.init_app(app)
login_manager.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

# Executed immediately on engine compilation for container workers
with app.app_context():
    create_superadmin()

# =========================================================
# LOGIN MANAGER
# =========================================================

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Admin, int(user_id))

# =========================================================
# REGISTER BLUEPRINTS
# =========================================================

app.register_blueprint(main)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(api_bp, url_prefix="/api")

# =========================================================
# RUN APP
# =========================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
