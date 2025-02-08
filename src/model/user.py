from src.model import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(150))
    
    def __repr__(self) -> str:
        """Defines the instance representation for a User object."""
        return (
            '<User('
            f'username={self.username},'
            f'password_hash={self.password_hash}'
            ')>'
        )