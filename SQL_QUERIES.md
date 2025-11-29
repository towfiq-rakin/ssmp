# SQL Queries Used in SSMP (Scholarship and Stipend Management Portal)

## Table of Contents
1. [Database and Schema Creation](#database-and-schema-creation)
2. [SELECT Queries](#select-queries)
3. [INSERT Queries](#insert-queries)
4. [UPDATE Queries](#update-queries)
5. [DELETE Queries](#delete-queries)
6. [Aggregate and Join Queries](#aggregate-and-join-queries)

---

## Database and Schema Creation

### Create Database
```sql
CREATE DATABASE IF NOT EXISTS ssmp;
USE ssmp;
```

### Create Departments Table
```sql
CREATE TABLE IF NOT EXISTS departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    faculty VARCHAR(100) NOT NULL,
    budget FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT dept_budget_check CHECK (budget >= 0)
);
```

### Create Admins Table
```sql
CREATE TABLE IF NOT EXISTS admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    dept_id INT NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (dept_id) REFERENCES departments(id),
    CONSTRAINT admin_email_check CHECK (email LIKE '%@bup.edu.bd')
);
```

### Create Students Table
```sql
CREATE TABLE IF NOT EXISTS students (
    student_id BIGINT PRIMARY KEY,
    reg_no BIGINT UNIQUE NOT NULL,
    dept_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    session VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (dept_id) REFERENCES departments(id),
    CONSTRAINT student_email_check CHECK (email LIKE '%@%')
);
```

### Create Academic Records Table
```sql
CREATE TABLE IF NOT EXISTS academic_records (
    reg_no BIGINT PRIMARY KEY,
    student_id BIGINT,
    cgpa FLOAT NOT NULL,
    semester_1_gpa FLOAT DEFAULT NULL,
    semester_2_gpa FLOAT DEFAULT NULL,
    semester_3_gpa FLOAT DEFAULT NULL,
    semester_4_gpa FLOAT DEFAULT NULL,
    semester_5_gpa FLOAT DEFAULT NULL,
    semester_6_gpa FLOAT DEFAULT NULL,
    semester_7_gpa FLOAT DEFAULT NULL,
    semester_8_gpa FLOAT DEFAULT NULL,
    current_semester INT NOT NULL DEFAULT 5,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT cgpa_check CHECK (cgpa >= 0 AND cgpa <= 4.0),
    CONSTRAINT current_semester_check CHECK (current_semester >= 1 AND current_semester <= 8)
);
```

### Create Income Records Table
```sql
CREATE TABLE IF NOT EXISTS income_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id BIGINT NOT NULL,
    amount FLOAT NOT NULL,
    source VARCHAR(255) NOT NULL,
    family_member INT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT income_amount_check CHECK (amount >= 0),
    CONSTRAINT family_member_check CHECK (family_member >= 0)
);
```

### Create Applications Table
```sql
CREATE TABLE IF NOT EXISTS applications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id BIGINT NOT NULL,
    type VARCHAR(255) NOT NULL,
    semester VARCHAR(50) NOT NULL,
    status VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
```

### Create Scholarships Table
```sql
CREATE TABLE IF NOT EXISTS scholarships (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id BIGINT NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    type VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    semester VARCHAR(50) NOT NULL,
    awarded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
```

### Create Stipends Table
```sql
CREATE TABLE IF NOT EXISTS stipends (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id BIGINT NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    type VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    semester VARCHAR(50) NOT NULL,
    awarded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
```

---

## SELECT Queries

### Authentication Queries

#### Find Admin by Email
```sql
SELECT * FROM admins WHERE email = ?;
```

#### Find Student by Email
```sql
SELECT * FROM students WHERE email = ?;
```

#### Find Student by Student ID
```sql
SELECT * FROM students WHERE student_id = ?;
```

#### Get User by ID (Admin)
```sql
SELECT * FROM admins WHERE id = ?;
```

#### Get User by ID (Student)
```sql
SELECT * FROM students WHERE student_id = ?;
```

### Department Queries

#### Get Department by ID
```sql
SELECT * FROM departments WHERE id = ?;
```

### Student Queries

#### Get Students by Department
```sql
SELECT * FROM students WHERE dept_id = ?;
```

#### Search Students with Filters
```sql
SELECT * FROM students 
WHERE dept_id = ? 
AND (
    name LIKE ? OR 
    email LIKE ? OR 
    student_id LIKE ? OR 
    reg_no LIKE ? OR 
    session LIKE ?
);
```

#### Get Student by Student ID
```sql
SELECT * FROM students WHERE student_id = ?;
```

### Academic Record Queries

#### Get Academic Record by Student ID
```sql
SELECT * FROM academic_records WHERE student_id = ?;
```

#### Get Academic Record by Registration Number
```sql
SELECT * FROM academic_records WHERE reg_no = ?;
```

#### Get Academic Records for Department (with Join)
```sql
SELECT academic_records.* 
FROM academic_records 
JOIN students ON academic_records.student_id = students.student_id 
WHERE students.dept_id = ?;
```

### Scholarship Queries

#### Get Scholarships by Student ID
```sql
SELECT * FROM scholarships 
WHERE student_id = ? 
ORDER BY awarded_at DESC;
```

#### Get Scholarship by Student and Semester
```sql
SELECT * FROM scholarships 
WHERE student_id = ? AND semester = ?;
```

#### Get Scholarship by Student, Type and Semester
```sql
SELECT * FROM scholarships 
WHERE student_id = ? AND type = ? AND semester = ?;
```

#### Get All Scholarships for Department (with Student Join)
```sql
SELECT scholarships.*, students.* 
FROM scholarships 
JOIN students ON scholarships.student_id = students.student_id 
WHERE students.dept_id = ? 
ORDER BY scholarships.awarded_at DESC;
```

### Stipend Queries

#### Get Stipends by Student ID
```sql
SELECT * FROM stipends 
WHERE student_id = ? 
ORDER BY awarded_at DESC;
```

#### Get Stipend by Student and Semester
```sql
SELECT * FROM stipends 
WHERE student_id = ? AND semester = ?;
```

#### Get Stipend by Student, Type and Semester
```sql
SELECT * FROM stipends 
WHERE student_id = ? AND type = ? AND semester = ?;
```

#### Get All Stipends for Department (with Student Join)
```sql
SELECT stipends.*, students.* 
FROM stipends 
JOIN students ON stipends.student_id = students.student_id 
WHERE students.dept_id = ? 
ORDER BY stipends.awarded_at DESC;
```

### Application Queries

#### Get Applications by Student ID
```sql
SELECT * FROM applications 
WHERE student_id = ? 
ORDER BY created_at DESC;
```

#### Get Pending Application by Student, Type and Semester
```sql
SELECT * FROM applications 
WHERE student_id = ? AND type = ? AND semester = ? AND status = 'Pending';
```

#### Get All Applications for Department (with Student Join)
```sql
SELECT applications.* 
FROM applications 
JOIN students ON applications.student_id = students.student_id 
WHERE students.dept_id = ?;
```

#### Get Application by ID
```sql
SELECT * FROM applications WHERE id = ?;
```

### Income Record Queries

#### Get Income Record by Student ID (Latest)
```sql
SELECT * FROM income_records 
WHERE student_id = ? 
ORDER BY date DESC 
LIMIT 1;
```

#### Get Income Record by Student ID
```sql
SELECT * FROM income_records WHERE student_id = ?;
```

### Join Queries for Scholarship Eligibility

#### Get Students with Academic Records for Scholarship Evaluation
```sql
SELECT students.*, academic_records.* 
FROM students 
JOIN academic_records ON students.student_id = academic_records.student_id 
WHERE students.dept_id = ?;
```

---

## INSERT Queries

### Insert Scholarship
```sql
INSERT INTO scholarships (student_id, student_name, type, amount, semester) 
VALUES (?, ?, ?, ?, ?);
```

### Insert Stipend
```sql
INSERT INTO stipends (student_id, student_name, type, amount, semester) 
VALUES (?, ?, ?, ?, ?);
```

### Insert Application
```sql
INSERT INTO applications (student_id, type, semester, status) 
VALUES (?, ?, ?, ?);
```

### Insert Income Record
```sql
INSERT INTO income_records (student_id, amount, source, family_member) 
VALUES (?, ?, ?, ?);
```

### Insert New Student
```sql
INSERT INTO students (student_id, reg_no, dept_id, name, session, email, password) 
VALUES (?, ?, ?, ?, ?, ?, ?);
```

### Insert New Admin
```sql
INSERT INTO admins (name, dept_id, email, password) 
VALUES (?, ?, ?, ?);
```

### Insert New Department
```sql
INSERT INTO departments (name, faculty, budget) 
VALUES (?, ?, ?);
```

### Insert New Academic Record
```sql
INSERT INTO academic_records (reg_no, student_id, cgpa, current_semester) 
VALUES (?, ?, ?, ?);
```

---

## UPDATE Queries

### Update Academic Record
```sql
UPDATE academic_records 
SET current_semester = ?, 
    semester_1_gpa = ?, 
    semester_2_gpa = ?, 
    semester_3_gpa = ?, 
    semester_4_gpa = ?, 
    semester_5_gpa = ?, 
    semester_6_gpa = ?, 
    semester_7_gpa = ?, 
    semester_8_gpa = ?, 
    cgpa = ? 
WHERE student_id = ?;
```

### Update Department Budget
```sql
UPDATE departments 
SET budget = budget - ? 
WHERE id = ?;
```

### Update Application Status (Approve)
```sql
UPDATE applications 
SET status = 'Approved', 
    updated_at = CURRENT_TIMESTAMP 
WHERE id = ?;
```

### Update Application Status (Reject)
```sql
UPDATE applications 
SET status = 'Rejected', 
    updated_at = CURRENT_TIMESTAMP 
WHERE id = ?;
```

### Update Income Record
```sql
UPDATE income_records 
SET amount = ?, 
    source = ?, 
    family_member = ? 
WHERE student_id = ?;
```

### Update Student Information
```sql
UPDATE students 
SET name = ?, 
    email = ?, 
    session = ? 
WHERE student_id = ?;
```

---

## DELETE Queries

### Delete Student (Cascade deletes academic_records and income_records)
```sql
DELETE FROM students WHERE student_id = ?;
```

### Delete Scholarship
```sql
DELETE FROM scholarships WHERE id = ?;
```

### Delete Stipend
```sql
DELETE FROM stipends WHERE id = ?;
```

### Delete Application
```sql
DELETE FROM applications WHERE id = ?;
```

---

## Aggregate and Join Queries

### Count Total Students in Department
```sql
SELECT COUNT(*) FROM students WHERE dept_id = ?;
```

### Sum of All Scholarships for Department
```sql
SELECT SUM(scholarships.amount) 
FROM scholarships 
JOIN students ON scholarships.student_id = students.student_id 
WHERE students.dept_id = ?;
```

### Sum of All Stipends for Department
```sql
SELECT SUM(stipends.amount) 
FROM stipends 
JOIN students ON stipends.student_id = students.student_id 
WHERE students.dept_id = ?;
```

### Count of Scholarships Awarded in Department
```sql
SELECT COUNT(*) 
FROM scholarships 
JOIN students ON scholarships.student_id = students.student_id 
WHERE students.dept_id = ?;
```

### Count of Stipends Awarded in Department
```sql
SELECT COUNT(*) 
FROM stipends 
JOIN students ON stipends.student_id = students.student_id 
WHERE students.dept_id = ?;
```

### Get Academic Records Statistics for Department
```sql
SELECT academic_records.* 
FROM academic_records 
JOIN students ON academic_records.student_id = students.student_id 
WHERE students.dept_id = ?;
```

### Get Students with Academic Records and Income Information
```sql
SELECT students.*, academic_records.*, income_records.* 
FROM students 
LEFT JOIN academic_records ON students.student_id = academic_records.student_id 
LEFT JOIN income_records ON students.student_id = income_records.student_id 
WHERE students.dept_id = ?;
```

### Get Application Details with Student Information
```sql
SELECT applications.*, students.name, students.email, students.session 
FROM applications 
JOIN students ON applications.student_id = students.student_id 
WHERE applications.id = ?;
```

### Get Scholarship Distribution by Type
```sql
SELECT type, COUNT(*) as count, SUM(amount) as total_amount 
FROM scholarships 
JOIN students ON scholarships.student_id = students.student_id 
WHERE students.dept_id = ? 
GROUP BY type;
```

### Get Stipend Distribution by Type
```sql
SELECT type, COUNT(*) as count, SUM(amount) as total_amount 
FROM stipends 
JOIN students ON stipends.student_id = students.student_id 
WHERE students.dept_id = ? 
GROUP BY type;
```

### Get Average CGPA for Department
```sql
SELECT AVG(academic_records.cgpa) 
FROM academic_records 
JOIN students ON academic_records.student_id = students.student_id 
WHERE students.dept_id = ?;
```

### Get Students Above Certain CGPA Threshold
```sql
SELECT students.*, academic_records.cgpa 
FROM students 
JOIN academic_records ON students.student_id = academic_records.student_id 
WHERE students.dept_id = ? AND academic_records.cgpa >= ?;
```

### Get Total Financial Aid per Student
```sql
SELECT 
    students.student_id,
    students.name,
    COALESCE(SUM(scholarships.amount), 0) as scholarship_total,
    COALESCE(SUM(stipends.amount), 0) as stipend_total,
    COALESCE(SUM(scholarships.amount), 0) + COALESCE(SUM(stipends.amount), 0) as total_aid
FROM students
LEFT JOIN scholarships ON students.student_id = scholarships.student_id
LEFT JOIN stipends ON students.student_id = stipends.student_id
WHERE students.dept_id = ?
GROUP BY students.student_id, students.name;
```
