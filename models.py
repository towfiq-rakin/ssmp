"""
Database Models
"""
from flask_login import UserMixin
from extensions import db


class Department(db.Model):
    """Department Model"""
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    faculty = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    
    def __repr__(self):
        return f'<Department {self.name}>'


class Admin(UserMixin, db.Model):
    """Admin Model"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dept_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    
    def get_id(self):
        return f'admin_{self.id}'
    
    def get_department(self):
        return Department.query.get(self.dept_id)
    
    def __repr__(self):
        return f'<Admin {self.name}>'


class User(UserMixin, db.Model):
    """User Model - mapped to students table"""
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
        return f'student_{self.student_id}'
    
    # Relationship with department
    def get_department(self):
        return Department.query.get(self.dept_id)
    
    def __repr__(self):
        return f'<User {self.name}>'


class AcademicRecord(db.Model):
    """Academic Records Model"""
    __tablename__ = 'academic_records'
    
    reg_no = db.Column(db.BigInteger, primary_key=True)
    student_id = db.Column(db.BigInteger, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    semester_1_gpa = db.Column(db.Float, nullable=True)
    semester_2_gpa = db.Column(db.Float, nullable=True)
    semester_3_gpa = db.Column(db.Float, nullable=True)
    semester_4_gpa = db.Column(db.Float, nullable=True)
    semester_5_gpa = db.Column(db.Float, nullable=True)
    semester_6_gpa = db.Column(db.Float, nullable=True)
    semester_7_gpa = db.Column(db.Float, nullable=True)
    semester_8_gpa = db.Column(db.Float, nullable=True)
    current_semester = db.Column(db.Integer, nullable=False, default=5)
    
    def get_current_gpa(self):
        """Get GPA for the current semester (may be None if not yet graded)"""
        semester_field = f'semester_{self.current_semester}_gpa'
        return getattr(self, semester_field, None)
    
    def get_last_semester_gpa(self):
        """Get GPA for the last completed semester (current_semester - 1)"""
        if self.current_semester <= 1:
            return None
        last_semester = self.current_semester - 1
        semester_field = f'semester_{last_semester}_gpa'
        return getattr(self, semester_field, None)
    
    def get_last_completed_semester(self):
        """Get the last completed semester number"""
        return self.current_semester - 1 if self.current_semester > 1 else 0
    
    def calculate_cgpa(self):
        """Calculate CGPA from all non-null semester GPAs"""
        gpas = []
        for i in range(1, 9):
            gpa = getattr(self, f'semester_{i}_gpa')
            if gpa is not None:
                gpas.append(gpa)
        
        if gpas:
            return round(sum(gpas) / len(gpas), 2)
        return 0.0
    
    def __repr__(self):
        return f'<AcademicRecord {self.reg_no}>'


class Scholarship(db.Model):
    """Scholarship Model"""
    __tablename__ = 'scholarships'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.BigInteger, nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    awarded_at = db.Column(db.TIMESTAMP)
    
    def __repr__(self):
        return f'<Scholarship {self.student_name} - {self.type}>'


class Stipend(db.Model):
    """Stipend Model"""
    __tablename__ = 'stipends'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.BigInteger, nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    awarded_at = db.Column(db.TIMESTAMP)
    
    def __repr__(self):
        return f'<Stipend {self.student_name} - {self.type}>'


class IncomeRecord(db.Model):
    """Income Record Model"""
    __tablename__ = 'income_records'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.BigInteger, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(255), nullable=False)
    family_member = db.Column(db.Integer, nullable=False)
    date = db.Column(db.TIMESTAMP)
    
    def __repr__(self):
        return f'<IncomeRecord {self.student_id} - {self.amount}>'


class Application(db.Model):
    """Application Model"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.BigInteger, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Application {self.student_id} - {self.type} - {self.status}>'
