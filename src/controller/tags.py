from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from datetime import datetime

from src.model.database import get_db


bp = Blueprint('tags', __name__, url_prefix='/tags')


@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    pass