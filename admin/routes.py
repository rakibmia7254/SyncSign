from . import admin_bp, db, render_template, request, redirect, url_for, flash, session
from .image_validation import allowed_file, validate_image, optimize_image
import os
from uuid import uuid4
from secrets import token_urlsafe

# image upload folder
UPLOAD_FOLDER = 'logos'

# Routes
@admin_bp.route('/', methods=['GET', 'POST'])
def index():
    if "admin" not in session:
        return redirect(url_for('admin.login'))
    data = db.get_apps()
    user = session.get('admin')
    return render_template('home.html', data=data, user=user)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin'):
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        user = db.get_admin(request.form['username'])
        if user and user['password'] == request.form['password']:
            session['admin'] = user['username']
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid email or password')
    return render_template('admin_login.html')

@admin_bp.route('/users')
def users():
    if "admin" not in session:
        return redirect(url_for('admin.login'))
    data = db.get_users()
    return render_template('users.html', data=data)

@admin_bp.route('/add', methods=['GET', 'POST'])
def add():
    if "admin" not in session:
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        app_name = request.form['app_name']
        redirect_uri = request.form['redirect_uri']
        app_logo = request.files['app_logo']
        app_id = str(uuid4())

        # validate url
        if not redirect_uri.startswith('http://') and not redirect_uri.startswith('https://'):
            flash('Invalid URL')
            return redirect(url_for('admin.add'))
        
        # Validate image
        if app_logo is not None and allowed_file(app_logo.filename) is False:
            flash('Invalid image')
            return redirect(url_for('admin.add'))
        
        is_valid, size = validate_image(app_logo)
        if is_valid is False:
            flash('Invalid image')
            return redirect(url_for('admin.add'))
        # Save the file
        filename = app_id + '.' + app_logo.filename.split('.')[::-1][0]
        file_path = os.path.join("admin",UPLOAD_FOLDER, filename)
        optimize_image(app_logo, file_path)
        app_data = {
            'id': app_id,
            'name': app_name,
            'redirect_uri': redirect_uri,
            'logo': f'{UPLOAD_FOLDER}/{filename}',
            'api_key': token_urlsafe(16),
            }
        # Add to database
        db.add_app(app_data)
        flash('App added successfully')
        return redirect(url_for('admin.index'))
    return render_template('add.html')

@admin_bp.route('/view/<app_id>', methods=['GET', 'POST'])
def view(app_id):
    if "admin" not in session:
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        app_name = request.form['app_name']
        redirect_uri = request.form['redirect_uri']
        print(app_id, app_name, redirect_uri)
        db.update_app(app_id, {'name': app_name, 'redirect_uri': redirect_uri})
        flash('App updated successfully')
        return redirect(url_for('admin.index'))
    app = db.get_app(app_id)
    if not app:
        return "App not found"
    return render_template('view.html', data=app)

@admin_bp.route('/settings', methods=['GET','POST'])
def settings():
    if "admin" not in session:
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_new_password']
        admin = db.get_admin(session.get('admin'))
        if admin and admin['password'] == password:
            if new_password == confirm_password:
                db.update_admin(admin['id'],username, new_password)
                session['admin'] = username
                flash('Password updated successfully')
                return redirect(url_for('admin.index'))
            else:
                flash('Passwords do not match')
                return redirect(url_for('admin.settings'))
        else:
            flash('Invalid password')
        return redirect(url_for('admin.settings'))
    
    return render_template('settings.html')

@admin_bp.route('/delete', methods=['POST'])
def delete():
    if "admin" not in session:
        return redirect(url_for('admin.login'))
    app_id = request.form['app_id']
    app_logo = request.form['logo']
    file_path = os.path.join("admin", app_logo)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.delete_app(app_id)
    flash('App deleted successfully')
    return redirect(url_for('admin.index'))

@admin_bp.route('/delete_user/<id>')
def delete_user(id):
    if "admin" not in session:
        return redirect(url_for('admin.login'))
    db.delete_user(id)
    flash('User deleted successfully')
    return redirect(url_for('admin.users'))

@admin_bp.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))