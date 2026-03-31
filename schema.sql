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


-- read
/*
SELECT * FROM companies;
SELECT * FROM companies WHERE company_id = %s;

-- update
UPDATE companies SET company_name = %s, industry = %s, website = %s, city = %s, state = %s, notes = %s WHERE company_id = %s;

-- delete
DELETE FROM companies WHERE company_id = %s;*/

-- JOBS
-- create
INSERT IGNORE INTO jobs (company_id, job_title, job_type, salary_min, salary_max, date_posted)
VALUES
(1, 'Software Developer', 'Internship', 70000, 90000, '2025-01-15'),
(1, 'Database Administrator', 'Full-time', 75000, 95000, '2025-01-10'),
(2, 'Data Analyst', 'Contract', 65000, 85000, '2025-01-12'),
(3, 'Cloud Engineer', 'Full-time', 80000, 100000, '2025-01-08'),
(4, 'Junior Developer', 'Part-time', 55000, 70000, '2025-01-14'),
(4, 'Senior Developer', 'Full-time', 95000, 120000, '2025-01-14'),
(5, 'ML Engineer', 'Full-time', 90000, 115000, '2025-01-11');

-- read
/*SELECT * FROM jobs;
SELECT * FROM jobs WHERE job_id = %s;

-- update
UPDATE jobs SET company_id = %s, job_title = %s, job_type = %s, salary_min = %s, salary_max = %s, job_url = %s, date_posted = %s WHERE job_id = %s;

-- delete
DELETE FROM jobs WHERE job_id = %s;*/


-- APPLICATIONS
-- create
INSERT IGNORE INTO applications (job_id, application_date, status, resume_version, cover_letter_sent) 
VALUES
(1, '2025-01-16', 'Applied', 'v2.1', TRUE),
(3, '2025-01-13', 'Interview', 'v2.1', TRUE),
(4, '2025-01-09', 'Rejected', 'v2.0', FALSE),
(5, '2025-01-15', 'Applied', 'v2.1', TRUE),
(7, '2025-01-12', 'Screening', 'v2.1', TRUE);


-- read
/*SELECT * FROM applications;
SELECT * FROM applications WHERE application_id = %s;

-- update
UPDATE applications SET job_id = %s, application_date = %s, status = %s, resume_version = %s, cover_letter_sent = %s, interview_data = %s WHERE application_id = %s;

-- delete
DELETE FROM applications WHERE application_id = %s;*/

-- CONTACTS
-- create
INSERT IGNORE INTO contacts (company_id, contact_name, email, title) 
VALUES
(1, 'Sarah Johnson', 'sjohnson@techsolutions.com', 'HR Manager'),
(2, 'Michael Chen', 'mchen@dataanalytics.com', 'Technical Recruiter'),
(3, 'Emily Williams', 'ewilliams@cloudsystems.com', 'Hiring Manager'),
(4, 'David Brown', NULL, 'Senior Developer'),
(5, 'Lisa Garcia', 'lgarcia@smarttech.com', 'Talent Acquisition');


/*-- read
SELECT * FROM contacts;
SELECT * FROM contacts WHERE contact_id = %s;

-- update
UPDATE contacts SET company_id = %s, contact_name= %s, title = %s, email = %s, phone = %s, linkedin_url = %s, notes = %s WHERE contact_id = %s;

-- delete
DELETE FROM contacts WHERE contact_id = %s;
*/
SHOW Tables;