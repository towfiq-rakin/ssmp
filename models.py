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
    gpa = db.Column(db.Float, nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f'<AcademicRecord {self.reg_no}>'
