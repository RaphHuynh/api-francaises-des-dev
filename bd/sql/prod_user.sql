CREATE DATABASE IF NOT EXISTS `API_francaises_des_dev`;

CREATE USER 'api'@'%' IDENTIFIED BY 'api';
GRANT ALL PRIVILEGES on API_francaises_des_dev.* TO 'api'@'%';
FLUSH PRIVILEGES;