CREATE TABLE USERS(
    user_id CHAR(255) PRIMARY KEY,
    user_password CHAR(255) NOT NULL,
    user_name CHAR(255) NOT NULL,
    user_email CHAR(255) NOT NULL
);