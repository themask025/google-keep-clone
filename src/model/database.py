import sqlite3
from flask import Flask
from datetime import datetime


import click
from flask import current_app, g


def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON;')

    return g.db


def close_db(e=None) -> None:
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()

    with current_app.open_resource('create_tables.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command() -> None:
    init_db()
    click.echo('Initialized the database')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def read_all_results_from_database(stmt: str, params: tuple) -> list[sqlite3.Row] | None:
    db = get_db()
    return db.execute(stmt, params).fetchall()


def read_single_result_from_database(stmt: str, params: tuple) -> sqlite3.Row | None:
    db = get_db()
    return db.execute(stmt, params).fetchone()


def write_to_database(stmt: str, params: tuple) -> None:
    db = get_db()
    db.execute(stmt, params)
    db.commit()


def write_to_database_and_get_id(stmt: str, params: tuple) -> None:
    db = get_db()
    cursor = db.execute(stmt, params)
    db.commit()
    return cursor.lastrowid
