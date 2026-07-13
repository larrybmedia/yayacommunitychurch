import os
from flask_mail import Message

from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.utils import secure_filename
from flask import jsonify
# Added Testimony to the import list
from models import Announcement, Member, LiveStream, db, User, Branch, Manual, Post, Job, Log, Event, Admin,Testimony
from functools import wraps
from datetime import datetime
from extensions import db, mail
from decorators import role_required


admin_bp = Blueprint('admin', __name__, template_folder='../templates')

# --- SECURITY & UTILS ---
def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'superadmin':
            flash("Unauthorized access!", "danger")
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def log_action(admin_user, action_type, details):
    new_log = Log(
        admin_id=admin_user.id,
        action=action_type,
        details=details
    )
    db.session.add(new_log)
    db.session.commit()
# --- ROUTES ---

@admin_bp.route('/server-verification', methods=['GET', 'POST'])
def server_verification():
    if request.method == 'POST':
        if request.form.get('server_key') == "MASTER_KEY_2026":
            session['is_verified'] = True  # This unlocks the Gatekeeper
            return redirect(url_for('admin.login'))
        else:
            flash("Invalid Master Key", "danger")

    return render_template('server_verification.html')

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    # 1. Gatekeeper: Ensure verification first
    if not session.get('is_verified'):
        return redirect(url_for('admin.server_verification'))

    # 2. If already logged in, redirect them to their dashboard
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for('admin.superadmin_dashboard') if current_user.role == 'superadmin' else url_for('admin.dashboard'))

    # 3. Handle login attempt
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        portal = request.form.get('portal_type')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            # Route based on the portal they selected and their role
            if portal == 'superadmin' and user.role == 'superadmin':
                return redirect(url_for('admin.superadmin_dashboard'))
            return redirect(url_for('admin.dashboard'))

        flash("Invalid username or password.", "danger")

    return render_template('admin_login.html')

@admin_bp.route('/super-admin-dashboard')
@login_required
@superadmin_required
def superadmin_dashboard():
    member_stats = {
        'total': Member.query.count(),
        'active': Member.query.filter_by(status='Active').count(),
        'this_month': Member.query.filter(Member.joined_date >= datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).count()
    }

    all_testimonies = Testimony.query.all()
    pending_testimonies = Testimony.query.filter_by(is_approved=False).order_by(Testimony.id.desc()).all()

    # Fetch all announcements to display in the dashboard
    all_announcements = Announcement.query.order_by(Announcement.date_created.desc()).all()

    return render_template('superadmin_dashboard.html',
                           branches=Branch.query.all(),
                           jobs_count=Job.query.count(),
                           approved_jobs=Job.query.filter_by(status='approved').all(),
                           manuals=Manual.query.all(),
                           manuals_count=Manual.query.count(),
                           logs_count=Log.query.count(),
                           admins=User.query.filter(User.role.in_(['admin', 'superadmin'])).all(),
                           all_testimonies=all_testimonies,
                           pending_testimonies=pending_testimonies,
                           all_announcements=all_announcements, # New variable added
                           member_stats=member_stats)

@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    if current_user.role == 'superadmin':
        return redirect(url_for('admin.superadmin_dashboard'))

    current_parish = Branch.query.get(current_user.branch_id)
    posts = Post.query.filter(
        (Post.branch_id == current_user.branch_id) | (Post.branch_id == None)
    ).all()

    return render_template(
        'admin_dashboard.html',
        posts=posts,
        parish=current_parish
    )

@admin_bp.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for('admin.admin_signup'))

        new_user = User(username=username, role='admin')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Admin account created! Please log in.", "success")
        return redirect(url_for('admin.login'))

    return render_template('admin_signup.html')

# --- MANAGEMENT ACTIONS ---

@admin_bp.route('/admin/events')
@login_required
def events():
    events_list = Event.query.filter_by(branch_id=current_user.branch_id).all()
    return render_template('admin/events.html', events=events_list)

@admin_bp.route('/admin/events/add', methods=['POST'])
@login_required
def add_event():
    new_event = Event(
        title=request.form.get('title'),
        date=request.form.get('event_date'),
        branch_id=current_user.branch_id
    )
    db.session.add(new_event)
    db.session.commit()
    flash('Event scheduled successfully!', 'success')
    return redirect(url_for('admin.events'))

@admin_bp.route('/admin/members')
@login_required
def members():
    query = request.args.get('search')
    members_query = Member.query.filter_by(branch_id=current_user.branch_id)
    if query:
        members_query = members_query.filter(Member.full_name.ilike(f'%{query}%'))
    return render_template('admin/members.html', members=members_query.all())

@admin_bp.route('/admin/members/add', methods=['POST'])
@login_required
def add_member():
    new_member = Member(
        full_name=request.form.get('full_name'),
        email=request.form.get('email'),
        phone=request.form.get('phone'),
        branch_id=current_user.branch_id
    )
    db.session.add(new_member)
    db.session.commit()
    flash('Member added successfully!', 'success')
    return redirect(url_for('admin.members'))

