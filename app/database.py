import sqlite3
from flask import g
from . import app 
import os

DATABASE = 'database.db'

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(os.path.join(os.path.dirname(__file__), 'database', 'database.sql'), mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
def query_db(query, args=(), one=False, com=False):
    with app.app_context():
        db = get_db()
        cur = db.execute(query, args)
        rv = cur.fetchall()
        if com:
            db.commit()
        cur.close()
        return (rv[0] if rv else None) if one else rv
