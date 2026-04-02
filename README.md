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

## Video
<iframe width="560" height="315" src="https://www.youtube.com/embed/zyDR-ml22pk?si=MLPWUTr8K-Da1J5j" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

