from src.model.database import (read_single_result_from_database,
                                read_all_results_from_database,
                                write_to_database)


def insert_tag_into_database(creator_id, tag_name):
    stmt = 'INSERT INTO tags(creator_id, name) VALUES (?, ?)'
    params = (creator_id, tag_name)
    write_to_database(stmt, params)


def fetch_all_tags_by_creator_id(creator_id):
    stmt = 'SELECT * FROM tags WHERE creator_id=?'
    params = (creator_id,)
    return read_all_results_from_database(stmt, params)


def fetch_tag_by_name(tag_name):
    stmt = 'SELECT * FROM tags WHERE name=?'
    params = (tag_name,)
    return read_single_result_from_database(stmt, params)


def update_tag_name_in_database_by_tag_id(new_tag_name, tag_id):
    stmt = 'UPDATE tags SET name = ? WHERE id=?'
    params = (new_tag_name, tag_id)
    write_to_database(stmt, params)


def delete_tag_by_id(tag_id):
    stmt = 'DELETE FROM tags WHERE id=?'
    params = (tag_id,)
    write_to_database(stmt, params)


def validate_new_tag_name(creator_id, tag_name):
    all_tags = fetch_all_tags_by_creator_id(creator_id)
    all_tags_names = [tag['name'] for tag in all_tags]

    if tag_name is None or tag_name == "":
        return 'The name of the tag cannot be empty.'

    if tag_name in all_tags_names:
        return 'The tag already exists.'

    return None
