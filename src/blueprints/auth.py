import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from src.model import db
from src.model.user import User
# from sqlalchemy.exc import NoResultFound, MultipleResultsFound


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
            user = User(username=username, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('index'))

        flash(error)

    return render_template("auth/register.html")


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
    # user = User.query.filter_by(username=username).first()
    user = db.session.execute(db.select(User).filter_by(username=username)).first()
    return user is not None


@bp.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        error = None

        user = db.session.execute(db.select(User).filter_by(username=username)).first()
        
        error = user.User
        
        # password = 
        
        # if user is None or check_password_hash(user._asdict().get('password_hash'), password) == False:
        #     error = 'Incorrect username/password.'
            
        # if error is None:
        #     session.clear()
        #     session['user_id'] = user.id
        #     session['username'] = user.username
        #     return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))