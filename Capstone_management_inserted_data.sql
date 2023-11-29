USE Capstone_management;

-- Insert 5 entries into the Student table
INSERT INTO Student (SRN, CGPA, Department, Section, Phone_Number, Email, Semester, First_Name, Last_Name)
VALUES
    ('SRN001', 3.75, 'Computer Science', 'A', '123-456-7890', 'student1@example.com', 6, 'John', 'Doe'),
    ('SRN002', 3.90, 'Electrical Engineering', 'B', '987-654-3210', 'student2@example.com', 7, 'Jane', 'Smith'),
    ('SRN003', 3.60, 'Mechanical Engineering', 'C', '555-555-5555', 'student3@example.com', 8, 'David', 'Wilson'),
    ('SRN004', 3.80, 'Chemistry', 'A', '999-999-9999', 'student4@example.com', 6, 'Alice', 'Johnson'),
    ('SRN005', 3.95, 'Physics', 'B', '777-777-7777', 'student5@example.com', 7, 'Robert', 'Brown');

-- Insert 5 entries into the Team table
INSERT INTO Team (Phase, ProjectName, ProjectID, TeamID)
VALUES
    (1, 'Project 1', 101, 1),
    (2, 'Project 2', 102, 2),
    (3, 'Project 3', 103, 3),
    (1, 'Project 1', 101, 4),
    (2, 'Project 2', 102, 5);

-- Insert 5 entries into the DomainOfStudy table
INSERT INTO DomainOfStudy (Domain)
VALUES
    ('Computer Science'),
    ('Electrical Engineering'),
    ('Mechanical Engineering'),
    ('Chemistry'),
    ('Physics');

-- Insert 5 entries into the Panel table
INSERT INTO Panel (Panel_ID, Panel_Name, Panel_Team, No_Of_Members)
VALUES
    (1, 'Panel 1', 'Team 1', 3),
    (2, 'Panel 2', 'Team 2', 3),
    (3, 'Panel 3', 'Team 3', 3),
    (4, 'Panel 4', 'Team 4', 3),
    (5, 'Panel 5', 'Team 5', 3);
    
-- Insert 5 entries into the Faculty table
INSERT INTO Faculty (Phone_Number, First_Name, Last_Name, Position, Department, F_SRN, Panel_ID)
VALUES
    ('111-111-1111', 'Dr. Smith', 'Anderson', 'Professor', 'Computer Science', 'F001', 1),
    ('222-222-2222', 'Dr. Sarah', 'Johnson', 'Associate Professor', 'Electrical Engineering', 'F002', 2),
    ('333-333-3333', 'Dr. James', 'Wilson', 'Professor', 'Mechanical Engineering', 'F003', 3),
    ('444-444-4444', 'Dr. Alice', 'Brown', 'Associate Professor', 'Chemistry', 'F004', 4),
    ('555-555-5555', 'Dr. Robert', 'Davis', 'Professor', 'Physics', 'F005', 5);

-- Insert 5 entries into the DomainKnowledge table
INSERT INTO DomainKnowledge (Domain_of_interest, F_SRN)
VALUES
    ('Artificial Intelligence', 'F001'),
    ('Robotics', 'F002'),
    ('Thermodynamics', 'F003'),
    ('Organic Chemistry', 'F004'),
    ('Quantum Physics', 'F005');



-- Insert 5 entries into the Review table
INSERT INTO Review (Review_ID, ISA_1, ISA_2, ESA_1, ISA_3, ISA_4, ESA_2, ESA_3, Faculty_ID, SRN)
VALUES
    (1, 95, 88, 78, 87, 92, 82, 79, 'F001', 'SRN001'),
    (2, 90, 85, 76, 80, 88, 85, 80, 'F002', 'SRN002'),
    (3, 87, 82, 72, 85, 90, 80, 75, 'F003', 'SRN003'),
    (4, 92, 89, 80, 88, 92, 84, 81, 'F004', 'SRN004'),
    (5, 89, 84, 77, 86, 90, 83, 79, 'F005', 'SRN005');
