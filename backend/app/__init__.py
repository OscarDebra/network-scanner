from flask import Flask
from flask_cors import CORS
from config import Config
from app.models import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    init_db()

    from app.routes import bp
    app.register_blueprint(bp)

    return app