import os
from datetime import datetime
from flask import (
    Blueprint, session, redirect, url_for,
    render_template, request, flash,
    current_app, jsonify, abort
)
from werkzeug.utils import secure_filename
from flask_login import (
    login_user, logout_user,
    login_required, current_user
)

from decorators import role_required

# FIX 1: Imported FileAllowed to prevent NameError inside edit_manual
from flask_wtf.file import FileAllowed  
from forms import ManualUploadForm  

# MODELS
from models import (
    db,
    Branch,
    Post,
    Job,
    Event,
    Testimony,
    Application,
    Manual,
    Admin,
    ActivityLog,
    Stream,
    BankDetail,
    Announcement
)

main = Blueprint('main', __name__)

# =========================================================
# GLOBAL DATA
# =========================================================
@main.app_context_processor
def inject_branches():
    """Provide branches globally."""
    if current_user.is_authenticated:
        if hasattr(current_user, 'role') and current_user.role == 'superadmin':
            branches = Branch.query.order_by(Branch.name.asc()).all()
        else:
            branches = Branch.query.filter_by(
                id=current_user.branch_id
            ).all()
    else:
        branches = Branch.query.order_by(
            Branch.name.asc()
        ).all()
    return dict(branches=branches)


# =========================================================
# HOME PAGE
# =========================================================
@main.route('/')
def index():
    active_branch_id = session.get('selected_branch_id')
    all_branches = Branch.query.order_by(Branch.name.asc()).all()

    # MAIN LIVE STREAM (GLOBAL)
    main_stream = Stream.query.order_by(Stream.created_at.desc()).first()

    # BRANCH STREAM (OPTIONAL)
    branch_stream = None
    if active_branch_id:
        branch_stream = Branch.query.get(active_branch_id)

    # POSTS
    if active_branch_id:
        posts = Post.query.filter(
            (Post.is_global == True) |
            (Post.branch_id == active_branch_id)
        ).order_by(Post.id.desc()).all()
    else:
        posts = Post.query.filter_by(is_global=True).order_by(Post.id.desc()).all()

    # ANNOUNCEMENTS
    announcements = Announcement.query.order_by(Announcement.id.desc()).all()

    return render_template(
        'index.html',
        main_stream=main_stream,
        branch_stream=branch_stream,
        posts=posts,
        branches=all_branches,
        announcements=announcements
    )


@main.route('/gatekeeper', methods=['GET', 'POST'])
def gatekeeper():
    if request.method == 'POST':
        key = request.form.get('server_key')
        if key == current_app.config.get("SERVER_VERIFICATION_KEY"):
            session['verified'] = True
            return redirect(url_for('main.login'))
        flash("Invalid verification key", "danger")
        return redirect(url_for('main.gatekeeper'))
    return render_template("gatekeeper.html")


