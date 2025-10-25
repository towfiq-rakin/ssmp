CREATE USER IF NOT EXISTS 'ssmp_user'@'localhost' IDENTIFIED BY 'ssmp_password';
GRANT ALL PRIVILEGES ON ssmp.* TO 'ssmp_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;