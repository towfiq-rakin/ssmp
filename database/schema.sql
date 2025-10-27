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

-- Admin table
create table if not exists admins (
    id int primary key auto_increment,
    name varchar(100) not null,
    dept_id int not null,
    email varchar(100) unique not null,
    password varchar(255) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    foreign key (dept_id) references departments(id)
);


-- Students table
create table if not exists students (
    student_id bigint primary key,
    reg_no bigint unique not null,
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
    reg_no bigint primary key,
    student_id bigint,
    cgpa float not null,
    gpa float not null,
    semester varchar(20) not null,
    foreign key (student_id) references students(student_id)
);  

-- Income records table
create table if not exists income_records (
    id int primary key auto_increment,
    student_id bigint not null,
    amount float not null,
    source varchar(255) not null,
    family_member int not null,
    date timestamp default current_timestamp,
    foreign key (student_id) references students(student_id)
);

-- Application table
create table if not exists applications (
    id int primary key auto_increment,
    student_id bigint not null,
    type varchar(255) not null,
    semester varchar(50) not null,
    status varchar(100) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    foreign key (student_id) references students(student_id)
);

-- Scholarship table
create table if not exists scholarships (
    id int primary key auto_increment,
    student_id bigint not null,
    student_name varchar(100) not null,
    type varchar(100) not null,
    amount float not null,
    semester varchar(50) not null,
    awarded_at timestamp default current_timestamp,
    foreign key (student_id) references students(student_id)
);

-- Stipend table
create table if not exists stipends (
    id int primary key auto_increment,
    student_id bigint not null,
    student_name varchar(100) not null,
    type varchar(100) not null,
    amount float not null,
    semester varchar(50) not null,
    awarded_at timestamp default current_timestamp,
    foreign key (student_id) references students(student_id)
);

insert into departments (id, name, faculty, budget) values
(1, 'Computer Science and Engineering', 'FST', 200000.00),
(2, 'Information and Communication Technology', 'FST', 200000.00),
(3, 'Environmental Science', 'FST', 200000.00);

