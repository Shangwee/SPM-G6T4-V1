CREATE DATABASE IF NOT EXISTS account;

USE account;

CREATE TABLE Employee (
    Staff_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,  -- PK for staff
    Staff_FName VARCHAR(50) NOT NULL,  -- First Name
    Staff_LName VARCHAR(50) NOT NULL,  -- Last Name
    Dept VARCHAR(50) NOT NULL,  -- Department staff belong to
    Position VARCHAR(50) NOT NULL,  -- Position in the organization
    Country VARCHAR(50) NOT NULL,  -- Country located
    Email VARCHAR(50) NOT NULL,  -- Email Address
    Reporting_Manager INT,  -- FK to Staff_ID for reporting manager
    Role INT NOT NULL,  -- Role in the system (HR(1), Staff(2), Manager(3))
    Password VARCHAR(50) NOT NULL  -- Password for login
);

CREATE DATABASE IF NOT EXISTS meeting;

USE meeting;

CREATE TABLE Meeting (
    Meeting_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Created_By INT NOT NULL,
    Date DATE NOT NULL,
    Title TEXT(50) NULL
);

CREATE TABLE MeetingStaffs (
    MeetingStaffs_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Meeting_ID INT NOT NULL,
    Staff_ID INT NOT NULL
);

CREATE DATABASE IF NOT EXISTS notifications;

USE notifications;

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    request_id INT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE DATABASE IF NOT EXISTS request;

USE request;

CREATE TABLE Request (
    Request_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Employee_ID INT NOT NULL,
    Approver_ID INT NOT NULL,
    Date DATE NOT NULL,
    Reason TEXT(100) NULL,
    Status INT NOT NULL DEFAULT 0 -- 0: Pending, 1: Approved, 2: Rejected
);

CREATE DATABASE IF NOT EXISTS schedule;

USE schedule;

CREATE TABLE Schedule (
    Schedule_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Staff_ID INT NOT NULL,
    Request_ID INT NOT NULL,
    Date DATE NOT NULL
);