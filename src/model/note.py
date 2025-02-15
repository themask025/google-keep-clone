from src.model.database import get_db


def insert_note_into_database(creator_id, title, content):
    db = get_db()
    cursor = db.execute(
        'INSERT INTO notes(creator_id, title, content) VALUES (?, ?, ?)',
        (creator_id, title, content)
    )
    db.commit()
    
    note_id = cursor.lastrowid
    return note_id

def fetch_note_by_id(note_id):
    db = get_db()
    current_note_row = db.execute(
        'SELECT * FROM notes WHERE id=?;', (note_id,)).fetchone()
    return current_note_row

def fetch_all_notes_by_user_id(user_id):
    db = get_db()
    notes = db.execute(
    'SELECT * FROM notes WHERE creator_id=?;', (user_id,)).fetchall()
    return notes

def fetch_user_notes_by_tags(user_id, filter_tags):
    db = get_db()
    
    stmt = ('SELECT DISTINCT n.* '
            'FROM notes n '
            'JOIN notes_tags nt ON n.id = nt.note_id '
            'JOIN tags t ON nt.tag_id = t.id '
            'WHERE n.creator_id = ? ')
    stmt_suffix = ""
    
    if filter_tags is not None and filter_tags != []:
        filter_stmts = [('t.name = ' + '?') for tag_name in filter_tags if tag_name is not None and tag_name != ""]
        filter_stmts = ' OR '.join(filter_stmts)
        stmt_suffix = 'AND (' + filter_stmts + ')'
    else:
        filter_tags = []
    
    stmt += stmt_suffix
    
    # return stmt
    
    notes_rows = db.execute(stmt, (user_id, *filter_tags))
    
    return notes_rows
    

def update_note_in_database(note_id, title, content, updated_at):
    db = get_db()
    db.execute(
    f'UPDATE notes SET (title, content, updated_at) = (?, ?, ?) WHERE id={note_id}',
    (title, content, updated_at)
    )
    db.commit()

def delete_note_by_id(note_id):
    db = get_db()
    db.execute('DELETE FROM notes WHERE id=?;', (note_id,))
    db.commit()
   
