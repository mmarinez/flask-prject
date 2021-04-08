import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.database import get_database

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_database()
    posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            'FROM post p JOIN user u ON p.author_id = u.id'
            ' ORDER BY created ESC'
            ).fetchall()

    return render_template('blog/index.html', posts=posts)
