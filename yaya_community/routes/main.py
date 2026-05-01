import os
from datetime import datetime
from flask import Blueprint, session, redirect, url_for, render_template, request, flash, current_app
from werkzeug.utils import secure_filename
# ADDED 'Manual' to the imports below
from models import db, Branch, Post, Job, Event, Testimony, Application, Manual

main = Blueprint('main', __name__)

# --- GLOBAL DATA ---
@main.app_context_processor
def inject_branches():
    return dict(branches=Branch.query.all())

# --- BRANCH SELECTOR ---
@main.route('/set_branch/<int:branch_id>')
def set_branch(branch_id):
    if branch_id == 0:
        session.pop('selected_branch_id', None)
        session.pop('branch_name', None)
        flash("Switched to National View")
    else:
        branch = Branch.query.get_or_404(branch_id)
        session['selected_branch_id'] = branch.id
        session['branch_name'] = branch.name
        flash(f"Switched to {branch.name}")
    
    return redirect(request.referrer or url_for('main.index'))

# --- HOME / NEWS FEED ---
@main.route('/')
def index():
    active_branch_id = session.get('selected_branch_id')
    
    # Combined Query: Fetch National posts AND Branch-specific posts in one list
    if active_branch_id:
        posts = Post.query.filter(
            (Post.is_global == True) | (Post.branch_id == active_branch_id)
        ).order_by(Post.id.desc()).all()
    else:
        posts = Post.query.filter_by(is_global=True).order_by(Post.id.desc()).all()

    return render_template('index.html', posts=posts)

# --- JOB BOARD ---
@main.route('/jobs')
def jobs():
    active_branch_id = session.get('selected_branch_id')
    
    if active_branch_id:
        jobs = Job.query.filter(
            (Job.is_global == True) | (Job.branch_id == active_branch_id)
        ).order_by(Job.id.desc()).all()
    else:
        jobs = Job.query.filter_by(is_global=True).order_by(Job.id.desc()).all()
    
    return render_template('jobs.html', jobs=jobs)

# --- JOB APPLICATION UPLOAD ---
@main.route('/apply/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    if 'resume' not in request.files:
        flash('No file selected.')
        return redirect(request.referrer)
    
    file = request.files['resume']
    name = request.form.get('full_name')
    email = request.form.get('email')

    if file and file.filename.lower().endswith('.pdf'):
        original_name = secure_filename(file.filename)
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{original_name}"
        
        # FIXED: Use a default if UPLOAD_FOLDER isn't in config
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads/resumes')
        os.makedirs(upload_folder, exist_ok=True)
        file.save(os.path.join(upload_folder, filename))

        new_app = Application(
            job_id=job_id, 
            user_name=name, 
            user_email=email, 
            resume_filename=filename
        )
        db.session.add(new_app)
        db.session.commit()
        
        flash('Application submitted successfully!')
    else:
        flash('Please upload a valid PDF resume.')
    
    return redirect(url_for('main.jobs'))

# --- ADMIN DASHBOARD ---
@main.route('/admin')
def admin():
    all_branches = Branch.query.all()
    all_apps = Application.query.order_by(Application.id.desc()).all()
    all_posts = Post.query.order_by(Post.id.desc()).all()
    # Added manuals to admin view so you can see what is uploaded
    all_manuals = Manual.query.all()
    return render_template('admin.html', 
                           branches=all_branches, 
                           applications=all_apps, 
                           posts=all_posts, 
                           manuals=all_manuals)

# --- MANUALS (FIXED TO BE DYNAMIC) ---
@main.route('/manuals')
def manuals():
    # Fetching manuals from database instead of just returning template
    all_manuals = Manual.query.order_by(Manual.id.desc()).all()
    return render_template('manuals.html', manuals=all_manuals)

@main.route('/admin/upload-manual', methods=['GET', 'POST'])
def upload_manual():
    if request.method == 'POST':
        file = request.files.get('manual_file')
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')

        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'manuals')
            os.makedirs(upload_path, exist_ok=True)
            
            file.save(os.path.join(upload_path, filename))

            new_manual = Manual(title=title, description=description, filename=filename, category=category)
            db.session.add(new_manual)
            db.session.commit()
            flash('Manual uploaded successfully!')
            return redirect(url_for('main.admin'))
            
        flash('Invalid file format. Please upload a PDF.')
    return render_template('upload_manual.html')

# --- OTHER ROUTES (STABLE) ---
@main.route('/create_branch', methods=['GET', 'POST'])
def create_branch():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        if not name or not location:
            flash("Name and location are required!")
            return redirect(url_for('main.create_branch'))

        new_branch = Branch(name=name, location=location, stream_url=request.form.get('stream_url'))
        db.session.add(new_branch)
        db.session.commit()
        flash(f"Branch '{name}' created!")
        return redirect(url_for('main.admin'))
    return render_template('create_branch.html')

@main.route('/delete_branch/<int:id>')
def delete_branch(id):
    branch = Branch.query.get_or_404(id)
    db.session.delete(branch)
    db.session.commit()
    flash(f"Branch '{branch.name}' removed.")
    return redirect(url_for('main.admin'))

@main.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        is_global = request.form.get('is_global') == '1'
        branch_id = session.get('selected_branch_id')

        if not is_global and not branch_id:
            flash("Please select a branch before posting local news.")
            return redirect(url_for('main.admin'))

        new_post = Post(
            title=request.form.get('title'),
            content=request.form.get('content'),
            is_global=is_global,
            branch_id=branch_id if not is_global else None
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Announcement published!")
        return redirect(url_for('main.index'))
    return render_template('create_post.html')

@main.route('/events')
def events():
    selected_branch_id = session.get('selected_branch_id')
    if selected_branch_id:
        events = Event.query.filter(
            (Event.is_global == True) | (Event.branch_id == selected_branch_id)
        ).order_by(Event.event_date.asc()).all()
    else:
        events = Event.query.filter_by(is_global=True).order_by(Event.event_date.asc()).all()
    return render_template('events.html', events=events)

@main.route('/testimonies')
def testimonies():
    all_testimonies = Testimony.query.order_by(Testimony.id.desc()).all()
    return render_template('testimonies.html', testimonies=all_testimonies)

@main.route('/submit_testimony', methods=['POST'])
def submit_testimony():
    new_testimony = Testimony(
        user_name=request.form.get('full_name') or "Anonymous", 
        title=request.form.get('title'), 
        content=request.form.get('content')
    )
    db.session.add(new_testimony)
    db.session.commit()
    flash('Thank you for sharing!')
    return redirect(url_for('main.testimonies'))

@main.app_context_processor
def inject_branches():
    # This fetches all branches from the database automatically for every page
    from models import Branch
    return dict(branches=Branch.query.order_by(Branch.name.asc()).all())

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/offering')
def offering():
    # This renders the new offering.html page you created
    return render_template('offering.html')