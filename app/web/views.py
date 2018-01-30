# -*- coding: utf-8 -*-
import os
from flask import Flask, request, redirect, url_for,render_template,session,send_from_directory,jsonify,escape
from werkzeug.utils import secure_filename
import base64
import time
from flask import Blueprint
from app.web import web
from flask import jsonify
import json

@web.route('/')
def home():
    return render_template('/default.html',title="face+")
@web.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('web.home'))
    return render_template('/login.html',title="login")
@web.route('/login_with_face',methods=['GET','POST'])
def login_with_face():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('web.home'))
    return render_template('/login_with_face.html',title="login")
@web.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))
