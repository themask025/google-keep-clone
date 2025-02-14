from flask import Flask, redirect, url_for
import os
from src.model import database
from src.controller import auth, notes, tags


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'db.sqlite'),
    )
    
    if(test_config is not None):
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    database.init_app(app)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(notes.bp)
    app.register_blueprint(tags.bp)
    
    app.add_url_rule('/notes/', endpoint='index')
    
    @app.route('/', methods=('GET',))
    def main():
        return redirect(url_for('index'))
    
    return app