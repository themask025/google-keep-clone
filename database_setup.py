from src.model import db
from src.model.user import User
from src import create_app

app = create_app()

with app.app_context():
    db.create_all()
    
# if __name__ == '__main__':
#     app.run()