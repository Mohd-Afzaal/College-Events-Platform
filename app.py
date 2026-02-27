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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # check if user already exists
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('register'))
        # create new user
        new_user = Users(name=name, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            # redirect to dashboard or next page
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'club_admin':
        return render_template(url_for('club_dashboard'))
    elif current_user.role == 'student':
        return render_template(url_for('student_dashboard'))
    elif current_user.role == 'college_admin':
        return render_template(url_for('admin_dashboard'))
    else:
        flash('Invalid user role.', 'danger')
        return redirect(url_for('index'))

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    registrations = Registrations.query.filter_by(student_id=current_user.id).all()
    return render_template('student_dashboard.html', registrations=registrations)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
    app.run(debug=True)