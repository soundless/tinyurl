#!/usr/bin/env python
# -*- utf-8 -*-

# all the imports
import os
import sys
import sqlite3
import validators

from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# current directory
HERE = os.path.abspath(os.path.dirname(__file__))

sys.path.append(HERE + '/lib')
from short_url import ShortUrl

# Configuration
DATABASE = os.path.join(HERE, "tiny.db")
TABLE = 'urls'
_COL1 = 'url'
_COL2 = 'tiny'
DEBUG = True
SECRET_KEY = "rHOdfonwlytLycKkdP1Hb5pvy+DmNGav"
USERNAME = "admin"
PASSWORD = "admin"

# Create our application
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(app.config['DATABASE'])
    return db

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_urls():
    search = 'SELECT %s, %s FROM %s ORDER BY ID DESC' % (_COL1, _COL2, TABLE)
    cur = g.db.execute(search)
    entries = [dict(url=row[0], tiny=row[1]) for row in cur.fetchall()]
    return render_template('show_urls.html', entries=entries)

@app.route('/a', methods=['POST'])
def add_url():
    if not session.get('logged_in'):
        abort(401)

    url = request.form['url']
    # validate URL
    if not url:
        flash("URL cannot be empty")
        return redirect(url_for('show_urls'))
    if not validators.url(url):
        flash("URL is invalid, valid one starts with 'http://' or 'https://'")
        return redirect(url_for('show_urls'))

    # insert record
    insert = 'INSERT INTO urls (url) VALUES (?)'
    cur = g.db.cursor()
    cur.execute(insert, [url])
    g.db.commit()

    # get the last record id and encoded
    last_id = cur.lastrowid
    short_url = ShortUrl.encode(last_id)

    # update the record again with short_url
    update = 'UPDATE %s SET %s="%s" WHERE id=%s' \
                % (TABLE, _COL2, short_url, last_id)
    cur.execute(update)
    g.db.commit()
    cur.close()

    flash("Tiny URL was successfully created: " + request.host_url + 'o/' + short_url)
    return redirect(url_for('show_urls'))

@app.route('/o/<short_url>')
def redirect_url(short_url):
    app.logger.debug(short_url)
    s_id = ShortUrl.decode(short_url)
    search = 'SELECT %s, %s FROM %s WHERE ID = ?' % (_COL1, _COL2, TABLE)
    url = query_db(search, [s_id], one=True)
    app.logger.debug(url)
    if url is None:
        flash("Failed to locate URL for " + short_url)
        return redirect(url_for('show_urls'))
    else:
        return redirect(url[0], 307)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash("You were logged in successfully!")
            return redirect(url_for('show_urls'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out successfully!')
    return redirect(url_for('show_urls'))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)
