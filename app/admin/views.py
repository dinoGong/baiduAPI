# -*- coding: utf-8 -*-
import os
from flask import Flask, request, redirect, url_for,render_template,session,send_from_directory,jsonify,escape
from werkzeug.utils import secure_filename
import base64
import time
from flask import Blueprint
from app.admin import admin
from flask import jsonify
import json

@admin.route('/')
def home():
    if "username" in session:
        logged=True
    else:
        logged=False
    return render_template('/admin/default.html',title="face+",logged=logged)
@admin.route('/add_user')
def add_user():
    if "username" in session:
        logged=True
    else:
        logged=False
    return render_template('/admin/add_user.html',title="api:add user")
@admin.route('/delete_user')
def delete_user():
    if "username" in session:
        logged=True
    else:
        logged=False
    return render_template('/admin/delete_user.html',title="api:delete user")
