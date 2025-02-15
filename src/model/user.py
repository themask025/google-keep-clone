from src.model.database import get_db


def insert_user_into_database(username: str, password_hash: str) -> None:
    db = get_db()
    db.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash,))
    db.commit()
    
def fetch_user_by_username(username: str) -> None:
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    return user