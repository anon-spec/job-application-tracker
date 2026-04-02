-- Database creation script
CREATE DATABASE IF NOT EXISTS job_application_tracker;
USE job_application_tracker;

-- Companies
CREATE TABLE IF NOT EXISTS companies(
company_id INT PRIMARY KEY AUTO_INCREMENT,
company_name VARCHAR(100) NOT NULL,
industry VARCHAR(50),
website VARCHAR(200),
city VARCHAR(50),
state VARCHAR(50),
notes TEXT
);

-- jobs
CREATE TABLE IF NOT EXISTS jobs(
job_id INT PRIMARY KEY AUTO_INCREMENT,
company_id INT,
job_title VARCHAR(100) NOT NULL,
job_type ENUM('Full-time', 'Part-time', 'Contract', 'Internship'),
salary_min INT, salary_max INT,
job_url VARCHAR(300),
date_posted DATE,
requirements JSON,
UNIQUE KEY uq_jobs_combo (company_id, job_title, job_type, salary_min, salary_max, date_posted, job_url, requirements(255)),
FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- applications
CREATE TABLE IF NOT EXISTS applications(
application_id INT PRIMARY KEY AUTO_INCREMENT,
job_id INT,
application_date DATE NOT NULL,
status ENUM('Applied', 'Screening', 'Interview', 'Offer', 'Rejected', 'Withdrawn'),
resume_version VARCHAR(50),
cover_letter_sent BOOLEAN,
interview_data JSON,
FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);

-- contacts
CREATE TABLE IF NOT EXISTS contacts(
contact_id INT PRIMARY KEY AUTO_INCREMENT,
company_id INT,
contact_name VARCHAR(100) NOT NULL,
title VARCHAR(100),
email VARCHAR(100),
phone VARCHAR(20),
linkedin_url VARCHAR(200),
notes TEXT,
FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- COMPANIES
-- create
INSERT IGNORE INTO companies (company_name, industry, website, city, state)
VALUES
('Tech Solutions Inc', 'Technology', 'www.techsolutions.com', 'Miami', 'Florida'),
('Data Analytics Corp', 'Data Science', 'www.dataanalytics.com', 'Austin', 'Texas'),
('Cloud Systems LLC', 'Cloud Computing', 'www.cloudsystems.com', 'Seattle', 'Washington'),
('Digital Innovations', 'Software', 'www.digitalinnovations.com', 'San Francisco', 'California'),
('Smart Tech Group', 'AI/ML', 'www.smarttech.com', 'Boston',
'Massachusetts');




-- JOBS
-- create
INSERT IGNORE INTO jobs (company_id, job_title, job_type, salary_min, salary_max, date_posted, requirements)
VALUES
(1, 'Software Developer', 'Internship', 70000, 90000, '2025-01-15', JSON_OBJECT('required_skills', JSON_ARRAY('python', 'sql', 'git'), 'preferred_skills', JSON_ARRAY('flask', 'docker', 'aws'), 'education', 'Bachelor in CS or related field', 'experience_years', 2, 'remote_option', TRUE)),
(1, 'Database Administrator', 'Full-time', 75000, 95000, '2025-01-10', JSON_OBJECT('required_skills', JSON_ARRAY('sql', 'mysql', 'python'), 'preferred_skills', JSON_ARRAY('linux', 'aws'), 'education', 'Bachelor degree', 'experience_years', 2, 'remote_option', FALSE)),
(2, 'Data Analyst', 'Contract', 65000, 85000, '2025-01-12', JSON_OBJECT('required_skills', JSON_ARRAY('sql', 'excel', 'tableau'), 'preferred_skills', JSON_ARRAY('python', 'r'), 'education', 'Bachelor degree', 'experience_years', 1, 'remote_option', FALSE)),
(3, 'Cloud Engineer', 'Full-time', 80000, 100000, '2025-01-08', JSON_OBJECT('required_skills', JSON_ARRAY('aws', 'docker', 'linux'), 'preferred_skills', JSON_ARRAY('terraform', 'python'), 'education', 'Bachelor degree', 'experience_years', 3, 'remote_option', TRUE)),
(4, 'Junior Developer', 'Part-time', 55000, 70000, '2025-01-14', JSON_OBJECT('required_skills', JSON_ARRAY('html', 'css', 'javascript'), 'preferred_skills', JSON_ARRAY('react', 'git'), 'education', 'Associate degree', 'experience_years', 1, 'remote_option', TRUE)),
(4, 'Senior Developer', 'Full-time', 95000, 120000, '2025-01-14', JSON_OBJECT('required_skills', JSON_ARRAY('python', 'flask', 'postgresql'), 'preferred_skills', JSON_ARRAY('docker', 'aws', 'ci/cd'), 'education', 'Bachelor in CS or related field', 'experience_years', 4, 'remote_option', TRUE)),
(5, 'ML Engineer', 'Full-time', 90000, 115000, '2025-01-11', JSON_OBJECT('required_skills', JSON_ARRAY('python', 'pandas', 'scikit-learn'), 'preferred_skills', JSON_ARRAY('tensorflow', 'sql', 'docker'), 'education', 'Bachelor in CS or related field', 'experience_years', 2, 'remote_option', TRUE));




-- APPLICATIONS
-- create
INSERT IGNORE INTO applications (job_id, application_date, status, resume_version, cover_letter_sent) 
VALUES
(1, '2025-01-16', 'Applied', 'v2.1', TRUE),
(3, '2025-01-13', 'Interview', 'v2.1', TRUE),
(4, '2025-01-09', 'Rejected', 'v2.0', FALSE),
(5, '2025-01-15', 'Applied', 'v2.1', TRUE),
(7, '2025-01-12', 'Screening', 'v2.1', TRUE);



-- CONTACTS
-- create
INSERT IGNORE INTO contacts (company_id, contact_name, email, title) 
VALUES
(1, 'Sarah Johnson', 'sjohnson@techsolutions.com', 'HR Manager'),
(2, 'Michael Chen', 'mchen@dataanalytics.com', 'Technical Recruiter'),
(3, 'Emily Williams', 'ewilliams@cloudsystems.com', 'Hiring Manager'),
(4, 'David Brown', NULL, 'Senior Developer'),
(5, 'Lisa Garcia', 'lgarcia@smarttech.com', 'Talent Acquisition');



SHOW Tables;

UPDATE applications
SET interview_data = '{
	"interview_rounds": 2,
    "interviewers": ["Sarah Johnson", "Mike Chen"],
    "technical_questions": ["SQL joins", "Python basics", "API design"],
    "feedback": "Strong technical skills, good communication",
    "next_steps": "Final round scheduled"
}'
WHERE application_id = 2;

UPDATE applications
SET interview_data = '{
	"interview_rounds": 1, 
    "interviewers": ["Emily Williams"],
    "technical_questions": ["Database normalization", "Transaction isolation"],
    "feedback": "Needs more experience with cloud platforms",
    "rating": 3
}'
WHERE application_id = 4;

UPDATE jobs
SET requirements = '{
	"required_skills": ["Python", "SQL", "Git"],
    "preferred_skills": ["Flask", "Docker", "AWS"],
    "education": "Bachelor in CS or related field",
    "experience_years": 2,
    "remote_option": true
}'
WHERE job_id = 1;

UPDATE jobs 
SET requirements = '{
	"required_skills": ["SQL", "Excel", "Tableau"],
    "preferred_skills": ["Python", "R"],
    "education": "Bachelor degree",
    "experience_years": 1,
    "remote_option": false
}'
WHERE job_id = 3;