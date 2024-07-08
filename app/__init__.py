# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.sucilzhqzugjcucykwmo:rT12dIOsWoqV2wln@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

    db.init_app(app)
    jwt.init_app(app)

    from app.auth import auth
    from app.routes import route_bp

    app.register_blueprint(auth)
    app.register_blueprint(route_bp)

    return app
