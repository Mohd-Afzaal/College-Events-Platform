from flask import Flask, request, render_template
from models import db, Users, Clubs, Announcements, Events, Registrations
import os

# initializing the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
# Add Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///college_events.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initializing database
db.init_app(app)

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
    app.run(debug=True)