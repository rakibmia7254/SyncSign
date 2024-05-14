from main import app
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from db import SQLDB
from uuid import uuid4
from time import time
from hashlib import sha256

db = SQLDB()

def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()

@app.route('/')
def index():
    if session.get('user'):
        return "Hello {} <a href='/logout'>Logout</a>".format(session.get('user'))
    else:
        return redirect(url_for('login', app_id="379b045bf18e4b1588cb8188de166538"))

@app.route('/signin/<app_id>', methods=['GET', 'POST'])
def login(app_id):
    app_data = db.get_app(app_id)
    # checking if user is already logged in
    if session.get('user') and session.get('user_id'):
        code = uuid4().hex
        db.add_code({"code": code,
                           "app_id": app_id,
                           "user_id": session.get('user_id'),
                           "email": session.get('user'), 
                           "expires": time() + 300})
        return redirect(app_data['redirect_uri']+'?code='+code)
    
    if not app_data:
        return jsonify({'error': 'invalid app_id'}), 400
    
    # checking if user is submitting login form
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.get_user(email)
        if user and user['password'] == hash_password(password):
            session['user'] = user['email']
            session['user_id'] = user['_id']
            code = uuid4().hex
            db.add_code({"code": code,
                           "app_id": app_id,
                           "user_id": user['_id'],
                           "email": email, 
                           "expires": time() + 300})
            
            return redirect(f"{app_data['redirect_uri']}?code={code}")
        else:
            flash('Invalid email or password')
    return render_template('login.html',app=app_data)


@app.route('/signup/<app_id>', methods=['GET', 'POST'])
def signup(app_id):
    app_data = db.get_app(app_id)

    if session.get('user'):
        code = uuid4().hex
        db.add_code({"code": code,
                        "app_id": app_id,
                        "user_id": session.get('user_id'),
                        "email": session.get('user'), 
                        "expires": time() + 300})
        return redirect(app_data['redirect_uri']+'?code='+code)
    
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        user = db.get_user(email)

        if user:
            flash('User already exists')
            return redirect(url_for('signup', app_id=app_id))
    
        db.set_user(email, password)
        user = db.get_user(email)
        session['user'] = email
        code = uuid4().hex
        db.add_code({"code": code,
                       "app_id": app_id,
                       "user_id": user['_id'],
                       "email": email,
                       "expires": time() + 300})
        return redirect(app_data['site'])
    
    return render_template('signup.html',app=app_data)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login', app_id="379b045bf18e4b1588cb8188de166538"))