# =========================================================
# AUTHENTICATION
# =========================================================
@main.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get('verified'):
        return redirect(url_for('main.gatekeeper'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Admin.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            session.permanent = True
            if user.role == 'superadmin':
                return redirect(url_for('main.super_admin_dashboard'))
            return redirect(url_for('main.admin'))
        flash("Invalid credentials", "danger")
    return render_template('login.html')


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        branch_name = request.form.get('branch_name', '').strip().title()
        location = request.form.get('location')

        if not username or not password or not branch_name:
            flash("All fields are required", "danger")
            return redirect(url_for('main.signup'))

        existing_user = Admin.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists", "danger")
            return redirect(url_for('main.signup'))

        branch = Branch.query.filter_by(name=branch_name).first()
        if not branch:
            branch = Branch(name=branch_name, location=location)
            db.session.add(branch)
            db.session.commit()

        user = Admin(username=username, branch_id=branch.id, role='admin')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for('main.login'))
    return render_template("signup.html")


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out 👋", "info")
    return redirect(url_for('main.index'))


# =========================================================
# ADMIN DASHBOARDS
# =========================================================
@main.route('/admin')
@login_required
def admin():
    news = Post.query.filter_by(branch_id=current_user.branch_id).all()
    testimonies = Testimony.query.filter_by(branch_id=current_user.branch_id).all()
    recent_jobs = Job.query.filter_by(branch_id=current_user.branch_id).all()

    if current_user.role == 'superadmin':
        branches_list = Branch.query.all()
    else:
        branches_list = Branch.query.filter_by(id=current_user.branch_id).all()

    return render_template(
        'admin.html',
        news=news,
        testimonies=testimonies,
        applications=[],
        recent_jobs=recent_jobs,
        branches=branches_list
    )


@main.route('/super-admin-dashboard')
@login_required
@role_required('superadmin')
def super_admin_dashboard():
    return render_template(
        'super_admin_dashboard.html',
        admins=Admin.query.order_by(Admin.id.desc()).all(),
        branches=Branch.query.order_by(Branch.name.asc()).all(),
        jobs_count=Job.query.count(),
        manuals=Manual.query.all(),
        manuals_count=Manual.query.count(),
        logs_count=ActivityLog.query.count(),
        announcements=Announcement.query.order_by(Announcement.id.desc()).all()
    )


# =========================================================
# JOBS MANAGEMENT
# =========================================================
@main.route('/jobs')
def jobs():
    local_jobs = Job.query.filter(Job.branch_id.isnot(None)).all()
    global_jobs = Job.query.filter(Job.branch_id.is_(None)).all()
    return render_template(
        'jobs.html',
        local_jobs=local_jobs,
        global_jobs=global_jobs,
        jobs=Job.query.all()
    )


@main.route('/admin/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    if request.method == 'POST':
        is_global = current_user.role == 'superadmin'
        new_job = Job(
            title=request.form.get('title'),
            company=request.form.get('company'),
            description=request.form.get('description'),
            branch_id=None if is_global else current_user.branch_id,
            is_global=is_global,
            is_approved=True
        )
        db.session.add(new_job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('main.jobs'))
    return render_template('admin/post_job.html')


@main.route('/job/<int:id>')
def job_details(id):
    job = Job.query.get_or_404(id)
    return render_template('job_detail_page.html', job=job)


@main.route('/job/delete/<int:id>', methods=['POST'])
@login_required
@role_required('superadmin')
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash("Job listing removed.", "success")
    return redirect(url_for('main.jobs'))


@main.route('/apply-job/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    file = request.files.get('cv_file')

    if file and file.filename != '':
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.root_path, 'static/uploads')
        
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
            
        file.save(os.path.join(upload_path, filename))
        flash(f"Application submitted successfully for job #{job_id}!", "success")
    else:
        flash("Please upload a CV to apply.", "danger")
    return redirect(url_for('main.jobs'))


# =========================================================
# MANUALS
# =========================================================
@main.route('/manuals')
def manuals():
    all_manuals = Manual.query.order_by(Manual.id.desc()).all()
    return render_template('manuals.html', manuals=all_manuals)


@main.route('/upload-manual', methods=['GET', 'POST'])
@login_required
@role_required('superadmin')
def upload_manual():
    form = ManualUploadForm()

    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)

        upload_path = os.path.join(
            current_app.config.get('UPLOAD_FOLDER', 'static/uploads'), 
            'manuals'
        )
        os.makedirs(upload_path, exist_ok=True)
        file.save(os.path.join(upload_path, filename))

        manual = Manual(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            icon_class=form.icon_class.data,
            filename=filename
        )
        db.session.add(manual)
        
        log = ActivityLog(
            admin_name=current_user.username,
            action=f"Uploaded manual via WTForm: {form.title.data}"
        )
        db.session.add(log)
        db.session.commit()

        flash('Manual uploaded successfully!', 'success')
        return redirect(url_for('main.manuals'))

    return render_template('upload_manual.html', form=form)


@main.route('/manual/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('superadmin')
def edit_manual(id):
    manual = Manual.query.get_or_404(id)
    form = ManualUploadForm(obj=manual)

    form.file.validators = [FileAllowed(['pdf'], 'PDFs only!')]

    if form.validate_on_submit():
        manual.title = form.title.data
        manual.description = form.description.data
        manual.category = form.category.data
        manual.icon_class = form.icon_class.data

        file = form.file.data
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'static/uploads'), 'manuals')
            file.save(os.path.join(upload_path, filename))
            manual.filename = filename

        log = ActivityLog(
            admin_name=current_user.username,
            action=f"Edited manual details for: {manual.title}"
        )

        db.session.add(log)
        db.session.commit()
        
        flash('Manual updated successfully!', 'success')
        return redirect(url_for('main.super_admin_dashboard'))

    return render_template('edit_manual.html', form=form, manual=manual)


