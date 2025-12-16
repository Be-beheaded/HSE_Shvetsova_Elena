CREATE DATABASE IF NOT EXISTS university_db;
USE university_db;


CREATE TABLE IF NOT EXISTS Student_groups (
    group_id INT PRIMARY KEY AUTO_INCREMENT,
    group_name VARCHAR(50) NOT NULL UNIQUE,
    course_level TINYINT NOT NULL,
    CONSTRAINT chk_course_level_range CHECK (course_level BETWEEN 1 AND 5)
);

CREATE TABLE IF NOT EXISTS Teachers (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    birth_date DATE NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) UNIQUE
);

CREATE TABLE IF NOT EXISTS Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    birth_date DATE NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) UNIQUE,
    group_id INT NOT NULL,
    enrollment_year YEAR NOT NULL,
    FOREIGN KEY (group_id) REFERENCES Student_groups(group_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Subjects (
    subject_id INT PRIMARY KEY AUTO_INCREMENT,
    subject_name VARCHAR(100) NOT NULL UNIQUE,
    subject_type ENUM('Math', 'Humanities')	
);

CREATE TABLE IF NOT EXISTS SubjectAssignments (
    assignment_id INT PRIMARY KEY AUTO_INCREMENT,
    subject_id INT NOT NULL,
    teacher_id INT NOT NULL,
    group_id INT NOT NULL,
    academic_year YEAR NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES Student_groups(group_id) ON DELETE CASCADE,
    UNIQUE KEY uk_assignment (subject_id, teacher_id, group_id, academic_year)
);

CREATE TABLE IF NOT EXISTS Grades (
    grade_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    teacher_id INT NOT NULL,
    grade_value TINYINT NOT NULL,
    grade_date DATE NOT NULL,
    CONSTRAINT chk_grade_range CHECK (grade_value BETWEEN 1 AND 5),
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id) ON DELETE RESTRICT,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id) ON DELETE RESTRICT
);

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS  AddGradeByEmail(
    IN p_student_email VARCHAR(100),    
    IN p_subject_name VARCHAR(100),
    IN p_teacher_email VARCHAR(100),       
    IN p_grade INT
)
BEGIN 
	DECLARE std_id INT;
	DECLARE teach_id INT;
	DECLARE subj_id INT;

        SELECT student_id INTO std_id FROM Students WHERE email = p_student_email;
	SELECT teacher_id INTO teach_id FROM Teachers WHERE email = p_teacher_email;
	SELECT subject_id INTO subj_id FROM Subjects WHERE subject_name = p_subject_name;

	IF std_id IS NOT NULL AND teach_id IS NOT NULL AND subj_id IS NOT NULL THEN
	INSERT INTO Grades (student_id, subject_id, teacher_id, grade_value, grade_date)
        VALUES (std_id, subj_id, teach_id, p_grade, CURDATE());
END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS AddSubjectAssignmentByEmail(
    IN p_teacher_email VARCHAR(100),       
    IN p_subject_name VARCHAR(100),       
    IN p_group_name VARCHAR(50),       
    IN p_academic_year VARCHAR(100)
)
BEGIN 
	DECLARE gr_id INT;
	DECLARE teach_id INT;
	DECLARE subj_id INT;

        SELECT group_id INTO gr_id FROM Student_groups WHERE group_name = p_group_name;
	SELECT teacher_id INTO teach_id FROM Teachers WHERE email = p_teacher_email;
	SELECT subject_id INTO subj_id FROM Subjects WHERE subject_name = p_subject_name;

	IF gr_id IS NOT NULL AND teach_id IS NOT NULL AND subj_id IS NOT NULL THEN
	INSERT INTO SubjectAssignments (subject_id, teacher_id, group_id, academic_year)
        VALUES (subj_id, teach_id, gr_id, p_academic_year);
END IF;
END //
DELIMITER ;

INSERT INTO Student_groups (group_name, course_level) VALUES 
('CS-101', 1), ('CS-102', 1), ('MATH-201', 2);

INSERT INTO Teachers (first_name, last_name, middle_name, email, phone, birth_date) VALUES 
('John', 'Doe', NULL, 'john.doe@uni.edu', '1234567890', '1980-05-15'),
('Jane', 'Smith', NULL, 'jane.smith@uni.edu', '0987654321', '1985-08-20'),
('Alan', 'Turing', 'James', 'alan.turing@uni.edu', NULL, '1912-06-23'),
('Marie', 'Curie', NULL, 'marie.c@uni.edu', '5551112233', '1867-11-07'),
('Albert', 'Einstein', NULL, 'albert.e@uni.edu', '5552223344', '1879-03-14');

INSERT INTO Subjects (subject_name, subject_type) VALUES 
('History', 'Humanities'),
('Physics', 'Math'),
('Literature', 'Humanities'),
('Databases', 'Math'),
('Algebra', 'Math');

