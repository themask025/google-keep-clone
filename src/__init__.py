from flask import Flask
import os
from src.model import db
from src.blueprints import auth, notes


def create_app(test_config=None):
    # app configuration
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    )
    
    if(test_config is not None):
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # db initialization
    db.init_app(app)
    
    # blueprint registration
    app.register_blueprint(auth.bp)
    app.register_blueprint(notes.bp)
    
    app.add_url_rule('/notes/', endpoint='index')
    
    return app