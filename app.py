from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# MySQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ssmp_user:ssmp_password@localhost/ssmp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Department Model
class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    faculty = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

# User Model - mapped to students table
class User(UserMixin, db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.BigInteger, primary_key=True)
    reg_no = db.Column(db.BigInteger, unique=True, nullable=False)
    dept_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    session = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    
    # Override get_id for Flask-Login since we use student_id instead of id
    def get_id(self):
        return str(self.student_id)
    
    # Relationship with department
    def get_department(self):
        return Department.query.get(self.dept_id)

# Academic Records Model
class AcademicRecord(db.Model):
    __tablename__ = 'academic_records'
    
    reg_no = db.Column(db.BigInteger, primary_key=True)
    student_id = db.Column(db.BigInteger, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    gpa = db.Column(db.Float, nullable=False)
    semester = db.Column(db.String(20), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_id = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        # Try to find user by email first
        user = User.query.filter_by(email=email_or_id).first()
        
        # If not found by email, try by student ID
        if not user:
            try:
                student_id = int(email_or_id)
                user = User.query.filter_by(student_id=student_id).first()
            except ValueError:
                # Not a valid number, skip ID lookup
                pass
        
        # Direct password comparison (plain text)
        if user and user.password == password:
            login_user(user, remember=remember)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email/ID or password')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Get department info
    department = current_user.get_department()
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=current_user.student_id).first()
    
    return render_template('dashboard.html', 
                         user=current_user, 
                         department=department,
                         academic_record=academic_record)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
