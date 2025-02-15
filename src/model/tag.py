from src.model.database import get_db


def insert_tag_into_database(creator_id, tag_name):
    db = get_db()
    db.execute(
        'INSERT INTO tags(creator_id, name) VALUES (?, ?)', (creator_id, tag_name,))
    db.commit()

def fetch_all_tags_by_creator_id(creator_id):
    db = get_db()
    all_tags = db.execute('SELECT * FROM tags WHERE creator_id=?', (creator_id,)).fetchall()
    return all_tags

def fetch_tag_by_name(tag_name):
    db = get_db()
    tag_row = db.execute(
    'SELECT * FROM tags WHERE name=?', (tag_name,)).fetchone()
    return tag_row

def update_tag_name_in_database_by_tag_id(new_tag_name, tag_id):
    db = get_db()
    db.execute('UPDATE tags SET name = ? WHERE id=?', (new_tag_name, tag_id))
    db.commit()
    
def delete_tag_by_id(tag_id):
    db = get_db()
    db.execute('DELETE FROM tags WHERE id=?', (tag_id,))
    db.commit()
    

def validate_new_tag_name(creator_id, tag_name):
    all_tags = fetch_all_tags_by_creator_id(creator_id)
    all_tags_names = [tag['name'] for tag in all_tags]
    
    if tag_name is None or tag_name == "":
        return 'The name of the tag cannot be empty.'
    
    if tag_name in all_tags_names:
        return 'The tag already exists.'
    
    return None