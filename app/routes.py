from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user 
from app import db, bcrypt
from app.models import User

# Create a Blueprint for authentication routes.
auth_routes = Blueprint('auth', __name__)

# Route for the login page
@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Basic validation
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')
        
        # Find user in database
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            login_user(user)  # This creates the user session
            flash('Login successful!', 'success')

             # Redirect to next page if it exists, otherwise to dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template('login.html')
    
    # For GET requests, just show the form
    return render_template('login.html')

# Route for the registration page
@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html')
        
        # Create new user
        try:
            new_user = User(username=username)
            new_user.password = password  # This will hash the password
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            # It's good practice to log the actual error (e) here for debugging
    
    # For GET requests, just show the form
    return render_template('register.html')

# Route for logout
@auth_routes.route('/logout')
@login_required  # Only logged-in users can logout
def logout():
    logout_user()  # This destroys the user session
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

# Create a Blueprint for our main routes. This helps organize the app.
main_routes = Blueprint('main', __name__)

# Route for the homepage
@main_routes.route('/')
def index():
    return render_template('index.html')

# Route for the dashboard (will be protected later)
@main_routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Custom error handler for 401 errors...redundancy a function was created in __init__.py
# @main_routes.app_errorhandler(401)
# def unauthorized_error(error):
#     flash('Please log in to access this page.', 'error')
#     return redirect(url_for('auth.login'))


# Base function example
# @auth_routes.route('/register')
# def register():
#     return render_template('register.html')