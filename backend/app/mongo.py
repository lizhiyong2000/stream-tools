from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo

db = MongoEngine()

mongo = PyMongo()

login_manager = LoginManager()