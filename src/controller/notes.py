from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for


bp = Blueprint('notes', __name__, url_prefix='/notes')

@bp.route('/', methods=('GET',))
def index():
    return render_template("notes/index.html")