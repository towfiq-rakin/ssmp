# SSMP - Student Scholarship Management Platform

A Flask-based web application for managing student scholarships and academic records at BUP (Bangladesh University of Professionals).

## Features

### Student Features
- Login using email or student ID
- View personal information and academic records
- Access department information

### Admin Features
- Admin login with email
- View all students from their department
- Search students by:
  - Name
  - Student ID
  - Registration Number
  - Email
  - Session
- View detailed student information including academic records
- Department-specific access control

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd ssmp
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up the database
```bash
# Import the schema
mysql -u your_username -p < database/schema.sql

# Import test student data
mysql -u your_username -p ssmp < database/test.sql

# Import test admin accounts
mysql -u your_username -p ssmp < database/admin_test.sql
```

4. Update database configuration in `config.py`
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/ssmp'
```

5. Run the application
```bash
python app.py
```

## Default Test Accounts

### Admin Accounts
- **Email:** ahmed.rahman@bup.edu.bd | **Password:** admin123 (CSE Department)
- **Email:** sarah.khan@bup.edu.bd | **Password:** admin123 (CSE Department)
- **Email:** mohammad.ali@bup.edu.bd | **Password:** admin123 (ICT Department)
- **Email:** fatima.akter@bup.edu.bd | **Password:** admin123 (ICT Department)

### Student Accounts
All test students have the password: `admin`
Example: 
- **Student ID:** 23524202001 | **Password:** admin

## Usage

### Admin Login
1. Go to the login page
2. Select "Admin" from the "Login As" dropdown
3. Enter your admin email and password
4. You'll be redirected to the admin dashboard

### Admin Dashboard Features
- **Student List:** View all students from your department in a table format
- **Search:** Use the search bar to find specific students
- **View Details:** Click "View Details" button to see complete student information
- **Department Filtering:** Only students from your department are visible

### Student Login
1. Go to the login page
2. Select "Student" from the "Login As" dropdown
3. Enter your email or student ID and password
4. You'll be redirected to your personal dashboard

## Project Structure
```
ssmp/
├── app.py                 # Main application file
├── config.py              # Configuration settings
├── extensions.py          # Flask extensions
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── routes/
│   ├── auth.py           # Authentication routes
│   └── main.py           # Main application routes
├── templates/
│   ├── base.html         # Base template
│   ├── base_auth.html    # Auth base template
│   ├── login.html        # Login page
│   ├── dashboard.html    # Student dashboard
│   ├── admin_dashboard.html       # Admin dashboard
│   └── admin_student_detail.html  # Student detail view for admin
├── static/
│   └── css/
│       └── style.css     # Stylesheet
└── database/
    ├── schema.sql        # Database schema
    ├── test.sql          # Test student data
    └── admin_test.sql    # Test admin data
```

## Technologies Used
- **Backend:** Flask, Flask-Login, Flask-SQLAlchemy
- **Database:** MySQL
- **Frontend:** HTML, CSS, Jinja2 templates

## Security Notes
⚠️ **Warning:** This application currently uses plain text passwords for demonstration purposes. In production, you should:
- Implement password hashing (bcrypt, werkzeug.security, etc.)
- Use environment variables for sensitive configuration
- Enable HTTPS
- Implement CSRF protection
- Add rate limiting for login attempts

## License
This project is for educational purposes.
