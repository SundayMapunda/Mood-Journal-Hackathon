from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user 
from app import db, bcrypt
from app.models import User, Entry, EmotionScore, Tag
from app.utils import analyze_sentiment  # Import the utility function
import json
from datetime import datetime

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
@main_routes.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        # Get form data
        content = request.form.get('content')
        tags_input = request.form.get('tags', '')
        
        if not content:
            flash('Journal content cannot be empty.', 'error')
            return render_template('dashboard.html')
        
        # Create new journal entry
        try:
            new_entry = Entry(content=content, author=current_user)
            
            # Process tags
            if tags_input:
                tag_names = [tag.strip().lower() for tag in tags_input.split(',')]
                for tag_name in tag_names:
                    if tag_name:  # Skip empty tags
                        # Get or create the tag
                        tag = Tag.query.filter_by(name=tag_name).first()
                        if not tag:
                            tag = Tag(name=tag_name)
                            db.session.add(tag)
                        new_entry.tags.append(tag)
            
            db.session.add(new_entry)
            db.session.flush()  # Flush to get the entry ID without committing
            
            # Analyze sentiment using Hugging Face API
            emotion_scores = analyze_sentiment(content)
            
            if emotion_scores:
                # Create emotion score record
                emotion_score = EmotionScore(
                    joy=emotion_scores.get('joy', 0.0),
                    sadness=emotion_scores.get('sadness', 0.0),
                    anger=emotion_scores.get('anger', 0.0),
                    fear=emotion_scores.get('fear', 0.0),
                    surprise=emotion_scores.get('surprise', 0.0),
                    entry_id=new_entry.id
                )
                db.session.add(emotion_score)
                flash('Journal entry saved and analyzed successfully!', 'success')
            else:
                # Create default emotion scores if analysis fails
                emotion_score = EmotionScore(entry_id=new_entry.id)
                db.session.add(emotion_score)
                flash('Journal entry saved, but sentiment analysis failed.', 'warning')
            
            db.session.commit()
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error saving journal entry: {e}")
            flash('An error occurred while saving your entry. Please try again.', 'error')
    
    # For GET requests, show the dashboard with recent entries
    recent_entries = Entry.query.filter_by(user_id=current_user.id)\
                              .order_by(Entry.date_created.desc())\
                              .limit(5).all()

    # Get data for the line chart - last 7 days of emotion scores
    import datetime
    seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    
    chart_data = Entry.query\
        .join(EmotionScore)\
        .filter(Entry.user_id == current_user.id,
               Entry.date_created >= seven_days_ago)\
        .order_by(Entry.date_created.asc())\
        .all()
    
    # Prepare data for Chart.js
    dates = []
    joy_scores = []
    sadness_scores = []
    anger_scores = []
    fear_scores = []
    surprise_scores = []
    
    for entry in chart_data:
        dates.append(entry.date_created.strftime('%Y-%m-%d'))
        if entry.emotion_score:  # Check if emotion_score exists
            joy_scores.append(round(entry.emotion_score.joy * 100, 1))
            sadness_scores.append(round(entry.emotion_score.sadness * 100, 1))
            anger_scores.append(round(entry.emotion_score.anger * 100, 1))
            fear_scores.append(round(entry.emotion_score.fear * 100, 1))
            surprise_scores.append(round(entry.emotion_score.surprise * 100, 1))
    
    # NEW: Calculate emotion distribution for pie chart
    all_entries = Entry.query\
        .options(db.joinedload(Entry.emotion_score))\
        .filter(Entry.user_id == current_user.id)\
        .all()
    
    emotion_totals = {
        'joy': 0,
        'sadness': 0,
        'anger': 0,
        'fear': 0,
        'surprise': 0
    }
    
    entry_count = 0
    for entry in all_entries:
        if entry.emotion_score:
            entry_count += 1
            emotion_totals['joy'] += entry.emotion_score.joy
            emotion_totals['sadness'] += entry.emotion_score.sadness
            emotion_totals['anger'] += entry.emotion_score.anger
            emotion_totals['fear'] += entry.emotion_score.fear
            emotion_totals['surprise'] += entry.emotion_score.surprise
    
    # Calculate average percentages
    emotion_distribution = {}
    if entry_count > 0:
        for emotion, total in emotion_totals.items():
            emotion_distribution[emotion] = round((total / entry_count) * 100, 1)
    
    return render_template('dashboard.html', 
                         entries=recent_entries,
                         dates=dates,
                         joy_scores=joy_scores,
                         sadness_scores=sadness_scores,
                         anger_scores=anger_scores,
                         fear_scores=fear_scores,
                         surprise_scores=surprise_scores,
                         emotion_distribution=emotion_distribution,  # NEW
                         entry_count=entry_count)  # NEW
    

# Custom error handler for 401 errors...redundancy a function was created in __init__.py
# @main_routes.app_errorhandler(401)
# def unauthorized_error(error):
#     flash('Please log in to access this page.', 'error')
#     return redirect(url_for('auth.login'))


# Base function example
# @auth_routes.route('/register')
# def register():
#     return render_template('register.html')