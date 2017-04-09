from flask import Flask

from os import urandom

def create_app():
    app = Flask(__name__)
    app.secret_key = urandom(24)
    
    #from utils import init_utils, init_errors
    from core import core

    #init_utils(app)
    #init_errors(app)
    app.register_blueprint(core)

    return app