@admin_bp.route('/delete-branch/<int:id>', methods=['POST'])
@login_required
@superadmin_required
def delete_branch(id):
    branch = Branch.query.get_or_404(id)
    branch_name = branch.name
    db.session.delete(branch)
    log_action(current_user, "Delete Branch", f"Deleted branch: {branch_name}")
    db.session.commit()
    flash("Branch deleted.", "success")
    return redirect(url_for('admin.superadmin_dashboard'))

@admin_bp.route('/create-announcement', methods=['POST'])
@login_required
@superadmin_required
def create_announcement():
    title = request.form.get('title')
    content = request.form.get('content')
    video_url = request.form.get('video')

    if not title:
        flash("Title is required!", "danger")
        return redirect(url_for('admin.superadmin_dashboard'))

    # Handle Image Upload
    image = request.files.get('image')
    image_filename = None
    if image and image.filename != '':
        image_filename = secure_filename(image.filename)
        if not os.path.exists('static/uploads'):
            os.makedirs('static/uploads')
        image.save(os.path.join('static/uploads', image_filename))

    new_announcement = Announcement(
        title=title,
        content=content,
        image_filename=image_filename,
        video_url=video_url,
        admin_id=current_user.id
    )

    db.session.add(new_announcement)
    db.session.commit()
    flash("Announcement broadcasted!", "success")
    return redirect(url_for('admin.superadmin_dashboard'))

@admin_bp.route('/delete-announcement/<int:id>', methods=['POST'])
@login_required
@superadmin_required
def delete_announcement(id):
    announcement = Announcement.query.get_or_404(id)

    # Optional: Delete the image file from the server
    if announcement.image_filename:
        image_path = os.path.join('static/uploads', announcement.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(announcement)
    db.session.commit()
    flash("Announcement deleted successfully.", "success")
    return redirect(url_for('admin.superadmin_dashboard'))

@admin_bp.route('/approve-testimony/<int:id>', methods=['POST'])
@login_required
@superadmin_required
def approve_testimony(id):
    testimony = Testimony.query.get_or_404(id)
    testimony.is_approved = True
    db.session.commit()
    flash("Testimony approved and now visible to the public.", "success")
    return redirect(url_for('admin.superadmin_dashboard'))

@admin_bp.route('/delete-testimony/<int:id>', methods=['POST'])
@login_required
@superadmin_required
def delete_testimony(id):
    testimony = Testimony.query.get_or_404(id)
    db.session.delete(testimony)
    db.session.commit()
    flash("Testimony deleted successfully.", "success")
    return redirect(url_for('admin.superadmin_dashboard'))

@admin_bp.route('/admin/logout')
def logout():
    session.pop('is_verified', None)
    logout_user()
    return redirect(url_for('main.index'))

@admin_bp.route('/create-branch', methods=['GET', 'POST'])
@login_required
@superadmin_required
def create_branch():
    return "Branch Creation Page"

@admin_bp.route('/post-job', methods=['GET', 'POST'])
@login_required
@superadmin_required
def create_global_job():
    log_action(current_user, "Post Job", "Created a new global job listing")
    db.session.commit()
    return "Job Posting Page"

@admin_bp.route('/upload-manual', methods=['GET', 'POST'])
@login_required
@superadmin_required
def upload_manual():
    log_action(current_user, "Upload Manual", "Added a new resource to the library")
    db.session.commit()
    return "Manual uploaded!"

@admin_bp.route('/admin/upload-stream', methods=['POST'])
@login_required
def upload_stream():
    title = request.form.get('title')
    url = request.form.get('url')
    new_stream = LiveStream(title=title, url=url)
    db.session.add(new_stream)
    db.session.commit()
    flash('Live stream updated successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/superadmin/logs', methods=['GET'])
@login_required
@superadmin_required
def view_logs():
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    return render_template('view_logs.html', logs=logs)

@admin_bp.route('/admin/logs/clear', methods=['POST'])
@login_required
@superadmin_required
def clear_logs():
    try:
        db.session.query(Log).delete()
        log_action(current_user, "System Cleanup", "Cleared all audit logs")
        db.session.commit()
        flash("Audit logs cleared successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error clearing logs: {e}", "danger")
    return redirect(url_for('admin.view_logs'))

@admin_bp.route('/delete-job/<int:id>', methods=['POST'])
@login_required
@superadmin_required
def global_delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted successfully.", "success")
    return redirect(url_for('admin.superadmin_dashboard'))

@admin_bp.route('/edit-manual/<int:id>', methods=['GET', 'POST'])
@login_required
@superadmin_required
def edit_manual(id):
    return "Edit manual page"

@admin_bp.route('/delete-manual/<int:id>', methods=['POST'])
@login_required
@superadmin_required
def delete_manual(id):
    manual = Manual.query.get_or_404(id)
    db.session.delete(manual)
    db.session.commit()
    flash("Manual deleted.", "success")
    return redirect(url_for('admin.superadmin_dashboard'))

@admin_bp.route('/')
def admin_home():
    if current_user.is_authenticated:
        if current_user.role == 'superadmin':
            return redirect(url_for('admin.superadmin_dashboard'))
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('admin.login'))

