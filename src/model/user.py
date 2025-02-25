from src.model.database import (read_single_result_from_database,
                                write_to_database_and_get_id)


def insert_user_into_database(username: str, password_hash: str) -> int:
    stmt = 'INSERT INTO users (username, password_hash) VALUES (?, ?)'
    params = (username, password_hash,)
    user_id = write_to_database_and_get_id(stmt, params)
    return user_id


def fetch_user_by_username(username: str):
    stmt = 'SELECT * FROM users WHERE username = ?'
    params = (username,)
    return read_single_result_from_database(stmt, params)
