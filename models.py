from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import UserMixin 

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    clubs = db.relationship('Clubs', backref='admin', lazy=True)
    registrations = db.relationship('Registrations', backref='student', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f'<User {self.name}>'
    
class Clubs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # relationships
    announcements = db.relationship('Announcements', backref='club', lazy=True)

    def __repr__(self):
        return f'<Club {self.name}>'

class Announcements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)

    def __repr__(self):
        return f'<Announcement {self.title}>'

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    max_participants = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    registrations = db.relationship('Registrations', backref='event', lazy=True)
    
    @property
    def is_full(self):
        return len(self.registrations) >= self.max_participants

    @property
    def spots_left(self):
        return self.max_participants - len(self.registrations)

    def __repr__(self):
        return f'<Event {self.title}>'

class Registrations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('student_id', 'event_id', name='unique_registration'),)

    def __repr__(self):
        return f'<Registration Student {self.student_id} Event {self.event_id}>'