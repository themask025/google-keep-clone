from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from src.model.database import get_db

bp = Blueprint('notes', __name__, url_prefix='/notes')

@bp.route('/', methods=('GET',))
def index():
    if session.get('user_id') is not None:
        db = get_db()
        user_id = session.get('user_id')
        notes_rows = db.execute('SELECT * FROM notes WHERE creator_id = ?', (user_id,)).fetchall()
        
        output = ""
        if notes_rows is not []:
            for row in notes_rows:
                for value in row:
                    output += str(value)
            flash(output)
    
    return render_template("notes/index.html")
    

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        creator_id = session['user_id']
        title = request.form.get('title')
        content = request.form.get('content')
        error = None
        
        if title is None:
            error = 'A title is required'
        elif content is None:
            error = 'Content is required'
        
        if error is None:
            db = get_db()
            db.execute(
                'INSERT INTO notes(creator_id, title, content) VALUES (?, ?, ?)',
                (creator_id, title, content)
                )
            db.commit()

            return redirect(url_for('index'))
    
    return render_template('notes/create.html')
    