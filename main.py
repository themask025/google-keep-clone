import src
from src.model.database import init_db

app = src.create_app()

with app.app_context():
    init_db()

app.run()