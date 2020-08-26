CREATE USER 'imgrepo'@'localhost' IDENTIFIED BY 'imgrepo';

GRANT ALL PRIVILEGES ON * . * TO 'imgrepo'@'localhost';

ALTER USER 'imgrepo'@'localhost' IDENTIFIED WITH mysql_native_password BY 'imgrepo';