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
from models import db, mail

# Replaced duplicate 'db' and 'mail' model initialization bindings to preserve extensions.py stability
from models import (
    Branch,
    Admin,
    Manual,
    Job,
    mail,
    LiveStream,
    Announcement
)

from routes.main import main as main_blueprint
from forms import ManualUploadForm
from decorators import role_required
from werkzeug.security import generate_password_hash


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================
load_dotenv()

# =========================================================
# APP INITIALIZATION
# =========================================================
app = Flask(__name__)

# =========================================================
# SECURITY KEYS
# =========================================================
SERVER_KEY = os.getenv("SERVER_VERIFICATION_KEY")
SERVER_VERIFICATION_KEY = os.getenv("SERVER_VERIFICATION_KEY")
SUPER_ADMIN_USERNAME = os.getenv("SUPER_ADMIN_USERNAME")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# =========================================================
# TEMPLATE FILTER
# =========================================================
@app.template_filter('humanize')
def humanize_filter(value):
    return humanize.naturaltime(value)

# =========================================================
# CONFIGURATION
# =========================================================
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///platform.db"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yaya_platform_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config["SERVER_VERIFICATION_KEY"] = os.getenv("SERVER_VERIFICATION_KEY")

# ---------------- MAIL CONFIG ----------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

# ---------------- UPLOAD FOLDER ----------------
app.config['UPLOAD_FOLDER'] = os.path.join(
    app.root_path,
    'static',
    'uploads'
)

os.makedirs(
    os.path.join(
        app.config['UPLOAD_FOLDER'],
        'resumes'
    ),
    exist_ok=True
)

os.makedirs(
    os.path.join(
        app.config['UPLOAD_FOLDER'],
        'manuals'
    ),
    exist_ok=True
)

# =========================================================
# INITIALIZE DATABASE / MAIL
# =========================================================
db.init_app(app)
mail.init_app(app)

# =========================================================
# LOGIN MANAGER
# =========================================================
login_manager = LoginManager()

login_manager.login_view = 'main.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(
        Admin,
        int(user_id)
    )

# =========================================================
# REGISTER BLUEPRINT
# =========================================================
app.register_blueprint(main_blueprint)

# =========================================================
# FAVICON
# =========================================================
@app.route('/favicon.ico')
def favicon():
    return redirect(
        url_for(
            'static',
            filename='favicon.ico'
        )
    )

# =========================================================
# ADMIN VERIFICATION
# =========================================================
@app.route('/verify-admin', methods=['POST'])
def verify_admin():
    data=request.json
    key=data.get("server_key")

    if key==SERVER_KEY:
        return jsonify({
            "status":"success"
        })

    return jsonify({
        "status":"error"
    }),401

# =========================================================
# SUPERADMIN AUTO CREATION
# =========================================================
def create_superadmin():
    admin = Admin.query.filter_by(username="superadmin").first()

    if not admin:
        admin = Admin(
            username="superadmin",
            password_hash=generate_password_hash("SuperAdmin@2026"),
            role="superadmin"
        )
        db.session.add(admin)
        db.session.commit()


def reset_superadmin():
    admin = Admin.query.filter_by(username="superadmin").first()

    if admin:
        db.session.delete(admin)
        db.session.commit()

    from werkzeug.security import generate_password_hash

    new_admin = Admin(
        username="superadmin",
        password_hash=generate_password_hash("SuperAdmin@2026"),
        role="superadmin"
    )

    db.session.add(new_admin)
    db.session.commit()

    print("Superadmin reset successful")

# =========================================================
# SEED DATA
# =========================================================
def seed_data():
    create_superadmin()


# =========================================================
# AUTH LOGIN
# =========================================================
@app.route('/auth_login', methods=['POST'])
def auth_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Admin.query.filter_by(
        username=username
    ).first()

    if user and user.check_password(password):
        login_user(user)

        if user.role == 'superadmin':
            return redirect(
                url_for('main.super_admin_dashboard')
            )

        return redirect(
            url_for('main.admin')
        )

    flash("Invalid credentials", "danger")

    return redirect(
        url_for('main.login')
    )

# =========================================================
# GLOBAL JOB POSTING
# =========================================================
@app.route('/superadmin/post-job', methods=['GET', 'POST'])
@login_required
@role_required('superadmin')
def post_job():
    if request.method == 'POST':
        job = Job(
            title=request.form['title'],
            company=request.form['company'],
            description=request.form['description'],
            is_global=True,
            branch_id=None
        )

        db.session.add(job)
        db.session.commit()

        flash(
            "Global job posted successfully!",
            "success"
        )

        return redirect(
            url_for('main.super_admin_dashboard')
        )

    return render_template('post_job.html')

