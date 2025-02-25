from src.model.tag import fetch_tag_by_name

from src.model.database import (read_all_results_from_database,
                                write_to_database)


def insert_note_tag(note_id, tag_id):
    stmt = 'INSERT INTO notes_tags(note_id, tag_id) VALUES (?, ?)'
    params = (note_id, tag_id)
    write_to_database(stmt, params)


def insert_newly_selected_tags(currently_selected_tags_names, selected_tags, note_id):
    selected_tags_names = [tag['name'] for tag in selected_tags]

    for tag_name in currently_selected_tags_names:
        if tag_name not in selected_tags_names:
            tag_row = fetch_tag_by_name(tag_name)
            tag_id = tag_row['id']
            insert_note_tag(note_id, tag_id)


def fetch_selected_tags_by_note_id(note_id):
    stmt = 'SELECT t.* FROM notes_tags nt JOIN tags t ON tag_id = id WHERE note_id=?'
    params = (note_id,)
    return read_all_results_from_database(stmt, params)


def update_selected_tags_in_database(currently_selected_tags_names, selected_tags, note_id):
    # insert the newly selected tags that are not already in the database
    insert_newly_selected_tags(
        currently_selected_tags_names, selected_tags, note_id)

    # delete the tags from the database that are not selected anymore
    for tag in selected_tags:
        if tag['name'] not in currently_selected_tags_names:
            delete_note_tag_by_ids(note_id, tag_id=tag['id'])


def delete_note_tag_by_ids(note_id, tag_id):
    stmt = 'DELETE FROM notes_tags WHERE (note_id=? AND tag_id=?)'
    params = (note_id, tag_id)
    write_to_database(stmt, params)