# =========================================================
# ROUTE SYSTEM ENDPOINTS
# =========================================================

@admin_bp.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

@admin_bp.route('/verify-admin', methods=['POST'])
def verify_admin():
    data = request.json
    key = data.get("server_key")
    if key == current_app.config["SERVER_VERIFICATION_KEY"]:
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 401

@admin_bp.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing credentials"}), 400

    user = Admin.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # Return a structured user profile to Flutter
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "branch_id": user.branch_id
            }
        }), 200

    return jsonify({"status": "error", "message": "Invalid username or password"}), 401

@admin_bp.route('/superadmin/post-job', methods=['GET', 'POST'])
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
        flash("Global job posted successfully!", "success")
        return redirect(url_for('main.super_admin_dashboard'))
    return render_template('post_job.html')

@admin_bp.route('/admin/post-job', methods=['GET', 'POST'])
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
        return redirect(url_for('main.admin'))
    return render_template('post_local_job.html')

# =========================================================
# MOBILE API: GET ALL AVAILABLE JOBS
# =========================================================
@admin_bp.route('/api/jobs', methods=['GET'])
def api_get_jobs():
    # Fetch global jobs
    global_jobs = Job.query.filter_by(is_global=True).all()

    # Optional parameter passed from the Flutter app to fetch local branch jobs
    branch_id = request.args.get('branch_id')
    local_jobs = []
    if branch_id:
        local_jobs = Job.query.filter_by(is_global=False, branch_id=branch_id).all()

    return jsonify({
        "global_jobs": [{
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "description": j.description
        } for j in global_jobs],
        "local_jobs": [{
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "description": j.description
        } for j in local_jobs]
    }), 200

@admin_bp.route('/api/job/approve/<int:id>', methods=['POST'])
@login_required
@role_required('superadmin')
def approve_job(id):
    job = Job.query.get_or_404(id)
    job.is_approved = True
    db.session.commit()
    flash("Job approved successfully", "success")
    return redirect(url_for('main.super_admin_dashboard'))

@admin_bp.route('/job/delete/<int:id>', methods=['POST'])
@login_required
def delete_job(id):
    if not hasattr(current_user, 'role') or current_user.role != 'superadmin':
        flash("Unauthorized action!", "danger")
        return redirect(url_for('main.index'))

    job = Job.query.get_or_404(id)
    try:
        db.session.delete(job)
        db.session.commit()
        flash(f"Job '{job.title}' deleted successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Error deleting job.", "danger")
    return redirect(url_for('main.super_admin_dashboard'))

@admin_bp.route('/job/edit/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('main.super_admin_dashboard'))
    return render_template("edit_job.html", job=job)

@admin_bp.route('/contact', methods=['GET', 'POST'])
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
            body=f"\nNew Message from RCCG YAYA Portal\n\nName: {name}\nEmail: {email}\nType: {subject_type}\n\nConfidential:\n{'YES' if confidential else 'NO'}\n\nMessage:\n{message_body}\n"
        )
        try:
            mail.send(msg)
            flash(f"Thank you {name}, your message has been received successfully.", "success")
        except Exception as e:
            print(f"Error: {e}")
            flash("Message could not be sent.", "danger")
        return redirect(url_for('contact'))
    return render_template('contact.html')

# =========================================================
# MOBILE API: UPDATE AN EXISTING STREAM
# =========================================================
@admin_bp.route('/api/stream/update/<int:id>', methods=['POST'])
def api_update_stream(id):
    data = request.get_json() or {}
    title_data = data.get('title')
    url_data = data.get('url')

    if not title_data or not url_data:
        return jsonify({"status": "error", "message": "Title and URL are required"}), 400

    stream = LiveStream.query.get_or_404(id)
    stream.title = title_data
    stream.url = url_data
    db.session.commit()

    return jsonify({"status": "success", "message": "Live stream updated successfully!"}), 200

@admin_bp.route('/superadmin/upload-stream', methods=['GET', 'POST'])
@login_required
def global_upload_stream():
    if current_user.role != 'superadmin':
        abort(403)

    if request.method == 'POST':
        title = request.form.get('title')
        url = request.form.get('url')

        if not title or not url:
            flash("Title and URL are required!", "danger")
            return redirect(url_for('main.super_admin_dashboard'))

        stream = LiveStream(title=title, url=url)
        db.session.add(stream)
        db.session.commit()
        flash("Live stream updated successfully!", "success")
        return redirect(url_for('main.super_admin_dashboard'))
    return render_template("admin/upload_stream.html")

