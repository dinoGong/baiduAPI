# -*- coding: utf-8 -*-
from flask import Flask
from app.api import api
app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)
