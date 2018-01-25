# -*- coding: utf-8 -*-
import os
from flask import Flask, request, redirect, url_for,render_template,session,send_from_directory,jsonify,escape
from werkzeug.utils import secure_filename
import base64
# 配置百度 faceAPI
from aip import AipFace
""" 你的 APPID AK SK """
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
# 配置结束

UPLOAD_FOLDER = os.path.dirname(os.path.abspath('static'))+'/static/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'akjdfkajdkfakdjfjahdfkasdfjahsdjfasjkfjads'



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file',filename=filename))
            img_url=url_for('static',filename=filename)
            #return jsonify(img=img_url)
            return img_url
    return render_template('upload.html',title="uploadServer")
@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('default.html',title="x",logged=True,username=session['username'])
    return render_template('default.html',title="x",logged=False)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template('login.html',title="Login")

@app.route('/login_with_face',methods=['GET','POST'])
def login_with_face():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template('login_with_face.html',title="Login")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404



# api
#detect 人脸检测
@app.route('/api/face/detect',methods=['GET','POST'])
def api_face_detect():
    if request.method == 'POST':
        img_base64=request.form['img_base64']
        imgdata=base64.b64decode(img_base64)
        options = {}
        options["max_face_num"] = 20
        options["face_fields"] = "age,beauty,race"
        txt=client.detect(imgdata, options)
        return jsonify(txt)
    return render_template('/api/face/detect.html',title="api:detect")
#match 人脸对比
@app.route('/api/face/match',methods=['GET','POST'])
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
    return render_template('/api/face/match.html',title="api:match")
#addUser 注册用户人脸（添加到人脸库）
@app.route('/api/face/add_user',methods=['GET','POST'])
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

#identifyUser 识别是谁
@app.route('/api/face/identify_user',methods=['GET','POST'])
def api_face_identify_user():
    if request.method == 'POST':
        img_base64=request.form['img_base64']
        image=base64.b64decode(img_base64)
        groupId = "group1"
        txt=client.identifyUser(groupId, image);
        return jsonify(txt)
    return render_template('/api/face/identify_user.html',title="api:identify user")
  
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)
