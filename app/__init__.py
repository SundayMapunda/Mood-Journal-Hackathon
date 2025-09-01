from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
# from flask_limiter import Limiter  # NEW
# from flask_limiter.util import get_remote_address  # NEW
# from app.utils import hf_limiter 
import os
from dotenv import load_dotenv  # Add this import

# Load environment variables from .env file
load_dotenv()  # Add this line

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
# limiter = Limiter(key_func=get_remote_address)  # NEW

def create_app():
    # Create the Flask application instance
    app = Flask(__name__)
    
    # Load configuration from .env file
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True <- return logs of what is sent to mysql

    # NEW: Configure rate limiting storage
    # ratelimit_storage_url = os.getenv('RATELIMIT_STORAGE_URL')
    # if ratelimit_storage_url:
    #     app.config['RATELIMIT_STORAGE_URL'] = ratelimit_storage_url
    # else:
    #     # Fallback to memory with warning
    #     app.config['RATELIMIT_STORAGE_URL'] = 'memory://'

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    # limiter.init_app(app)  # NEW
    # hf_limiter.init_app(app)  # NEW: Initialize the Hugging Face limiter

    # Configure Flask-Login to redirect to login page for unauthorized access
    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('auth.login'))

    # Set the login view
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'error'

    # Import and register Blueprints
    from app.routes import main_routes, auth_routes  # <-- Add this import
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)

    # Import models here to ensure they are registered with SQLAlchemy
    from app import models  # <-- Add this line

    return app