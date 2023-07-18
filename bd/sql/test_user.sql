CREATE DATABASE IF NOT EXISTS `API_francaises_des_dev_test`;

CREATE USER 'test'@'%' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES on API_francaises_des_dev_test.* TO 'test'@'%';
FLUSH PRIVILEGES;