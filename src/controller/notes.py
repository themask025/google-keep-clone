from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from datetime import datetime

from src.model.note import (fetch_all_notes_by_user_id,
                            fetch_note_by_id,
                            fetch_user_notes_by_tags,
                            insert_note_into_database,
                            update_note_in_database,
                            update_due_date_in_database,
                            remove_due_date_from_database,
                            delete_note_by_id)
from src.model.tag import (insert_tag_into_database,
                           fetch_all_tags_by_creator_id,
                           validate_new_tag_name)
from src.model.note_tag import (insert_newly_selected_tags,
                                fetch_selected_tags_by_note_id,
                                update_selected_tags_in_database)


bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/', methods=('GET', 'POST'))
def index():
    if session.get('user_id') is not None:
        user_id = session.get('user_id')

        if request.method == 'POST':
            if request.form.get('apply_filter') is not None:
                selected_filter_tags = request.form.getlist(
                    'filter_tag')  # can be None
                session['filter_tags'] = selected_filter_tags

            elif request.form.get('clear_filter') is not None:
                session['filter_tags'] = None

            elif request.form.get('search_button') is not None:
                search_expression = request.form.get('search_expression')
                session['search_expression'] = search_expression

            elif request.form.get('clear_search') is not None:
                session['search_expression'] = None

        selected_filter_tags = session.get('filter_tags')
        if selected_filter_tags is not None:
            notes_rows = fetch_user_notes_by_tags(
                user_id, filter_tags=selected_filter_tags)
        else:
            selected_filter_tags = []
            notes_rows = fetch_all_notes_by_user_id(user_id)

        notes = [dict(note) for note in notes_rows]

        for note in notes:
            note_id = note['id']
            note_tags = fetch_selected_tags_by_note_id(note_id)
            note_tags_names = [tag['name'] for tag in note_tags]
            note_tags_names = ', '.join(note_tags_names)
            note['tags'] = note_tags_names

        search_expression = session.get('search_expression')
        if search_expression is not None:
            notes = filter_notes_by_search_expression(notes, search_expression)

        tags = fetch_all_tags_by_creator_id(creator_id=user_id)

    else:
        notes_rows = []
        notes = []
        selected_filter_tags = []
        search_expression = None
        tags = []

    return render_template("notes/index.html",
                           notes_rows=notes_rows,
                           len=len,
                           notes=notes,
                           tags=tags,
                           selected_filter_tags=selected_filter_tags,
                           search_expression=search_expression)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    user_id = session.get('user_id')
    current_note = None
    all_tags = fetch_all_tags_by_creator_id(creator_id=user_id)
    selected_tags = []

    if request.method == 'POST':
        creator_id = session['user_id']
        title = request.form.get('title')
        content = request.form.get('content')        
        currently_selected_tags_names = request.form.getlist('tag')
        new_tag_name = request.form.get('new_tag_name')

        if request.form.get('submit_tag_button') is not None:
            tag_name = new_tag_name
            error = validate_new_tag_name(
                creator_id=user_id, tag_name=tag_name)
            if error is None:
                insert_tag_into_database(creator_id=user_id, tag_name=tag_name)

            flash(error)
            all_tags = fetch_all_tags_by_creator_id(creator_id=user_id)

        elif request.form.get('submit_note_button') is not None:
            error = validate_note_title_content(title, content)

            if error is None:
                note_id = insert_note_into_database(creator_id, title, content)
                currently_selected_tags_names = request.form.getlist('tag')
                insert_newly_selected_tags(
                    currently_selected_tags_names, selected_tags, note_id)

                return redirect(url_for('notes.edit', note_id=note_id))

            flash(error)

        current_note = dict(title=title, content=content,
                            new_tag_name=new_tag_name)
        selected_tags = [tag for tag in all_tags if tag['name'] in currently_selected_tags_names]

    return render_template('notes/view_note.html',
                           current_note=current_note,
                           all_tags=all_tags,
                           selected_tags=selected_tags,
                           enumerate=enumerate)


@bp.route('/edit/<note_id>', methods=('GET', 'POST'))
def edit(note_id):
    user_id = session.get('user_id')

    if note_id is None:
        return redirect(url_for('notes.index'))

    current_note_row = fetch_note_by_id(note_id)
    current_note = dict(current_note_row)

    all_tags = fetch_all_tags_by_creator_id(creator_id=user_id)
    selected_tags = fetch_selected_tags_by_note_id(note_id=note_id)
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        new_tag_name = request.form.get('new_tag_name')
        currently_selected_tags_names = request.form.getlist('tag')
        note_submitted = False

        if request.form.get('submit_tag_button') is not None:
            tag_name = new_tag_name
            error = validate_new_tag_name(
                creator_id=user_id, tag_name=tag_name)
            if error is None:
                insert_tag_into_database(
                    creator_id=user_id, tag_name=tag_name)
            else:
                flash(error)
            all_tags = fetch_all_tags_by_creator_id(creator_id=user_id)

        elif request.form.get('submit_note_button') is not None:
            error = validate_note_title_content(title, content)

            if error is None:
                timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
                note_id = current_note['id']
                update_note_in_database(
                    note_id=note_id, title=title, content=content, updated_at=timestamp)

                update_selected_tags_in_database(
                    currently_selected_tags_names, selected_tags, note_id)
                flash('Note saved.')    
                current_note['updated_at'] = timestamp
                
                note_submitted = True
            else:
                flash(error)

        elif request.form.get('due_date_submit_button') is not None:
            due_date = request.form.get('due_date')

            error = None
            due_date_formatted = due_date

            if due_date is not None:
                try:
                    due_date_formatted = datetime.fromisoformat(due_date)
                except ValueError:
                    error = 'The entered due date format is invalid.'

            if error is None:
                due_date_formatted = due_date_formatted.isoformat(
                    sep=' ', timespec='seconds')
                update_due_date_in_database(
                    note_id=note_id, new_due_date=due_date_formatted)

            else:
                flash(error)

            current_note['due_date'] = due_date_formatted

        elif request.form.get('due_date_remove_button') is not None:
            remove_due_date_from_database(note_id)
            current_note['due_date'] = None

        if note_submitted == True:
            selected_tags = fetch_selected_tags_by_note_id(note_id)
        else:
            selected_tags = [tag for tag in all_tags if tag['name'] in currently_selected_tags_names]

        current_note['title'] = title
        current_note['content'] = content

    return render_template('/notes/view_note.html',
                           current_note=current_note,
                           all_tags=all_tags,
                           selected_tags=selected_tags,
                           enumerate=enumerate)


@bp.route('/delete/<note_id>', methods=('POST',))
def delete(note_id):
    if note_id is not None:
        delete_note_by_id(note_id)

    return redirect(url_for('notes.index'))


def filter_notes_by_search_expression(notes, search_expression):
    result = []

    for note in notes:
        if any((search_expression in note.get('title'),
                search_expression in note.get('content'),
                *(search_expression in tag_name for tag_name in note.get('tags').split(', ')))):
            result.append(note)

    return result


def validate_note_title_content(title, content):
    if title is None:
        return 'A title is required.'
    elif content is None:
        return 'Content is required.'
    return None
