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
   
