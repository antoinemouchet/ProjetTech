from flask import Flask, request, redirect
from flask_cors import CORS
from jinja2 import Template, Environment, PackageLoader, select_autoescape
from flask_login import LoginManager
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.login_message = "You can not access this page. Please log in to access this page."
login_manager.session_protection = "strong"

app.secret_key = b'super secret omg'
CORS(app)
static_url_path = "/static"
app_url = "http://127.0.0.1:5000/"

from app import routes