@main.route('/manual/delete/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required('superadmin')
def delete_manual(id):
    manual = Manual.query.get_or_404(id)
    title = manual.title

    if manual.filename:
        file_path = os.path.join(
            current_app.config.get('UPLOAD_FOLDER', 'static/uploads'),
            'manuals',
            manual.filename
        )

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Error removing physical file {file_path}: {e}")

    db.session.delete(manual)
    
    log = ActivityLog(
        admin_name=current_user.username,
        action=f"Deleted manual: {title}"
    )
    db.session.add(log)
    db.session.commit()

    flash(f"Manual '{title}' was successfully deleted.", "success")
    return redirect(url_for('main.super_admin_dashboard'))


# =========================================================
# BRANCH SELECTION & ACTIONS
# =========================================================
@main.route('/super-admin/create-branch', methods=['GET', 'POST'])
@login_required
@role_required('superadmin')
def create_branch():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')

        if not name or not location:
            flash("All fields are required!", "danger")
            return redirect(url_for('main.create_branch'))

        new_branch = Branch(name=name, location=location)
        db.session.add(new_branch)

        log = ActivityLog(
            admin_name=current_user.username,
            action=f"Created new branch: {name}"
        )
        db.session.add(log)
        db.session.commit()

        flash(f"Branch '{name}' created successfully!", "success")
        return redirect(url_for('main.super_admin_dashboard'))
    return render_template('create_branch.html')


@main.route('/branch/delete/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required('superadmin')
def delete_branch(id):
    branch = Branch.query.get_or_404(id)
    db.session.delete(branch)

    log = ActivityLog(
        admin_name=current_user.username,
        action=f"Deleted branch: {branch.name}"
    )
    db.session.add(log)
    db.session.commit()

    flash(f"Branch '{branch.name}' has been removed.", "success")
    return redirect(url_for('main.super_admin_dashboard'))


@main.route('/select-branch', methods=['POST'])
def select_branch():
    branch_id = request.form.get('branch_id')
    if branch_id:
        session['selected_branch_id'] = int(branch_id)
        branch = db.session.get(Branch, int(branch_id))
        if branch:
            flash(f"Now viewing updates for {branch.name}!", "success")
    else:
        session.pop('selected_branch_id', None)
        flash("Viewing all global updates.", "info")
    return redirect(url_for('main.index'))


@main.route('/select_branch_by_name', methods=['POST'])
def select_branch_by_name():
    branch_name = request.form.get('branch_name')
    parish = Branch.query.filter_by(name=branch_name).first()
    if parish:
        return render_template('parish_detail.html', parish=parish)
        
    flash("Parish not found. Please check the name and try again.", "warning")
    return redirect(url_for('main.index'))


@main.route('/admin/add-branch', methods=['POST'])
@login_required
def add_branch():
    name = request.form.get('name')
    youtube_link = request.form.get('youtube_link')
    calendar_updates = request.form.get('calendar_updates')

    if not name or not youtube_link:
        flash("Title and URL are required!", "danger")
        return redirect(url_for('main.admin'))

    new_branch = Branch(
        name=name,
        youtube_link=youtube_link,
        calendar_updates=calendar_updates
    )
    db.session.add(new_branch)
    db.session.commit()
    flash("Parish added successfully!", "success")
    return redirect(url_for('main.admin'))


# =========================================================
# STREAMS
# =========================================================
@main.route('/upload-stream', methods=['POST'])
@login_required
def upload_stream():
    branch_id = request.form.get('parish_id')
    url = request.form.get('stream_url') or request.form.get('url')

    if not url:
        flash("YouTube URL is required!", "danger")
        return redirect(url_for('main.admin'))

    if "watch?v=" in url:
        url = url.replace("watch?v=", "embed/")
    elif "youtu.be/" in url:
        url = url.replace("youtu.be/", "www.youtube.com/embed/")

    url = url.split('&')[0]

    if current_user.role == 'superadmin':
        if branch_id:
            branch = db.session.get(Branch, int(branch_id))
            if branch:
                branch.youtube_link = url
                db.session.commit()
                flash(f"Stream for {branch.name} updated.", "success")
        else:
            new_stream = Stream(
                title="Main Live Broadcast",
                url=url,
                is_live=True,
                created_at=datetime.utcnow()
            )
            db.session.add(new_stream)
            db.session.commit()
            flash("Front page live stream updated!", "success")
    else:
        branch = db.session.get(Branch, current_user.branch_id)
        if branch:
            branch.youtube_link = url
            db.session.commit()
            flash("Your parish stream has been updated.", "success")

    return redirect(url_for('main.admin'))


# =========================================================
# TESTIMONIES
# =========================================================
@main.route('/testimonies')
def testimonies():
    all_testimonies = Testimony.query.order_by(Testimony.id.desc()).all()
    return render_template('testimonies.html', testimonies=all_testimonies)


@main.route('/share-story', methods=['GET', 'POST'])
def share_story():
    if request.method == 'POST':
        testimony = Testimony(
            name=request.form.get('name'),
            title=request.form.get('title'),
            content=request.form.get('content'),
            branch_id=session.get('selected_branch_id'),
            is_approved=False
        )
        db.session.add(testimony)
        db.session.commit()
        flash('Testimony submitted for approval!', 'success')
        return redirect(url_for('main.testimonies'))
    return render_template('share_story.html')


# =========================================================
# EVENTS
# =========================================================
@main.route('/events')
def events():
    selected_branch_id = session.get('selected_branch_id')
    if selected_branch_id:
        events_list = Event.query.filter(
            (Event.is_global == True) | (Event.branch_id == selected_branch_id)
        ).order_by(Event.event_date.asc()).all()
    else:
        events_list = Event.query.filter_by(is_global=True).order_by(Event.event_date.asc()).all()
    return render_template('events.html', events=events_list)

# --- VIEW ALL EVENTS UPCOMING ---
@main.route('/events')
def view_events():
    # Queries all events ordered by nearest chronological date
    all_events = Event.query.order_by(Event.event_date.asc()).all()
    return render_template('events.html', events=all_events)


# --- ADMINISTRATIVE CREATION ENDPOINT ---
@main.route('/admin/create-event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location') or 'Main Auditorium'
        is_global = True if request.form.get('is_global') == 'true' else False
        
        # Convert HTML5 datetime-local string to native Python datetime object
        date_str = request.form.get('event_date')
        parsed_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')

        new_event = Event(
            title=title,
            description=description,
            event_date=parsed_date,
            location=location,
            is_global=is_global
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        flash('Event published successfully!', 'success')
        return redirect(url_for('main.view_events'))

    return render_template('create_event.html')


@main.route('/post-event', methods=['GET', 'POST'])
@login_required
def post_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description') or "No description provided."
        event_date = request.form.get('event_date')
        location = request.form.get('location')

        if title and event_date:
            try:
                parsed_date = datetime.fromisoformat(event_date)
            except ValueError:
                flash("Invalid date format configuration.", "danger")
                return redirect(url_for('main.post_event'))

            new_event = Event(
                title=title,
                description=description,
                event_date=parsed_date,
                location=location,
                branch_id=current_user.branch_id,
                is_global=False
            )
            db.session.add(new_event)
            db.session.commit()
            flash("Event posted!", "success")
            return redirect(url_for('main.admin'))
            
    return render_template('admin/post_event.html')


# =========================================================
# ANNOUNCEMENTS & FINANCE & BASE INFORMATION
# =========================================================
@main.route('/create-announcement', methods=['GET', 'POST'])
@login_required
def create_announcement():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        # FIX 2: Dynamic root path definitions to avoid execution environment crashes
        base_upload_path = os.path.join(current_app.root_path, 'static/uploads')
        os.makedirs(base_upload_path, exist_ok=True)

        # IMAGE
        image_file = request.files.get('image')
        image_filename = None
        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(base_upload_path, image_filename))

        # VIDEO FILE
        video_upload = request.files.get('video_file')
        video_filename = None
        if video_upload and video_upload.filename:
            video_filename = secure_filename(video_upload.filename)
            video_upload.save(os.path.join(base_upload_path, video_filename))

        video_link = request.form.get('video')

        announcement = Announcement(
            title=title,
            content=content,
            image=image_filename,
            video_file=video_filename,
            video=video_link
        )
        db.session.add(announcement)
        db.session.commit()

        flash("Announcement created successfully", "success")
        return redirect(url_for('main.index'))
    return render_template('create_announcement.html')


@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        flash("Password reset instructions have been sent if the account exists.", "info")
        return redirect(url_for('main.login'))
    return render_template('forgot_password.html')


@main.route('/super-admin/logs')
@login_required
@role_required('superadmin')
def view_logs():
    all_logs = ActivityLog.query.order_by(ActivityLog.id.desc()).limit(100).all()
    return render_template('view_logs.html', logs=all_logs)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/offering')
@main.route('/pay')
def offering():
    tithe_bank = BankDetail.query.filter_by(category='Tithe').first()
    project_bank = BankDetail.query.filter_by(category='Project').first()
    return render_template('offering.html', tithe=tithe_bank, project=project_bank)


@main.route('/update-bank', methods=['POST'])
@login_required
def update_bank():
    if current_user.role != 'superadmin':
        return "Unauthorized", 403

    category = request.form.get('category')
    bank_name = request.form.get('bank_name')
    acc_num = request.form.get('account_number')

    bank = BankDetail.query.filter_by(category=category).first()
    if bank:
        bank.bank_name = bank_name
        bank.account_number = acc_num
    else:
        new_bank = BankDetail(
            category=category,
            bank_name=bank_name,
            account_name="RCCG YAYA",
            account_number=acc_num
        )
        db.session.add(new_bank)

    db.session.commit()
    flash(f"{category} details updated successfully!", "success")
    return redirect(url_for('main.offering'))


@main.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


@main.route('/contact/submit', methods=['POST'])
def contact_submit():
    name = request.form.get('name')
    subject = request.form.get('subject')
    flash(f"Thank you {name}, your {subject} has been received successfully.", "success")
    return redirect(url_for('main.contact'))