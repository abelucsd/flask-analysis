import os
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/files/uploads'

db = SQLAlchemy()
DB_NAME = 'database.db'
app = Flask(__name__, instance_relative_config=True)

def create_app(test_config=None):
    # create and configure the app
    
    app.config['SECRET KEY'] = 'asdfasdqwer'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .api import api    
    from .analysis import analysis

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/')    
    app.register_blueprint(analysis, url_prefix='/')

    with app.app_context():
        db.create_all()    

    app.config['ALLOWED_EXTENSIONS'] = set(['xml', 'XML', 'text/xml'])
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )    

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app