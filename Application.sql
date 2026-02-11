DROP DATABASE IF EXISTS Application;
CREATE DATABASE Application;
USE Application;

CREATE TABLE Users(
user_id int,
email_address varchar(200),
password_hash varchar(50),
PRIMARY KEY (user_id)
);

CREATE TABLE Profiles(
profile_id int,
user_id int,
user_first_name varchar(50),
user_last_name varchar(50),
phone_number varchar(15),
address varchar(200),
date_of_birth date,
PRIMARY KEY (profile_id),
FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Departments(
department_id int,
department_name varchar(100),
PRIMARY KEY (department_id)
);

CREATE TABLE Roles(
role_id int,
role_name varchar(100),
PRIMARY KEY (role_id)
);

CREATE TABLE Skills(
skill_id int,
skill_name varchar(100),
PRIMARY KEY (skill_id)
);

CREATE TABLE Locations(
location_id int,
location_name varchar(100),
address varchar(200),
capacity int,
latitude decimal,
longitude decimal,
PRIMARY KEY (location_id)
);

CREATE TABLE Schedule_Slots(
slot_id int,
user_id int,
skill_id int,
location_id int,
date date,
slot_start_time time,
slot_end_time time,
task varchar(250),
location_description varchar(250),
PRIMARY KEY (slot_id),
FOREIGN KEY (user_id) REFERENCES Users(user_id),
FOREIGN KEY (skill_id) REFERENCES Skills(skill_id),
FOREIGN KEY (location_id) REFERENCES Locations(location_id)
);

CREATE TABLE JUNCTION_Users_Schedule_Slots(
user_id int,
slot_id int,
FOREIGN KEY (user_id) REFERENCES Users(user_id),
FOREIGN KEY (slot_id) REFERENCES Schedule_Slots(slot_id)
);

CREATE TABLE JUNCTION_Users_Departments(
user_id int,
department_id int,
FOREIGN KEY (user_id) REFERENCES Users(user_id),
FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

CREATE TABLE JUNCTION_Users_Roles(
user_id int,
role_id int,
FOREIGN KEY (user_id) REFERENCES Users(user_id),
FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);

CREATE TABLE JUNCTION_Users_Skills(
user_id int,
skill_id int,
FOREIGN KEY (user_id) REFERENCES Users(user_id),
FOREIGN KEY (skill_id) REFERENCES Skills(skill_id)
);

SELECT * FROM Users;
SELECT * FROM Profiles;
SELECT * FROM Departments;
SELECT * FROM Roles;
SELECT * FROM Skills;
SELECT * FROM Locations;
SELECT * FROM Schedule_Slots;
SELECT * FROM JUNCTION_Users_Schedule_Slots;
SELECT * FROM JUNCTION_Users_Departments;
SELECT * FROM JUNCTION_Users_Roles;
SELECT * FROM JUNCTION_Users_Skills;