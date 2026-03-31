# job-application-tracker
A web application to help track job applications during the job search process.
## Features (Coming Soon)
- Track companies and job listings
- Record application submissions
- Manage interview schedules
- Store contact information
## Technologies
- MySQL Database
- Python with Flask
- HTML/CSS for the web interface

## Local setup
Set your MySQL credentials as environment variables before starting Flask.

PowerShell (current terminal session):

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = "YOUR_ACTUAL_PASSWORD"
$env:DB_NAME = "job_application_tracker"
python app.py
```

If you prefer not to use `root`, create a dedicated MySQL user and grant it access to `job_application_tracker`.