insert into students (student_id, reg_no, dept_id, name, session, email, password) values
(2252421061,104201220061,1, 'LUTFUL AHMED NADIM', '2021-2022', '2252421061@student.bup.edu.bd', 'admin'),
(2252421086,104201220086,1, 'MAINUL HASSAN ASIF', '2021-2022', '2252421086@student.bup.edu.bd', 'admin'),
(2252421109,104201220109,1, 'AFSANA HENA', '2021-2022', '2252421109@student.bup.edu.bd', 'admin'),
(2252421120,104201220120,1, 'FARHAN ISHRAQ', '2021-2022', '2252421120@student.bup.edu.bd', 'admin'),
(23524202001,104201230001,1, 'M TASDIK MUTTAKI', '2022-2023', '23524202001@student.bup.edu.bd', 'admin'),
(23524202014,104201230014,1, 'AJWAD MOHTASIM', '2022-2023', '23524202014@student.bup.edu.bd', 'admin'),
(23524202021,104201230021,1, 'REHNUMA SALSABIL BINTE OBAYED', '2022-2023', '23524202021@student.bup.edu.bd', 'admin'),
(23524202024,104201230024,1, 'PRANABANTA SHETH SPONDON', '2022-2023', '23524202024@student.bup.edu.bd', 'admin'),
(23524202028,104201230028,1, 'MD. ZUNAYED IQBAL SHAHED', '2022-2023', '23524202028@student.bup.edu.bd', 'admin'),
(23524202029,104201230029,1, 'MISHA MALIHA', '2022-2023', '23524202029@student.bup.edu.bd', 'admin'),
(23524202030,104201230030,1, 'SAJID-AL-ADEEB', '2022-2023', '23524202030@student.bup.edu.bd', 'admin'),
(23524202041,104201230041,1, 'MD. TAHMIDUR RAHMAN KHAN', '2022-2023', '23524202041@student.bup.edu.bd', 'admin'),
(23524202042,104201230042,1, 'SHAHRIAR MAHMUD APURBO', '2022-2023', '23524202042@student.bup.edu.bd', 'admin'),
(23524202043,104201230043,1, 'FAIZA MUSTARI', '2022-2023', '23524202043@student.bup.edu.bd', 'admin'),
(23524202044,104201230044,1, 'SHAH MASROOR KABIR', '2022-2023', '23524202044@student.bup.edu.bd', 'admin'),
(23524202045,104201230045,1, 'GOLAM ALI KIBRIA', '2022-2023', '23524202045@student.bup.edu.bd', 'admin'),
(23524202047,104201230047,1, 'MD. MAINUL ISLAM', '2022-2023', '23524202047@student.bup.edu.bd', 'admin'),
(23524202048,104201230048,1, 'AYSHA SIDDIKA', '2022-2023', '23524202048@student.bup.edu.bd', 'admin'),
(23524202049,104201230049,1, 'MD.JONAEID KABIR SHANTO', '2022-2023', '23524202049@student.bup.edu.bd', 'admin'),
(23524202051,104201230051,1, 'SAROWAR HOSSAIN RONY', '2022-2023', '23524202051@student.bup.edu.bd', 'admin'),
(23524202052,104201230052,1, 'NUSAIR AHMED CHOWDHURY', '2022-2023', '23524202052@student.bup.edu.bd', 'admin'),
(23524202053,104201230053,1, 'FAIYAZ KAMRUL KHAN', '2022-2023', '23524202053@student.bup.edu.bd', 'admin'),
(23524202054,104201230054,1, 'ABDULLAH BIN TOWHID', '2022-2023', '23524202054@student.bup.edu.bd', 'admin'),
(23524202059,104201230059,1, 'TASHFIN RUAID', '2022-2023', '23524202059@student.bup.edu.bd', 'admin'),
(23524202060,104201230060,1, 'RUDRO ROY DIP', '2022-2023', '23524202060@student.bup.edu.bd', 'admin'),
(23524202061,104201230061,1, 'AL SADIQUE NUHIN', '2022-2023', '23524202061@student.bup.edu.bd', 'admin'),
(23524202062,104201230062,1, 'MD. ABU SAYED', '2022-2023', '23524202062@student.bup.edu.bd', 'admin'),
(23524202064,104201230064,1, 'UMME HANI PUNAM', '2022-2023', '23524202064@student.bup.edu.bd', 'admin'),
(23524202065,104201230065,1, 'MD. JUNAYET HOSSAIN MOHIT', '2022-2023', '23524202065@student.bup.edu.bd', 'admin'),
(23524202068,104201230068,1, 'MD. MARUF ALL RUSHAFI', '2022-2023', '23524202068@student.bup.edu.bd', 'admin'),
(23524202070,104201230070,1, 'MD. ABU ZIHAD', '2022-2023', '23524202070@student.bup.edu.bd', 'admin'),
(23524202071,104201230071,1, 'MARJIA KHATUN', '2022-2023', '23524202071@student.bup.edu.bd', 'admin'),
(23524202075,104201230075,1, 'ABDULLAH AL - YAMIN', '2022-2023', '23524202075@student.bup.edu.bd', 'admin'),
(23524202085,104201230085,1, 'ABDULLAH MAHMUD YAMIN', '2022-2023', '23524202085@student.bup.edu.bd', 'admin'),
(23524202088,104201230088,1, 'TASNIM RASHID MEDHA', '2022-2023', '23524202088@student.bup.edu.bd', 'admin'),
(23524202089,104201230089,1, 'SUMAIYA HOSSAIN ANIKA', '2022-2023', '23524202089@student.bup.edu.bd', 'admin'),
(23524202091,104201230091,1, 'MD. RAISUL ISLAM', '2022-2023', '23524202091@student.bup.edu.bd', 'admin'),
(23524202095,104201230095,1, 'SM SHAHRIER EMON', '2022-2023', '23524202095@student.bup.edu.bd', 'admin'),
(23524202096,104201230096,1, 'MD. RIFAT AL HASSAN ROMAN', '2022-2023', '23524202096@student.bup.edu.bd', 'admin'),
(23524202100,104201230100,1, 'ABRAR ZAHIN', '2022-2023', '23524202100@student.bup.edu.bd', 'admin'),
(23524202103,104201230103,1, 'FARHAN ISRAQ JAMI', '2022-2023', '23524202103@student.bup.edu.bd', 'admin'),
(23524202104,104201230104,1, 'DEWAN SOWAIB SADIF', '2022-2023', '23524202104@student.bup.edu.bd', 'admin'),
(23524202107,104201230107,1, 'IFTHEKHAR AHMED', '2022-2023', '23524202107@student.bup.edu.bd', 'admin'),
(23524202108,104201230108,1, 'SHEIKH SIFAT RAHMAN', '2022-2023', '23524202108@student.bup.edu.bd', 'admin'),
(23524202109,104201230109,1, 'SHREYA SARKER', '2022-2023', '23524202109@student.bup.edu.bd', 'admin'),
(23524202110,104201230110,1, 'TAQI TAHMID', '2022-2023', '23524202110@student.bup.edu.bd', 'admin'),
(23524202112,104201230112,1, 'MD. MASUM MEHORAB', '2022-2023', '23524202112@student.bup.edu.bd', 'admin'),
(23524202114,104201230114,1, 'M. SABBIR HASNAT SHAON', '2022-2023', '23524202114@student.bup.edu.bd', 'admin'),
(23524202116,104201230116,1, 'M SAIMOON GALIB', '2022-2023', '23524202116@student.bup.edu.bd', 'admin'),
(23524202117,104201230117,1, 'MD.MUSFIQUR RAHMAN SAMA', '2022-2023', '23524202117@student.bup.edu.bd', 'admin'),
(23524202118,104201230118,1, 'OVIZIT DUTT OVI', '2022-2023', '23524202118@student.bup.edu.bd', 'admin'),
(23524202119,104201230119,1, 'MD. MEHEDI HASAN FOYSAL', '2022-2023', '23524202119@student.bup.edu.bd', 'admin'),
(23524202120,104201230120,1, 'MD. MOSTAFIZUR RAHAMAN SHUVO', '2022-2023', '23524202120@student.bup.edu.bd', 'admin'),
(23524202121,104201230121,1, 'MIHIR BORMON', '2022-2023', '23524202121@student.bup.edu.bd', 'admin'),
(23524202122,104201230122,1, 'SUMEHRA AFSHEEN NUHAA', '2022-2023', '23524202122@student.bup.edu.bd', 'admin'),
(23524202123,104201230123,1, 'JANNATUL SHANJIMOM AURPY', '2022-2023', '23524202123@student.bup.edu.bd', 'admin'),
(23524202124,104201230124,1, 'MD. TAMJID AHMAD EMON', '2022-2023', '23524202124@student.bup.edu.bd', 'admin'),
(23524202125,104201230125,1, 'RAIHANUL HASAN KHAN', '2022-2023', '23524202125@student.bup.edu.bd', 'admin'),
(23524202126,104201230126,1, 'SHAZZAD HOSSAN LABIB', '2022-2023', '23524202126@student.bup.edu.bd', 'admin'),
(23524202128,104201230128,1, 'MASNOON TAHIM SIJAN', '2022-2023', '23524202128@student.bup.edu.bd', 'admin'),
(23524202129,104201230129,1, 'ABDUL HAKIM SHIFAT', '2022-2023', '23524202129@student.bup.edu.bd', 'admin'),
(23524202130,104201230130,1, 'TAMIM SHARIAR', '2022-2023', '23524202130@student.bup.edu.bd', 'admin'),
(23524202131,104201230131,1, 'TOWFIQ OMAR RAKIN', '2022-2023', '23524202131@student.bup.edu.bd', 'admin'),
(23524202133,104201230133,1, 'TAHIA ZAIMA', '2022-2023', '23524202133@student.bup.edu.bd', 'admin'),
(23524202134,104201230134,1, 'TABIDA AHMED SUMAIYA', '2022-2023', '23524202134@student.bup.edu.bd', 'admin'),
(23524202135,104201230135,1, 'ABID HASAN ZIDEN', '2022-2023', '23524202135@student.bup.edu.bd', 'admin'),
(23524202136,104201230136,1, 'MST. REBEKA SULTANA ORCE', '2022-2023', '23524202136@student.bup.edu.bd', 'admin'),
(23524202137,104201230137,1, 'MASHRAFI ELAHI', '2022-2023', '23524202137@student.bup.edu.bd', 'admin'),
(23524202138,104201230138,1, 'SUMAIYA BINTA SHAMS', '2022-2023', '23524202138@student.bup.edu.bd', 'admin'),
(23524202139,104201230139,1, 'ZARIN TASNIM RAHMAN TULY', '2022-2023', '23524202139@student.bup.edu.bd', 'admin'),
(23524202140,104201230140,1, 'MST. SUMAIYA AKTER', '2022-2023', '23524202140@student.bup.edu.bd', 'admin'),
(23524202141,104201230141,1, 'MD. ALVEE AHNAF KHAN', '2022-2023', '23524202141@student.bup.edu.bd', 'admin'),
(23524202142,104201230142,1, 'MST. ANIKA RAHAT SHIPLA', '2022-2023', '23524202142@student.bup.edu.bd', 'admin'),
(23524202143,104201230143,1, 'SHAHED SHAHRIER', '2022-2023', '23524202143@student.bup.edu.bd', 'admin'),
(23524202145,104201230145,1, 'NUZHAT SAIMA', '2022-2023', '23524202145@student.bup.edu.bd', 'admin'),
(23524202146,104201230146,1, 'NAFIZ AL ANJIM AHMED', '2022-2023', '23524202146@student.bup.edu.bd', 'admin'),
(23524202147,104201230147,1, 'MEHAR NIGAR ANONNA', '2022-2023', '23524202147@student.bup.edu.bd', 'admin'),
(23524202148,104201230148,1, 'MD. ABID REJWAN', '2022-2023', '23524202148@student.bup.edu.bd', 'admin'),
(23524202149,104201230149,1, 'MD. SHOAIB', '2022-2023', '23524202149@student.bup.edu.bd', 'admin'),
(23524202151,104201230151,1, 'MD. TAHMID ALAM', '2022-2023', '23524202151@student.bup.edu.bd', 'admin');

