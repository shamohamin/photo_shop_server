from flask import Flask
from flask_cors import CORS
from .config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

from .users.routes import users
from .filters.routes import filters

app.register_blueprint(users)
app.register_blueprint(filters)