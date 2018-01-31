# -*- coding: utf-8 -*-
import os
from flask import Flask, request, redirect, url_for,render_template,session,send_from_directory,jsonify,escape
from werkzeug.utils import secure_filename
import base64
import time
from flask import Blueprint
from app.api import api
from flask import jsonify
import json
from config import APP_ID,API_KEY,SECRET_KEY
# 配置百度 faceAPI
from aip import AipFace
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

# api
#detect 人脸检测
@api.route('/face/detect',methods=['GET','POST'])
def api_face_detect():
    if request.method == 'POST':
        img_base64=request.form['img_base64']
        imgdata=base64.b64decode(img_base64)
        options = {}
        options["max_face_num"] = 20
        options["face_fields"] = "age,beauty,race"
        txt=client.detect(imgdata, options)
        return jsonify(txt)

#match 人脸对比
@api.route('/face/match',methods=['GET','POST'])
def api_face_match():
    if request.method == 'POST':
        img_a_base64=request.form['img_base64_a']
        img_b_base64=request.form['img_base64_b']
        imgdata_a=base64.b64decode(img_a_base64)
        imgdata_b=base64.b64decode(img_b_base64)
        images = [
            imgdata_a,
            imgdata_b
        ]
        options = {}
        options["ext_fields"] = "qualities"
        options["image_liveness"] = ",faceliveness"
        options["types"] = "7,13"
        txt=client.match(images, options)
        return jsonify(txt)
#addUser 注册用户人脸（添加到人脸库）
@api.route('/face/add_user',methods=['GET','POST'])
def api_face_add_user():
    if request.method == 'POST':
        img_base64=request.form['img_base64']
        image=base64.b64decode(img_base64)
        uid = request.form['uid']
        userInfo = request.form['user_info']
        groupId = "group1"
        options = {}
        options["action_type"] = "replace"
        txt=client.addUser(uid, userInfo, groupId, image, options)
        return jsonify(txt)
    return render_template('/api/face/add_user.html',title="api:add user")


#deleteUser 删除用户人脸（从人脸库中删除）
@api.route('/face/delete_user',methods=['GET','POST'])
def api_face_delete_user():
    if request.method == 'POST':
        uid=request.form['uid']
        txt=client.deleteUser(uid);
        return jsonify(txt)
    return render_template('/api/face/delete_user.html',title="api:delete user")


#identifyUser 识别是谁
@api.route('/face/identify_user',methods=['GET','POST'])
def api_face_identify_user():
    if request.method == 'POST':
        img_base64=request.form['img_base64']
        image=base64.b64decode(img_base64)
        groupId = "group1"
        txt=client.identifyUser(groupId, image);
        print(txt)
        try:
            if(txt['result'][0]['scores'][0]>80):
                session['username'] = txt['result'][0]['user_info']
        except:
            # save
            filename="static/upload/%s.jpg" % (int(time.time()))
            file=open(filename,'wb')
            file.write(image)
            file.close()
            return jsonify("{'err':'yes'}")
        return jsonify(txt)
    return render_template('/api/face/identify_user.html',title="api:identify user")
