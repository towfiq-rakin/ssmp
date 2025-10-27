-- Insert test admin accounts
-- Password for all test admins is 'admin123'

-- Admin for Computer Science and Engineering Department (dept_id: 1)
insert into admins (name, dept_id, email, password) values
('Dr. Ahmed Rahman', 1, 'ahmed.rahman@bup.edu.bd', 'admin123'),
('Prof. Sarah Khan', 1, 'sarah.khan@bup.edu.bd', 'admin123');

-- Admin for Information and Communication Technology Department (dept_id: 2)
insert into admins (name, dept_id, email, password) values
('Dr. Mohammad Ali', 2, 'mohammad.ali@bup.edu.bd', 'admin123'),
('Prof. Fatima Akter', 2, 'fatima.akter@bup.edu.bd', 'admin123');
