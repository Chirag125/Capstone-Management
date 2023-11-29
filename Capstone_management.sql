-- Create the Student table
create database dbms;
use dbms;
show tables;
CREATE TABLE Student (
    SRN VARCHAR(10) PRIMARY KEY,
    CGPA DECIMAL(4, 2) DEFAULT 0 CHECK (CGPA >= 0 AND CGPA <= 10),
    Department VARCHAR(255) NOT NULL,
    Section CHAR(1) NOT NULL,
    Phone_Number VARCHAR(15) DEFAULT 'N/A',
    Email VARCHAR(255) DEFAULT 'N/A',
    Semester INT DEFAULT 6 CHECK (Semester > 5 AND Semester < 9),
    First_Name VARCHAR(255) DEFAULT 'N/A',
    Last_Name VARCHAR(255) DEFAULT 'N/A'
);

-- Create the Team table
CREATE TABLE Team (
    Phase INT,
    ProjectName VARCHAR(255),
    ProjectID INT,
    TeamID INT,
    PRIMARY KEY (TeamID, ProjectID)
);

-- Create the DomainOfStudy table
CREATE TABLE DomainOfStudy (
    Domain VARCHAR(255)
);

-- Create the Faculty table
CREATE TABLE Faculty (
    Phone_Number VARCHAR(15),
    First_Name VARCHAR(255),
    Last_Name VARCHAR(255),
    Position VARCHAR(255),
    Department VARCHAR(255),
    F_SRN VARCHAR(10) PRIMARY KEY
);

-- Create the DomainKnowledge table
CREATE TABLE DomainKnowledge (
    Domain_of_interest VARCHAR(255)
);

-- Create the Panel table
CREATE TABLE Panel (
    Panel_ID INT PRIMARY KEY,
    Panel_Name VARCHAR(255),
    Panel_Team VARCHAR(255),
    No_Of_Members INT CHECK (No_Of_Members >= 2 AND No_Of_Members <= 4)
);

-- Create the Review table
CREATE TABLE Review (
    ISA_1 INT,
    ISA_2 INT,
    ESA_1 INT,
    ISA_3 INT,
    ISA_4 INT,
    ESA_2 INT,
    ESA_3 INT
);

CREATE TABLE LoginCredentials (
    Username VARCHAR(255) PRIMARY KEY,
    Password VARCHAR(255),
    UserType ENUM('user', 'teacher', 'admin')
);



-- Add foreign key (TeamID, ProjectID) REFERENCES Team(TeamID, ProjectID) to Student table
ALTER TABLE Student
ADD TeamID INT,
ADD ProjectID INT;

-- Add foreign key constraint
ALTER TABLE Student
ADD CONSTRAINT fk_Student_Team FOREIGN KEY (TeamID, ProjectID) REFERENCES Team(TeamID, ProjectID);

-- Add foreign key (SRN) REFERENCES Faculty(F_SRN) to Team table
ALTER TABLE Team
ADD F_SRN varchar(10);

ALTER TABLE Team
ADD CONSTRAINT fk_Team_Faculty FOREIGN KEY (F_SRN) REFERENCES Faculty(F_SRN);

-- Add foreign key (PanelID) REFERENCES Panel(Panel_ID) to Team table


-- Add foreign key (TeamID, ProjectID) REFERENCES Team(TeamID, ProjectID) to DomainOfStudy table
ALTER TABLE DomainOfStudy
ADD TeamID INT,
ADD ProjectID INT;

ALTER TABLE DomainOfStudy
ADD CONSTRAINT fk_DomainOfStudy_Team FOREIGN KEY (TeamID, ProjectID) REFERENCES Team(TeamID, ProjectID);

-- Add foreign key (PanelID) REFERENCES Panel(Panel_ID) to Faculty table
ALTER TABLE Faculty
ADD Panel_ID INT;

ALTER TABLE Faculty
ADD CONSTRAINT fk_Faculty_Panel FOREIGN KEY (Panel_ID) REFERENCES Panel(Panel_ID);

-- Add foreign key (SRN) REFERENCES Faculty(F_SRN) to DomainKnowledge table
ALTER TABLE DomainKnowledge
ADD F_SRN varchar(10);

ALTER TABLE DomainKnowledge
ADD CONSTRAINT fk_DomainKnowledge_Faculty FOREIGN KEY (F_SRN) REFERENCES Faculty(F_SRN);

-- Add foreign key (Faculty_ID) REFERENCES Faculty(F_SRN) to Review table
ALTER TABLE Review
ADD Faculty_ID varchar(10);

ALTER TABLE Review
ADD CONSTRAINT fk_Review_Faculty FOREIGN KEY (Faculty_ID) REFERENCES Faculty(F_SRN);

-- Add foreign key (SRN) REFERENCES Student(SRN) to Review table
ALTER TABLE Review
ADD SRN varchar(10);

ALTER TABLE Review
ADD CONSTRAINT fk_Review_Student FOREIGN KEY (SRN) REFERENCES Student(SRN);



 
 






 
