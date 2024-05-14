from flask import Flask
from flask_wtf import CSRFProtect
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "your_secret_key"
csrf = CSRFProtect(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from . import routes