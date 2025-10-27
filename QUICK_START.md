# Quick Start Guide - Admin Login Feature

## 🚀 Getting Started

### 1. Database Setup
If you haven't already set up the database, run:
```bash
# Set up the main schema (includes admin table)
mysql -u your_username -p < database/schema.sql

# Add additional test admin accounts (optional)
mysql -u your_username -p ssmp < database/admin_test.sql
```

### 2. Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

### 3. Test Admin Login

#### Option 1: Use the existing admin from schema.sql
- **Email:** admin@bupeedu.bd
- **Password:** admin
- **Department:** CSE (Computer Science and Engineering)

#### Option 2: Use test admins from admin_test.sql
- **Email:** ahmed.rahman@bup.edu.bd | **Password:** admin123 (CSE Dept)
- **Email:** sarah.khan@bup.edu.bd | **Password:** admin123 (CSE Dept)
- **Email:** mohammad.ali@bup.edu.bd | **Password:** admin123 (ICT Dept)
- **Email:** fatima.akter@bup.edu.bd | **Password:** admin123 (ICT Dept)

### 4. Login Steps
1. Open browser and go to `http://127.0.0.1:5000`
2. You'll be redirected to the login page
3. Select **"Admin"** from the "Login As" dropdown
4. Enter admin email and password
5. Click "Login"
6. You'll be redirected to the Admin Dashboard

## 🎯 Admin Dashboard Features

### View All Students
- See a complete list of students from your department
- Table shows: Student ID, Registration No, Name, Email, Session
- Total student count displayed at the bottom

### Search Students
- Use the search box to find specific students
- Search works across:
  - Student Name
  - Student ID
  - Registration Number
  - Email
  - Session
- Click "Clear" button to reset search

### View Student Details
- Click "View Details" button for any student
- See complete student information including:
  - Personal details
  - Academic records (CGPA, GPA, Semester)
  - Department information
- Use "← Back to Dashboard" to return to student list

## 🔐 Security Features

### Department-Based Access
- Admins can **only** see students from their own department
- Example: CSE admin cannot view ICT students

### Role-Based Routing
- Admin users automatically redirect to admin dashboard
- Student users redirect to student dashboard
- Attempting to access unauthorized pages will show error message

## 📊 Sample Scenarios

### Test Scenario 1: CSE Admin
1. Login as: admin@bupeedu.bd / admin
2. You should see ~80+ CSE students (all dept_id = 1)
3. Search for "TOWFIQ" to find student 23524202131
4. View their details (CGPA: 3.77)

### Test Scenario 2: ICT Admin
1. Login as: mohammad.ali@bup.edu.bd / admin123
2. You should see 0 students (no ICT students in test data)
3. Message: "No students in your department."

### Test Scenario 3: Search Functionality
1. Login as admin
2. Search "2022-2023" to see all students from that session
3. Search "3.9" to find high-performing students (searches in all fields)
4. Search by email domain "@student.bup.edu.bd"

## 🔄 Switching Between Admin and Student

### To Test Student Login:
1. Logout from admin account
2. Select "Student" from dropdown
3. Login with student credentials:
   - **Student ID:** 23524202131
   - **Password:** admin
4. You'll see the student dashboard (different from admin view)

## ⚠️ Troubleshooting

### Issue: Can't login as admin
- **Check:** Did you select "Admin" from the dropdown?
- **Check:** Using admin email (not student email)
- **Check:** Database has admin records (check with query below)

```sql
SELECT * FROM admins;
```

### Issue: Not seeing any students
- **Check:** Students exist in your admin's department
- **Query:** Check student count per department
```sql
SELECT dept_id, COUNT(*) FROM students GROUP BY dept_id;
```

### Issue: Search not working
- **Try:** Clear browser cache
- **Check:** Search is case-insensitive and searches all fields
- **Test:** Search for a partial match (e.g., "AHMED" instead of full name)

## 📝 Development Notes

### Adding New Admins
```sql
INSERT INTO admins (name, dept_id, email, password) 
VALUES ('New Admin', 1, 'newadmin@bup.edu.bd', 'password123');
```

### Adding Students to Different Departments
```sql
-- Add ICT students for testing
INSERT INTO students (student_id, reg_no, dept_id, name, session, email, password) 
VALUES (23524212001, 105201230001, 2, 'Test ICT Student', '2022-2023', 'ict@student.bup.edu.bd', 'admin');
```

## 🎨 UI Elements

### Admin Dashboard
- Clean table layout with alternating row hover effects
- Search bar with instant feedback
- Professional blue color scheme matching app theme
- Responsive design for mobile devices

### Navigation
- Back button on student detail page
- Clear search option when active
- Logout always available in navbar

## 🚦 Next Steps

After testing the admin feature, you can:
1. Add more departments and their admins
2. Implement admin edit capabilities
3. Add export functionality (CSV/PDF)
4. Create admin statistics dashboard
5. Implement password hashing for production use

---

**Enjoy managing students! 🎓**
