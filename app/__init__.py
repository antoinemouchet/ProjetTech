from flask import Flask, request, redirect
from flask_cors import CORS
from jinja2 import Template, Environment, PackageLoader, select_autoescape

app = Flask(__name__)
app.secret_key = b'super secret omg'
CORS(app)

static_url_path = "/static"
app_url = "http://127.0.0.1:5000/"