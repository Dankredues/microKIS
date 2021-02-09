

from flask import Flask, render_template, session, redirect, url_for, escape, request

import sqlite3
from datetime import datetime
import re,os
import websockets
import json,time
from rust_rcon import Command, websocket_connection

app = Flask(__name__)



import webapp.draeger_routes
import webapp.mainroutes


@app.route("/admin")
def admin():
    if 'username' in session:
      username = session['username']
      return render_template("/admin/base.html",username=username)
    return admin_login()

@app.route('/admin/login', methods = ['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
      session['username'] = request.form['username']
      return redirect(url_for('admin'))

    return render_template("/admin/login.html")

app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/admin/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('admin'))

