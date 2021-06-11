import sqlite3

import click
from flask import g, current_app
from flask.cli import with_appcontext


def get_database():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_database(e=None):
    database = g.pop('db', None)

    if database is not None:
        database.close()


def init_database():
    database = get_database()

    with current_app.open_resource('schema.sql') as f:
        database.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_database_command():
    init_database()
    click.echo('Initialized database')


def init_app(app):
    app.teardown_appcontext(close_database)
    app.cli.add_command(init_database_command)
