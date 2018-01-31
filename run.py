# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from app.api import api
from app.web import web
from app.admin import admin
app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(web, url_prefix='')
app.register_blueprint(admin, url_prefix='/admin')
app.secret_key = 'akjdfkajdkfakdjfjahdfkasdfjahsdjfasjkfjads'
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)
