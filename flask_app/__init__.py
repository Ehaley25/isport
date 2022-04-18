from flask import Flask

app = Flask(__name__)

app.secret_key = "im creating a fake key"