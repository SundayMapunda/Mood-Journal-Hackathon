from app import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime

# This callback is required by Flask-Login to reload the user object from the user ID stored in the session.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the User model. 'UserMixin' provides default implementations for methods Flask-Login expects.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # This sets up a one-to-many relationship: one User can have many Entries.
    # The 'backref' creates a virtual column in the Entry model (e.g., entry.author)
    entries = db.relationship('Entry', backref='author', lazy=True)

    # Property to set a password - it automatically hashes it using bcrypt
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Method to check a provided password against the stored hash
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # How the object is printed for debugging
    def __repr__(self):
        return f'<User {self.username}>'

# Association Table for the many-to-many relationship between Entry and Tag
# This is a simple table with no additional fields, so we define it without a model class.
entry_tag = db.Table('entry_tag',
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Foreign key to link the entry to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # This sets up the many-to-many relationship with the Tag model via the association table.
    tags = db.relationship('Tag', secondary=entry_tag, backref=db.backref('entries', lazy='dynamic'))
    
    # How the object is printed for debugging
    def __repr__(self):
        return f'<Entry {self.id}>'

class EmotionScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    joy = db.Column(db.Float, default=0.0)
    sadness = db.Column(db.Float, default=0.0)
    anger = db.Column(db.Float, default=0.0)
    fear = db.Column(db.Float, default=0.0)
    surprise = db.Column(db.Float, default=0.0)
    
    # Foreign key to link the scores to a specific entry (One-to-One relationship)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False, unique=True)
    
    # How the object is printed for debugging
    def __repr__(self):
        return f'<EmotionScore for Entry {self.entry_id}>'

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # How the object is printed for debugging
    def __repr__(self):
        return f'<Tag {self.name}>'