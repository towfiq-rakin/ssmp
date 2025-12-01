# SSMP - Scholarship and Stipend Management Portal

A comprehensive Flask-based web application for managing student scholarships, stipends, and academic records at BUP (Bangladesh University of Professionals).

## Features

### Student Features
- 🔐 Login using email or student ID
- 📊 View personal information and academic records
- 🎓 Check scholarship eligibility based on GPA
- 💰 Apply for stipends (General/Vice Chancellor)
- 📜 View scholarship and stipend award history
- 📈 Track application status
- 🏛️ Access department information

### Admin Features
- 🔑 Secure admin login with email
- 👥 View and manage all students from their department
- 🔍 Advanced search students by:
  - Name
  - Student ID
  - Registration Number
  - Email
  - Session
- 🎖️ Award scholarships (General/Chancellor's List)
- 💵 Review and approve/reject stipend applications
- 📑 View detailed student information including academic records
- 📊 Generate reports (Excel & PDF exports)
- 📧 Send email notifications for awards
- 🏢 Department-specific access control
- 📈 Analytics and statistics dashboard

## Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/towfiq-rakin/ssmp.git
cd ssmp
```

2. **Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate     # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up MySQL database**
```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE ssmp;
CREATE USER 'ssmp_user'@'localhost' IDENTIFIED BY 'ssmp_password';
GRANT ALL PRIVILEGES ON ssmp.* TO 'ssmp_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Import the schema
mysql -u ssmp_user -p ssmp < database/schema.sql
```

5. **Configure environment variables**

Create a `.env` file in the project root:
```bash
## Usage

### Admin Workflow

1. **Login**
   - Navigate to `/login`
   - Select "Admin" from the "Login As" dropdown
   - Enter admin email and password

2. **Dashboard Features**
   - View total students, scholarships awarded, and stipends awarded
   - Access navigation menu for Students, Scholarships, Stipends, Analytics

3. **Student Management**
   - View all students from your department
   - Search by name, ID, email, or session
   - Export student lists to Excel or PDF
   - View detailed student academic records

4. **Scholarship Management**
   - View eligible students based on GPA criteria
   - Award General Scholarship (GPA ≥ 3.50)
   - Award Chancellor's List Scholarship (GPA ≥ 3.75)
   - View awarded scholarships with export options
   - Email notifications sent automatically (if enabled)

5. **Stipend Management**
   - Review pending stipend applications
   - Approve/reject applications
   - Award General Stipend (GPA ≥ 3.50)
   - Award Vice Chancellor Stipend (GPA ≥ 3.75)
   - View stipend history with export options
   - Email notifications for approvals/rejections

6. **Analytics**
   - View department statistics
   - Scholarship distribution charts
   - Stipend distribution charts
   - GPA distribution analysis

### Student Workflow

1. **Login**
   - Navigate to `/login`
   - Select "Student" from the "Login As" dropdown
   - Enter email/student ID and password

2. **Dashboard**
   - View personal information
   - Check academic records and CGPA
   - Navigate to Scholarships or Stipends sections

## Project Structure
```
ssmp/
├── app.py                          # Main application file
├── config.py                       # Configuration settings
├── extensions.py                   # Flask extensions (db, login_manager, mail)
├── models.py                       # Database models (User, Admin, Scholarship, Stipend, etc.)
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not in repo)
├── routes/
│   ├── __init__.py                # Routes package
│   ├── auth.py                    # Authentication routes
│   ├── main.py                    # Main dashboard routes
│   ├── student.py                 # Student-facing routes
│   ├── student_actions.py         # Student application actions
│   ├── admin.py                   # Admin dashboard routes
│   ├── admin_scholarship.py       # Scholarship management
│   ├── admin_stipend.py          # Stipend management
│   ├── analytics.py              # Analytics and statistics
│   ├── reports.py                # Excel/PDF export functionality
│   └── email_utils.py            # Email notification utilities
├── templates/
│   ├── base.html                 # Base template
│   ├── base_auth.html            # Auth base template
│   ├── home.html                 # Landing page
│   ├── login.html                # Login page
│   ├── dashboard.html            # Student dashboard
## Technologies Used

### Backend
- **Framework:** Flask 3.0.0
- **Authentication:** Flask-Login 0.6.3
- **Database ORM:** Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0.23
- **Database Driver:** PyMySQL 1.1.0
- **Email:** Flask-Mail 0.9.1
- **Environment:** python-dotenv 1.0.1

### Reports & Export
- **Excel Generation:** openpyxl 3.1.2
- **PDF Generation:** reportlab 4.0.7

### Database
- **Primary:** MySQL 5.7+
- **Connection:** mysql+pymysql connector

### Frontend
- **Templates:** Jinja2
- **Styling:** Custom CSS with gradients and animations
- **Icons:** Unicode symbols and custom designs

### Charts & Visualization
- **Analytics:** Matplotlib 3.8.2 (for future enhancements)

## Key Features Explained

### Scholarship System
- **Eligibility Criteria:**
  - General Scholarship: CGPA ≥ 3.50
  - Chancellor's List: CGPA ≥ 3.75
- **Automatic Award:** Admins can award from eligible students list
- **No Duplicate Awards:** System prevents awarding same semester twice
- **Email Notifications:** Automatic emails on scholarship award

### Stipend System
- **Application-Based:** Students apply for stipends
- **Eligibility Checks:**
  - Minimum 1 semester completed
  - Last semester GPA ≥ 3.50 (General)
  - Last semester GPA ≥ 3.75 (Vice Chancellor)
- **No Overlap:** Cannot have scholarship and stipend for same semester
- **Approval Workflow:** Admin reviews and approves/rejects
- **Email Notifications:** Sent on approval/rejection

### Report Generation
- **Formats:** Excel (.xlsx) and PDF (.pdf)
- **Reports Available:**
## Security Features

✅ **Implemented:**
- Password hashing using Werkzeug
- Session-based authentication with Flask-Login
- Department-based access control
- Environment variables for sensitive data (.env)
- SQL injection protection via SQLAlchemy ORM
- User type verification (Admin vs Student)

⚠️ **For Production Deployment:**
- Enable HTTPS/SSL
- Implement CSRF protection
- Add rate limiting for login attempts
- Set up firewall rules
- Use secure secret key
- Enable database backups
- Implement audit logging
- Add two-factor authentication (optional)

## Database Schema

### Key Tables:
- **students:** Student information
- **academic_records:** Semester GPAs and CGPA
- **admins:** Admin users
- **departments:** Department information
- **scholarships:** Awarded scholarships
- **stipends:** Awarded stipends
- **applications:** Stipend applications
- **income_records:** Student income data (for stipend eligibility)

### Relationships:
- Students → Academic Records (1:1)
- Students → Department (N:1)
- Students → Scholarships (1:N)
- Students → Stipends (1:N)
- Students → Applications (1:N)
- Admins → Department (N:1)

## API Endpoints

### Public Routes
- `GET /` - Landing page
- `GET /login` - Login page
- `POST /login` - Login submission
- `GET /logout` - Logout

### Student Routes (Authentication Required)
- `GET /dashboard` - Student dashboard
- `GET /student/scholarships` - Scholarship eligibility and history
- `GET /student/stipends` - Stipend application and history
- `POST /student/apply_stipend` - Apply for stipend

### Admin Routes (Admin Authentication Required)
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/students` - Students list
- `GET /admin/student/<id>` - Student details
- `GET /admin/scholarships` - Award scholarship page
- `GET /admin/scholarships/view` - View awarded scholarships
- `POST /admin/award_scholarship` - Award scholarship
- `GET /admin/stipend/applications` - Pending applications
- `GET /admin/stipends/view` - View awarded stipends
- `POST /admin/stipend/approve/<id>` - Approve stipend
- `POST /admin/stipend/reject/<id>` - Reject stipend
- `GET /admin/analytics` - Analytics dashboard

### Report Routes
- `GET /admin/reports/students/excel` - Export students to Excel
- `GET /admin/reports/students/pdf` - Export students to PDF
- `GET /admin/reports/scholarships/excel` - Export scholarships to Excel
- `GET /admin/reports/scholarships/pdf` - Export scholarships to PDF
- `GET /admin/reports/stipends/excel` - Export stipends to Excel
- `GET /admin/reports/stipends/pdf` - Export stipends to PDF

## Troubleshooting

### Common Issues:

**1. Module not found errors**
```bash
pip install -r requirements.txt --force-reinstall
```

**2. MySQL connection errors**
```bash
# Check MySQL is running
sudo systemctl status mysql
# Start if stopped
sudo systemctl start mysql
```

**3. Email not sending**
- Check Gmail App Password is correct
- Verify `SEND_EMAILS=True` in .env
- Check spam folder for emails

**4. Port already in use**
```bash
# Find process on port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

**5. Database schema errors**
```bash
# Drop and recreate database
mysql -u root -p
DROP DATABASE ssmp;
CREATE DATABASE ssmp;
EXIT;
mysql -u root -p ssmp < database/schema.sql
```

## Contributing

This is an academic project for Bangladesh University of Professionals (BUP). Contributions are welcome for educational purposes.

### Development Workflow:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is developed for educational purposes at Bangladesh University of Professionals (BUP).

## Contact

**Developer:** Towfiq Rakin  
**Institution:** Bangladesh University of Professionals  
**Project:** Scholarship and Stipend Management Portal

---

**Note:** This project demonstrates a full-stack web application with Flask, MySQL, email integration, and report generation capabilities. It showcases authentication, authorization, database relationships, and CRUD operations in a real-world academic context.
- **Provider:** Gmail SMTP (smtp.gmail.com:587)
- **Toggle:** Can enable/disable via `SEND_EMAILS` in `.env`
- **Templates:** HTML email templates
- **Notifications For:**
  - Scholarship awards
  - Stipend approvals
  - Stipend rejections

## Email Configuration

To enable email notifications:

1. **Get Gmail App Password:**
   - Go to Google Account settings
   - Enable 2-Factor Authentication
   - Generate App Password for Mail

2. **Update .env file:**
```bash
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-digit-app-password
SEND_EMAILS=True  # Set to False to disable
```

3. **Test email functionality:**
   - Award a scholarship to a student
   - Check if email is sent successfullytudents list
│   ├── admin_student_detail.html # Student detail view
│   ├── admin_scholarships.html   # Scholarship awarding page
│   ├── admin_scholarships_view.html # Awarded scholarships view
│   ├── admin_scholarship_detail.html # Scholarship details
│   ├── admin_stipend_applications.html # Stipend applications
│   ├── admin_stipends_view.html  # Awarded stipends view
│   └── admin_stipend_detail.html # Stipend details
├── static/
│   ├── css/
│   │   └── style.css             # Main stylesheet
│   └── img/                      # Images and assets
├── database/
│   ├── schema.sql                # Complete database schema
│   ├── test.sql                  # Test student data
│   └── user.sql                  # User/admin data
└── instance/
    └── ssmp.db                   # SQLite database (if using SQLite)
```
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
