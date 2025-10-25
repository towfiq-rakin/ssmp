create database if not exists ssmp;
use ssmp;

-- Departments table (create first since students references it)
create table if not exists departments (
    id int primary key,
    name varchar(100) unique not null,
    faculty varchar(100) not null,
    budget float not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp
);

-- Students table
create table if not exists students (
    id int primary key,
    reg_no int unique not null,
    dept_id int not null,
    name varchar(100) not null,
    session varchar(20) not null,
    email varchar(100) unique not null,
    password varchar(255) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    foreign key (dept_id) references departments(id)
);

-- Academic Records table
create table if not exists academic_records (
    reg_no int primary key,
    student_id int,
    cgpa float not null,
    gpa float not null,
    semester varchar(20) not null,
    foreign key (student_id) references students(id)
);  

insert into departments (id, name, faculty, budget) values
(1, 'Computer Science and Engineering', 'FST', 200000.00),
(2, 'Information and Communication Technology', 'FST', 200000.00),
(3, 'Environmental Science', 'FST', 200000.00);

insert into students (id, reg_no, dept_id, name, session, email, password) values
(23524202131, 104201230131, 1, 'Towfiq Omar Rakin', '2022-2023', '23524202131@student.bup.edu.bd', 'admin');

insert into academic_records (reg_no, student_id, cgpa, gpa, semester) values
(104201230131, 23524202131, 3.77, 3.92, '5th Semester');