# =========================================================
# LOCAL JOB POSTING
# =========================================================
@app.route('/admin/post-job', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def post_local_job():
    if request.method == 'POST':
        job = Job(
            title=request.form['title'],
            company=request.form['company'],
            description=request.form['description'],
            is_global=False,
            branch_id=current_user.branch_id
        )

        db.session.add(job)
        db.session.commit()

        flash("Local job posted!", "success")

        return redirect(
            url_for('main.admin')
        )

    return render_template('post_local_job.html')

# =========================================================
# JOBS PAGE
# =========================================================
@app.route('/jobs')
def jobs():
    global_jobs = Job.query.filter_by(
        is_global=True
    ).all()

    if current_user.is_authenticated:
        local_jobs = Job.query.filter_by(
            is_global=False,
            branch_id=current_user.branch_id
        ).all()
    else:
        local_jobs = []

    return render_template(
        "jobs.html",
        global_jobs=global_jobs,
        local_jobs=local_jobs
    )

# =========================================================
# APPROVE JOB
# =========================================================
@app.route('/job/approve/<int:id>')
@login_required
@role_required('superadmin')
def approve_job(id):
    job = Job.query.get_or_404(id)
    job.is_approved = True
    db.session.commit()

    flash(
        "Job approved successfully",
        "success"
    )

    return redirect(
        url_for('main.super_admin_dashboard')
    )

# =========================================================
# DELETE JOB
# =========================================================
@app.route('/job/delete/<int:id>', methods=['POST'])
@login_required
def delete_job(id):
    if (
        not hasattr(current_user, 'role')
        or current_user.role != 'superadmin'
    ):
        flash("Unauthorized action!", "danger")
        return redirect(
            url_for('main.index')
        )

    job = Job.query.get_or_404(id)

    try:
        db.session.delete(job)
        db.session.commit()

        flash(
            f"Job '{job.title}' deleted successfully.",
            "success"
        )

    except Exception:
        db.session.rollback()
        flash(
            "Error deleting job.",
            "danger"
        )

    return redirect(
        url_for('main.super_admin_dashboard')
    )

# =========================================================
# EDIT JOB
# =========================================================
@app.route('/job/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('superadmin')
def edit_job(id):
    job = Job.query.get_or_404(id)

    if request.method == 'POST':
        job.title = request.form['title']
        job.company = request.form['company']
        job.description = request.form['description']

        db.session.commit()
        flash("Job updated", "success")

        return redirect(
            url_for('main.super_admin_dashboard')
        )

    return render_template(
        "edit_job.html",
        job=job
    )

# =========================================================
# CONTACT PAGE
# =========================================================
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject_type = request.form.get('subject')
        message_body = request.form.get('message')
        confidential = request.form.get('confidential')

        msg = Message(
            subject=f"New {subject_type}: From {name}",
            recipients=['info@rccgyaya.org'],
            body=f"""
New Message from RCCG YAYA Portal

Name: {name}
Email: {email}
Type: {subject_type}

Confidential:
{'YES' if confidential else 'NO'}

Message:
{message_body}
"""
        )

        try:
            mail.send(msg)
            flash(
                f"Thank you {name}, your message has been received successfully.",
                "success"
            )

        except Exception as e:
            print(f"Error: {e}")
            flash(
                "Message could not be sent.",
                "danger"
            )

        return redirect(
            url_for('contact')
        )

    return render_template('contact.html')

# =========================================================
# UPDATE STREAM
# =========================================================
@app.route('/update_stream/<int:id>', methods=['POST'])
@login_required
def update_stream(id):
    title_data = request.form.get('title')
    url_data = request.form.get('url')

    if not title_data or not url_data:
        flash(
            "Title and URL are required!",
            "danger"
        )
        return redirect(
            url_for('main.admin')
        )

    stream = LiveStream.query.get_or_404(id)

    stream.title = title_data
    stream.url = url_data

    db.session.commit()

    flash(
        "Stream updated successfully!",
        "success"
    )

    return redirect(
        url_for('main.admin')
    )

# =========================================================
# SUPERADMIN LIVE STREAM
# =========================================================
@app.route('/superadmin/upload-stream', methods=['GET', 'POST'])
@login_required
def upload_stream():
    if current_user.role != 'superadmin':
        abort(403)

    if request.method == 'POST':
        title = request.form.get('title')
        url = request.form.get('url')

        if not title or not url:
            flash(
                "Title and URL are required!",
                "danger"
            )
            return redirect(
                url_for('main.super_admin_dashboard')
            )

        stream = LiveStream(
            title=title,
            url=url
        )

        db.session.add(stream)
        db.session.commit()

        flash(
            "Live stream updated successfully!",
            "success"
        )

        return redirect(
            url_for('main.super_admin_dashboard')
        )

    return render_template(
        "admin/upload_stream.html"
    )

def init_db():
    with app.app_context():
        db.create_all()
        print("Database created successfully")


# =========================================================
# RUN APP (Unified single application entry execution engine)
# =========================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

print(app.url_map)