insert into academic_records (reg_no, student_id, cgpa, gpa, semester) values
('104201220061', '2252421061', 3.06, 2.61, '5th semester'),
('104201220086', '2252421086', 2.60, 2.68, '5th semester'),
('104201220109', '2252421109', 3.99, 3.98, '5th semester'),
('104201220120', '2252421120', 3.16, 3.44, '5th semester'),
('104201230001', '23524202001', 3.59, 3.63, '5th semester'),
('104201230014', '23524202014', 3.54, 3.81, '5th semester'),
('104201230021', '23524202021', 3.74, 3.87, '5th semester'),
('104201230024', '23524202024', 3.72, 3.68, '5th semester'),
('104201230028', '23524202028', 3.92, 3.98, '5th semester'),
('104201230029', '23524202029', 3.83, 3.9, '5th semester'),
('104201230030', '23524202030', 3.94, 4, '5th semester'),
('104201230041', '23524202041', 3.59, 3.7, '5th semester'),
('104201230042', '23524202042', 3.33, 3.54, '5th semester'),
('104201230043', '23524202043', 3.04, 3.38, '5th semester'),
('104201230044', '23524202044', 2.83, 2.88, '5th semester'),
('104201230045', '23524202045', 3.12, 3.07, '5th semester'),
('104201230047', '23524202047', 3.47, 3.33, '5th semester'),
('104201230048', '23524202048', 3.3, 3.51, '5th semester'),
('104201230049', '23524202049', 2.81, 2.83, '5th semester'),
('104201230051', '23524202051', 3.43, 3.33, '5th semester'),
('104201230052', '23524202052', 3.73, 3.91, '5th semester'),
('104201230054', '23524202054', 2.94, 3.37, '5th semester'),
('104201230059', '23524202059', 3.17, 3.04, '5th semester'),
('104201230060', '23524202060', 3.29, 3.44, '5th semester'),
('104201230061', '23524202061', 3.13, 3.22, '5th semester'),
('104201230062', '23524202062', 3.5, 3.34, '5th semester'),
('104201230064', '23524202064', 3.87, 3.88, '5th semester'),
('104201230065', '23524202065', 3.81, 3.81, '5th semester'),
('104201230068', '23524202068', 3.24, 3.27, '5th semester'),
('104201230070', '23524202070', 3.86, 3.81, '5th semester'),
('104201230071', '23524202071', 3.92, 3.98, '5th semester'),
('104201230075', '23524202075', 3.88, 3.82, '5th semester'),
('104201230085', '23524202085', 3.65, 3.48, '5th semester'),
('104201230088', '23524202088', 3.8, 3.85, '5th semester'),
('104201230089', '23524202089', 3.57, 3.95, '5th semester'),
('104201230091', '23524202091', 3.35, 3.38, '5th semester'),
('104201230095', '23524202095', 2.77, 2.91, '5th semester'),
('104201230096', '23524202096', 3.04, 3.15, '5th semester'),
('104201230100', '23524202100', 3.97, 4, '5th semester'),
('104201230103', '23524202103', 3.76, 3.79, '5th semester'),
('104201230104', '23524202104', 2.85, 2.49, '5th semester'),
('104201230107', '23524202107', 3.25, 3.26, '5th semester'),
('104201230108', '23524202108', 3.85, 3.83, '5th semester'),
('104201230109', '23524202109', 3.94, 3.98, '5th semester'),
('104201230110', '23524202110', 3.42, 3.68, '5th semester'),
('104201230112', '23524202112', 3.13, 3.15, '5th semester'),
('104201230114', '23524202114', 3.34, 3.37, '5th semester'),
('104201230116', '23524202116', 3.03, 3.02, '5th semester'),
('104201230117', '23524202117', 3.51, 3.41, '5th semester'),
('104201230118', '23524202118', 3.74, 3.88, '5th semester'),
('104201230119', '23524202119', 3.22, 3.11, '5th semester'),
('104201230121', '23524202121', 3.39, 3.39, '5th semester'),
('104201230122', '23524202122', 3.63, 3.65, '5th semester'),
('104201230123', '23524202123', 3.38, 3.46, '5th semester'),
('104201230124', '23524202124', 2.99, 3.08, '5th semester'),
('104201230125', '23524202125', 3.52, 3.41, '5th semester'),
('104201230126', '23524202126', 2.93, 2.69, '5th semester'),
('104201230129', '23524202129', 3.44, 3.41, '5th semester'),
('104201230130', '23524202130', 3.16, 3.14, '5th semester'),
('104201230131', '23524202131', 3.77, 3.92, '5th semester'),
('104201230133', '23524202133', 3.33, 3.6, '5th semester'),
('104201230134', '23524202134', 3.09, 3.34, '5th semester'),
('104201230135', '23524202135', 3.51, 3.67, '5th semester'),
('104201230136', '23524202136', 3.01, 3.09, '5th semester'),
('104201230137', '23524202137', 3.06, 3.13, '5th semester'),
('104201230138', '23524202138', 2.78, 2.79, '5th semester'),
('104201230139', '23524202139', 3.16, 3.3, '5th semester'),
('104201230140', '23524202140', 3.07, 3.26, '5th semester'),
('104201230141', '23524202141', 3.28, 3.16, '5th semester'),
('104201230142', '23524202142', 2.94, 2.54, '5th semester'),
('104201230143', '23524202143', 3.42, 3.51, '5th semester'),
('104201230145', '23524202145', 3.64, 3.79, '5th semester'),
('104201230146', '23524202146', 2.85, 3.03, '5th semester'),
('104201230147', '23524202147', 2.73, 2.76, '5th semester'),
('104201230148', '23524202148', 3.11, 3.38, '5th semester'),
('104201230149', '23524202149', 3.13, 3.49, '5th semester'),
('104201230151', '23524202151', 2.94, 2.84, '5th semester');
