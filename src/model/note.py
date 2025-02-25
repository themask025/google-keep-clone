from src.model.database import (get_db,
                                read_single_result_from_database,
                                read_all_results_from_database,
                                write_to_database,
                                write_to_database_and_get_id)


def insert_note_into_database(creator_id, title, content):
    stmt = 'INSERT INTO notes(creator_id, title, content) VALUES (?, ?, ?)'
    params = (creator_id, title, content)
    note_id = write_to_database_and_get_id(stmt, params)
    return note_id


def fetch_note_by_id(note_id):
    stmt = 'SELECT * FROM notes WHERE id=?;'
    params = (note_id,)
    return read_single_result_from_database(stmt, params)


def fetch_all_notes_by_user_id(user_id):
    stmt = 'SELECT * FROM notes WHERE creator_id=?;'
    params = (user_id,)
    return read_all_results_from_database(stmt, params)


def fetch_user_notes_by_tags(user_id, filter_tags):
    stmt = ('SELECT DISTINCT n.* '
            'FROM notes n '
            'JOIN notes_tags nt ON n.id = nt.note_id '
            'JOIN tags t ON nt.tag_id = t.id '
            'WHERE n.creator_id = ? ')
    stmt_suffix = ""

    if filter_tags is not None and filter_tags != []:
        filter_stmts = [
            't.name = ?' for tag_name in filter_tags if tag_name is not None and tag_name != ""]
        filter_stmts = ' OR '.join(filter_stmts)
        stmt_suffix = 'AND (' + filter_stmts + ')'
    else:
        filter_tags = []

    stmt += stmt_suffix
    params = (user_id, *filter_tags)
    return read_all_results_from_database(stmt, params)


def update_note_in_database(note_id, title, content, updated_at):
    stmt = f'UPDATE notes SET (title, content, updated_at) = (?, ?, ?) WHERE id={note_id}'
    params = (title, content, updated_at)
    write_to_database(stmt, params)


def update_due_date_in_database(note_id, new_due_date):
    stmt = 'UPDATE notes SET due_date = ? WHERE id = ?'
    params = (new_due_date, note_id)
    write_to_database(stmt, params)


def remove_due_date_from_database(note_id):
    stmt = 'UPDATE notes SET due_date = NULL where id = ?'
    params = (note_id,)
    write_to_database(stmt, params)


def delete_note_by_id(note_id):
    stmt = 'DELETE FROM notes WHERE id=?;'
    params = (note_id,)
    write_to_database(stmt, params)
