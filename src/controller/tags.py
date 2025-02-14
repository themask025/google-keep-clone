from flask import Blueprint, flash, render_template, request

from src.model.tag import insert_tag_into_database, fetch_all_tags, update_tag_name_in_database_by_tag_id, delete_tag_by_id, validate_new_tag_name


bp = Blueprint('tags', __name__, url_prefix='/tags')


@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    tags = fetch_all_tags()
    
    if request.method == 'POST':
        error = None
        
        if request.form.get('create_tag') is not None:
            new_tag_name = request.form.get('new_tag_name')
            error = validate_new_tag_name(new_tag_name)
            if error is None:
                insert_tag_into_database(new_tag_name)
            else:
                flash(error)
        
        else:
            for i, tag in enumerate(tags):
                if request.form.get('update_tag_' + str(tag['id'])) is not None:
                    new_tag_name = request.form.get('tag_' + str(tag['id']))
                    if new_tag_name != tag['name']:
                        error = validate_new_tag_name(new_tag_name)
                        if error is None:
                            update_tag_name_in_database_by_tag_id(new_tag_name, tag_id=tag['id'])
                        else:
                            flash(error)

                elif request.form.get('delete_tag_' + str(tag['id'])) is not None:
                    delete_tag_by_id(tag['id'])
        
        tags = fetch_all_tags()
    
    return render_template('/tags/index.html', tags=tags)