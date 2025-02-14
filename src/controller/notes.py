from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from datetime import datetime

from src.model.database import get_db


bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/', methods=('GET',))
def index():
    if session.get('user_id') is not None:
        db = get_db()
        user_id = session.get('user_id')
        notes_rows = db.execute(
            'SELECT * FROM notes WHERE creator_id = ?', (user_id,)).fetchall()
        
        notes = [dict(note) for note in notes_rows]
        
        for note in notes:
            
            note_id = note['id']
            note_tags = db.execute('SELECT id, name FROM notes_tags JOIN tags ON tag_id = id WHERE note_id=?', (note_id,)).fetchall()
            note_tags_names = [tag['name'] for tag in note_tags]
            note_tags_names = ', '.join(note_tags_names)
            note['tags'] = note_tags_names
            
    else:
        notes_rows = []
        notes = []

    return render_template("notes/index.html", notes_rows=notes_rows, len=len, notes=notes)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    current_note = None

    db = get_db()

    # fetched from tags table
    all_tags = db.execute('SELECT * FROM tags').fetchall()

    # fetched from notes_tags table
    selected_tags = []

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

            # adding newly created tags to tags table in the database
            new_tags = request.form['new_tags']
            if new_tags != "":
                new_tags = new_tags.split(',')
                for tag_name in new_tags:
                    db.execute(
                        'INSERT INTO tags(name) VALUES (?)', (tag_name,))
                    db.commit()

            currently_selected_tags_names = request.form.getlist('tag')
            note_id = created_note_id

            # insert the newly selected tags that are not already in the database
            for tag_name in currently_selected_tags_names:
                tag_row = db.execute(
                    'SELECT * FROM tags WHERE name=?', (tag_name,)).fetchone()
                tag_id = tag_row['id']
                db.execute(
                    'INSERT INTO notes_tags(note_id, tag_id) VALUES (?, ?)', (note_id, tag_id))
                db.commit()

            return redirect(url_for('notes.edit', note_id=created_note_id))

        flash(error)

    return render_template('notes/view_note.html', current_note=current_note, all_tags=all_tags, selected_tags=selected_tags, enumerate=enumerate)


@bp.route('/edit/<note_id>', methods=('GET', 'POST'))
def edit(note_id):
    if note_id is None:
        return redirect(url_for('notes.index'))

    db = get_db()
    current_note_row = db.execute(
        'SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
    current_note = dict(current_note_row)

    # fetched from tags table
    all_tags = db.execute('SELECT * FROM tags').fetchall()

    # fetched from notes_tags table
    selected_tags = db.execute(
        'SELECT id, name FROM notes_tags JOIN tags ON tag_id = id WHERE note_id=?', (note_id,)).fetchall()

    if request.method == 'POST':

        if request.form.get('submit_tag_button') is not None:
            submitted_data_type = 'new_tag'
        elif request.form.get('submit_note_button') is not None:
            submitted_data_type = 'note'

        title = request.form['title']
        content = request.form['content']

        error = None

        if submitted_data_type == 'new_tag':
            tag_name = request.form.get('new_tag_name')
            if tag_name is None or tag_name == "":
                error = 'The name of the tag cannot be empty.'
            
            all_tags_names = [tag['name'] for tag in all_tags]
            if tag_name in all_tags_names:
                error = 'The tag already exists.'
            
            if error is None:        
                # add the new tag to the tags table
                cursor = db.execute(
                    'INSERT INTO tags(name) VALUES (?)', (tag_name,))
                db.commit()

                # refresh tag data for the rendering of the page
                all_tags = db.execute('SELECT * FROM tags').fetchall()
            else:
                flash(error)

        if submitted_data_type == 'note':
            
            if title is None:
                error = 'A title is required.'
            elif content is None:
                error = 'Content is required.'

            if error is None:
                # updating notes database table
                timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
                note_id = current_note['id']
                db.execute(
                    f'UPDATE notes SET (title, content, updated_at) = (?, ?, ?) WHERE id={note_id}',
                    (title, content, timestamp)
                )
                db.commit()

                currently_selected_tags_names = request.form.getlist('tag')
                selected_tags_names = [tag['name'] for tag in selected_tags]

                # insert the newly selected tags that are not already in the database
                for tag_name in currently_selected_tags_names:
                    if tag_name not in selected_tags_names:
                        tag_row = db.execute(
                            'SELECT * FROM tags WHERE name=?', (tag_name,)).fetchone()
                        tag_id = tag_row['id']
                        db.execute(
                            'INSERT INTO notes_tags(note_id, tag_id) VALUES (?, ?)', (note_id, tag_id))
                        db.commit()

                # delete the tags from the database that are not selected anymore
                for tag in selected_tags:
                    if tag['name'] not in currently_selected_tags_names:
                        db.execute(
                            'DELETE FROM notes_tags WHERE (note_id=? AND tag_id=?)', (note_id, tag['id']))
                        db.commit()

                flash('Note saved.')
                
                current_note['updated_at'] = timestamp
                selected_tags = db.execute(
                    'SELECT id, name FROM notes_tags JOIN tags ON tag_id = id WHERE note_id=?', (note_id,)).fetchall()
            else:
                flash(error)

        current_note['title'] = title
        current_note['content'] = content

    return render_template('/notes/view_note.html', current_note=current_note, all_tags=all_tags, selected_tags=selected_tags, enumerate=enumerate)


@bp.route('/delete/<note_id>', methods=('POST',))
def delete(note_id):
    if note_id is not None:
        db = get_db()
        db.execute('DELETE FROM notes WHERE id= ? ;', (note_id,))
        db.commit()
        return redirect(url_for('notes.index'))

    return redirect('notes.index')
