# -*- coding: utf-8 -*-
# @Author: TD21forever
# @Date:   2019-07-12 21:12:20
# @Last Modified by:   TD21forever
# @Last Modified time: 2019-07-12 23:44:04
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from app import views