INSERT INTO Students (first_name, last_name, birth_date, email, group_id, enrollment_year) VALUES 
('Alice', 'Johnson', '2005-03-10', 'alice.j@student.edu', 1, 2023),
('Bob', 'Williams', '2004-11-25', 'bob.w@student.edu', 1, 2023),
('Charlie', 'Brown', '2005-01-15', 'charlie.b@student.edu', 2, 2024),
('David', 'King', '2004-10-01', 'david.k@student.edu', 2, 2023),
('Fiona', 'Green', '2003-05-20', 'fiona.g@student.edu', 3, 2023), 
('Grace', 'Hall', '2003-05-20', 'grace.h@student.edu', 3, 2023),
('Mark', 'Zucker', '2002-01-01', 'mark.z@student.edu', 1, 2022), 
('Emily', 'Brown', '2005-01-15', 'emily.b@student.edu', 2, 2024),
('Ivan', 'Petrov', '2005-07-07', 'ivan.p@student.edu', 1, 2024);

CALL AddSubjectAssignmentByEmail('marie.c@uni.edu', 'Literature', 'CS-101', 2024);
CALL AddSubjectAssignmentByEmail('albert.e@uni.edu', 'Literature', 'CS-101', 2024);
CALL AddSubjectAssignmentByEmail('marie.c@uni.edu', 'Physics', 'MATH-201', 2024);
CALL AddSubjectAssignmentByEmail('john.doe@uni.edu', 'History', 'MATH-201', 2024);
CALL AddSubjectAssignmentByEmail('alan.turing@uni.edu', 'Physics', 'CS-101', 2023);
CALL AddSubjectAssignmentByEmail('jane.smith@uni.edu', 'Databases', 'CS-102', 2024);
CALL AddSubjectAssignmentByEmail('jane.smith@uni.edu', 'Databases', 'CS-101', 2024);
CALL AddSubjectAssignmentByEmail('john.doe@uni.edu', 'Physics', 'MATH-201', 2024);
CALL AddSubjectAssignmentByEmail('alan.turing@uni.edu', 'History', 'CS-102', 2024);
CALL AddSubjectAssignmentByEmail('jane.smith@uni.edu', 'Algebra', 'CS-101', 2024);
CALL AddSubjectAssignmentByEmail('jane.smith@uni.edu', 'Physics', 'MATH-201', 2024);
CALL AddSubjectAssignmentByEmail('jane.smith@uni.edu', 'History', 'CS-102', 2024);
CALL AddSubjectAssignmentByEmail('john.doe@uni.edu', 'History', 'CS-101', 2024);

CALL AddGradeByEmail('bob.w@student.edu', 'Databases', 'jane.smith@uni.edu', 4);
CALL AddGradeByEmail('charlie.b@student.edu', 'Databases', 'jane.smith@uni.edu', 3);
CALL AddGradeByEmail('alice.j@student.edu', 'Physics', 'marie.c@uni.edu', 5);
CALL AddGradeByEmail('alice.j@student.edu', 'History', 'marie.c@uni.edu', 4); 
CALL AddGradeByEmail('alice.j@student.edu', 'Literature', 'albert.e@uni.edu', 2);
CALL AddGradeByEmail('alice.j@student.edu', 'Literature', 'albert.e@uni.edu', 3);
CALL AddGradeByEmail('grace.h@student.edu', 'Databases', 'marie.c@uni.edu', 5);
CALL AddGradeByEmail('grace.h@student.edu', 'History', 'john.doe@uni.edu', 5);
CALL AddGradeByEmail('bob.w@student.edu', 'Literature', 'albert.e@uni.edu', 2);
CALL AddGradeByEmail('david.k@student.edu', 'Literature', 'albert.e@uni.edu', 2);
CALL AddGradeByEmail('emily.b@student.edu', 'History', 'alan.turing@uni.edu', 2);
CALL AddGradeByEmail('fiona.g@student.edu', 'Physics', 'marie.c@uni.edu', 5); 
CALL AddGradeByEmail('david.k@student.edu', 'Databases', 'marie.c@uni.edu', 2);
CALL AddGradeByEmail('mark.z@student.edu', 'Physics', 'alan.turing@uni.edu', 3);
CALL AddGradeByEmail('mark.z@student.edu', 'Physics', 'alan.turing@uni.edu', 5);
CALL AddGradeByEmail('ivan.p@student.edu', 'Physics', 'alan.turing@uni.edu', 5);
CALL AddGradeByEmail('ivan.p@student.edu', 'Databases', 'jane.smith@uni.edu', 5);
CALL AddGradeByEmail('ivan.p@student.edu', 'Algebra', 'jane.smith@uni.edu', 4);
CALL AddGradeByEmail('ivan.p@student.edu', 'History', 'john.doe@uni.edu', 2);
CALL AddGradeByEmail('ivan.p@student.edu', 'Literature', 'marie.c@uni.edu', 3);
