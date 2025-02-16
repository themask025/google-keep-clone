import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from src.model.user import insert_user_into_database, fetch_user_by_username


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')
        error = validate_register_input(
            username, password, password_confirmation)

        if error is None:
            password_hash = generate_password_hash(password)
            user_id = insert_user_into_database(username, password_hash)
            session.clear()
            session['user_id'] = user_id
            session['username'] = username
            return redirect(url_for('index'))

        flash(error)

    return render_template("auth/register.html")



@bp.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        user = fetch_user_by_username(username)
        if user is None or check_password_hash(user['password_hash'], password) == False:
            error = 'Incorrect username/password.'
            
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('auth/login.html')


@bp.route('/logout', methods=('POST',))
def logout():
    session.clear()
    return redirect(url_for('index'))


def validate_register_input(username: str | None, password: str | None, password_confirmation: str | None) -> str | None:
    if not username:
        return 'Username is required.'
    if not password:
        return 'Password is required.'
    if len(username) < 4:
        return 'Username must be at least 4 characters long.'
    if len(password) < 8:
        return 'Password must be at least 8 characters long.'
    if password != password_confirmation:
        return 'Passwords do not match.'
    if check_user_exists(username) == True:
        return 'User with this username already exists.'

    return None


def check_user_exists(username: str) -> str | None:
    user = fetch_user_by_username(username)
    return user is not None