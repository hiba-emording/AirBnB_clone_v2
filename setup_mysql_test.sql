-- Script to prepare MySQL server for the AirBnB project - test.
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED WITH mysql_native_password BY 'hbnb_test_pwd';
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
