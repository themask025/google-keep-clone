from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from src.model.database import get_db
from datetime import datetime


bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/', methods=('GET',))
def index():
    if session.get('user_id') is not None:
        db = get_db()
        user_id = session.get('user_id')
        notes_rows = db.execute(
            'SELECT * FROM notes WHERE creator_id = ?', (user_id,)).fetchall()

    else:
        notes_rows = []

    return render_template("notes/index.html", notes_rows=notes_rows, len=len)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    current_note = None

    if request.method == 'POST':
        creator_id = session['user_id']
        title = request.form.get('title')
        content = request.form.get('content')
        error = None

        if title is None:
            error = 'A title is required.'
        elif content is None:
            error = 'Content is required.'

        if error is None:
            db = get_db()
            cursor = db.execute(
                'INSERT INTO notes(creator_id, title, content) VALUES (?, ?, ?)',
                (creator_id, title, content)
            )
            db.commit()

            created_note_id = cursor.lastrowid

            return redirect(url_for('notes.edit', note_id=created_note_id))

        flash(error)

    return render_template('notes/view_note.html', current_note=current_note)


@bp.route('/edit/<note_id>', methods=('GET', 'POST'))
def edit(note_id):
    if note_id is None:
        return redirect(url_for('notes.index'))

    db = get_db()
    current_note_row = db.execute(
        'SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
    current_note = dict(current_note_row)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        timestamp = datetime.now().isoformat(sep=' ')

        error = None

        if title is None:
            error = 'A title is required.'
        elif content is None:
            error = 'Content is required.'

        if error is None:
            note_id = current_note['id']
            db.execute(
                f'UPDATE notes SET (title, content, updated_at) = (?, ?, ?) WHERE id={note_id}',
                (title, content, timestamp)
            )
            db.commit()

            flash('Note saved.')

            current_note['updated_at'] = timestamp
        else:
            flash(error)

        current_note['title'] = title
        current_note['content'] = content

    return render_template('/notes/view_note.html', current_note=current_note)


@bp.route('/delete/<note_id>', methods=('POST',))
def delete(note_id):
    if note_id is not None:
        db = get_db()
        db.execute('DELETE FROM notes WHERE id= ? ;', (note_id,))
        db.commit()
        return redirect(url_for('notes.index'))

    return redirect('notes.index')
