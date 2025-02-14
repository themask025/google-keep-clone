from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from datetime import datetime

from src.model.database import get_db


bp = Blueprint('tags', __name__, url_prefix='/tags')


@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    db = get_db()
    
    tags = db.execute('SELECT * FROM tags').fetchall()
    
    if request.method == 'POST':
        error = None
        
        tag_names = [tag['name'] for tag in tags]
        
        if request.form.get('create_tag') is not None:
            # check if tag name is valid
            new_tag_name = request.form.get('new_tag_name')
            if new_tag_name is None or new_tag_name == "":
                error = 'The name of the tag cannot be empty.'
            
            #   check if it's unique
            if new_tag_name in tag_names:
                error = 'A tag with this name already exists.'
            
            # update in db
            if error == None:
                db.execute('INSERT INTO tags (name) VALUES (?)', (new_tag_name,))
                db.commit()
            else:
                flash(error)
        
        else:
            for i, tag in enumerate(tags):
                if request.form.get('update_tag_' + str(tag['id'])) is not None:

                    # check if name is empty
                    new_tag_name = request.form.get('tag_' + str(tag['id']))
                    if new_tag_name != tag['name']:
                        if new_tag_name is None:
                            error = 'The name of the tag cannot be empty.'
                        
                        #   check if it's unique
                        if new_tag_name in tag_names:
                            error = 'A tag with this name already exists.'
                        
                        # update in db
                        if error == None:
                            db.execute('UPDATE tags SET name = ? WHERE id=?', (new_tag_name, tag['id']))
                            db.commit()
                        else:
                            flash(error)

                elif request.form.get('delete_tag_' + str(tag['id'])) is not None:
                    # delete tag from database
                    db.execute('DELETE FROM tags WHERE id=?', (tag['id'],))
                    db.commit()
        
        tags = db.execute('SELECT * FROM tags').fetchall()
    
    return render_template('/tags/index.html', tags=tags)