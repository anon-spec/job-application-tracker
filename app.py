import json

from flask import Flask, render_template, redirect, request, url_for
from database import get_db

app = Flask(__name__)


def normalize_skill(value):
    if not value:
        return ""
    return " ".join(str(value).strip().lower().split())

#Parses skills for job_match function
def parse_skills_csv(value):
    if not value:
        return []
    seen = set()
    skills = []
    for item in str(value).split(","):
        skill = normalize_skill(item)
        if skill and skill not in seen:
            seen.add(skill)
            skills.append(skill)
    return skills


#Parses the requirements JSON object and normalizes to canonical shape
def parse_requirements_value(value):
    normalized_empty = {
        "required_skills": [],
        "preferred_skills": [],
    }

    if value is None:
        return normalized_empty

    if isinstance(value, list):
        return {
            "required_skills": parse_skills_csv(",".join(str(item) for item in value)),
            "preferred_skills": [],
        }

    if isinstance(value, dict):
        required_source = value.get("required_skills") or value.get("skills") or []
        preferred_source = value.get("preferred_skills") or value.get("preffered_skills") or []

        required_skills = parse_skills_csv(",".join(str(item) for item in required_source)) if isinstance(required_source, list) else parse_skills_csv(required_source)
        preferred_skills = parse_skills_csv(",".join(str(item) for item in preferred_source)) if isinstance(preferred_source, list) else parse_skills_csv(preferred_source)

        normalized = {
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
        }

        if "education" in value:
            normalized["education"] = value.get("education")
        if "experience_years" in value:
            normalized["experience_years"] = value.get("experience_years")
        if "remote_option" in value:
            normalized["remote_option"] = value.get("remote_option")

        return normalized

    text = str(value).strip()
    if not text:
        return normalized_empty

    try:
        json_value = json.loads(text)
        return parse_requirements_value(json_value)
    except json.JSONDecodeError:
        # Backward-compatible plain text input: treat as required skills.
        return {
            "required_skills": parse_skills_csv(text),
            "preferred_skills": [],
        }


#job match function
def compute_job_match(user_skills, required_skills, preferred_skills):
    user_set = set(user_skills)
    required_set = set(required_skills)
    preferred_set = set(preferred_skills)

    matched_required = sorted(user_set & required_set)
    missing_required = sorted(required_set - user_set)
    matched_preferred = sorted(user_set & preferred_set)

    total_required = len(required_set)
    total_preferred = len(preferred_set)

    required_percent = round((len(matched_required) / total_required) * 100) if total_required else 0
    preferred_percent = round((len(matched_preferred) / total_preferred) * 100) if total_preferred else 0

    if total_required == 0 and total_preferred == 0:
        final_percent = 0
    elif total_required == 0:
        final_percent = preferred_percent
    elif total_preferred == 0:
        final_percent = required_percent
    else:
        final_percent = round((required_percent * 0.8) + (preferred_percent * 0.2))

    return {
        "percent": final_percent,
        "required_percent": required_percent,
        "preferred_percent": preferred_percent,
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "matched_required_count": len(matched_required),
        "total_required": total_required,
        "matched_preferred_count": len(matched_preferred),
        "total_preferred": total_preferred,
    }


def format_requirements_for_form(requirements_value):
    parsed = parse_requirements_value(requirements_value)
    return json.dumps(parsed)


def format_json_for_display(value):
    if value is None:
        return []

    parsed = value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return [text]

    if isinstance(parsed, dict):
        lines = []
        for key, item in parsed.items():
            if isinstance(item, list):
                item_text = ", ".join(str(x) for x in item) if item else "None"
            elif isinstance(item, dict):
                item_text = json.dumps(item)
            else:
                item_text = str(item)
            lines.append(f"{key}: {item_text}")
        return lines

    if isinstance(parsed, list):
        return [", ".join(str(x) for x in parsed)] if parsed else []

    return [str(parsed)]


def format_jobs_requirements_for_display(jobs):
    for job in jobs:
        job["requirements"] = format_requirements_for_form(job.get("requirements"))
        job["requirements_lines"] = format_json_for_display(job.get("requirements"))
    return jobs


def format_applications_interview_data_for_display(applications):
    for application in applications:
        application["interview_data_lines"] = format_json_for_display(application.get("interview_data"))
    return applications


def render_jobs_page_with_error(error_message):
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs ORDER BY job_id ASC")
    jobs = cursor.fetchall()
    cursor.close()
    connection.close()
    jobs = format_jobs_requirements_for_display(jobs)
    return render_template("jobs.html", jobs=jobs, error=error_message)


def validate_requirements_payload(payload):
    required_skills = payload.get("required_skills", [])
    preferred_skills = payload.get("preferred_skills", [])

    if not isinstance(required_skills, list) or not isinstance(preferred_skills, list):
        raise ValueError("required_skills and preferred_skills must both be arrays")

    if not required_skills:
        raise ValueError("At least one required skill is needed")

    return True

#normalizes url by adding https:// in front of url if missing
def normalize_url(value):
    if not value:
        return value
    value = value.strip()
    if not value:
        return value
    if value.startswith("www."):
        return "https://" + value
    if "://" not in value:
        return "https://" + value
    return value

#For linkedin url input, function checks if linkedin link is valid. Returns tuple (is_valid, error_message)
def validate_linkedin_url(url):
    if not url:
        return True, None
    
    url = url.strip().lower()
    
    if "linkedin.com" not in url:
        return False, "LinkedIn URL must contain 'linkedin.com'"
    
    if "/in/" not in url and "/company/" not in url:
        return False, "LinkedIn URL must contain '/in/' or '/company/' path"
    
    if "/in/" in url:
        after_path = url.split("/in/")[1].split("/")[0]
    else:
        after_path = url.split("/company/")[1].split("/")[0]
    
    if not after_path or not after_path.strip():
        return False, "LinkedIn URL must have a username or company name after /in/ or /company/"
    
    return True, None


@app.route('/')
def dashboard():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT COUNT(*) as count FROM applications')
    stats = cursor.fetchone()
    connection.close()
    return render_template('dashboard.html', stats=stats)


@app.route('/job-match', methods=["GET", "POST"])
def job_match():
    user_skills_input = ""
    user_skills = []
    matches = []

    if request.method == "POST":
        user_skills_input = request.form.get("skills", "")
        user_skills = parse_skills_csv(user_skills_input)

        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                j.job_id,
                j.job_title,
                j.requirements,
                c.company_name
            FROM jobs j
            LEFT JOIN companies c ON c.company_id = j.company_id
            ORDER BY j.job_id ASC
            """
        )
        jobs = cursor.fetchall()
        cursor.close()
        connection.close()

        for job in jobs:
            try:
                requirements = parse_requirements_value(job.get("requirements"))
            except ValueError:
                requirements = {"required_skills": [], "preferred_skills": []}

            score = compute_job_match(
                user_skills,
                requirements.get("required_skills", []),
                requirements.get("preferred_skills", []),
            )
            matches.append(
                {
                    "job_id": job["job_id"],
                    "job_title": job["job_title"],
                    "company_name": job.get("company_name") or "Unknown Company",
                    "percent": score["percent"],
                    "required_percent": score["required_percent"],
                    "preferred_percent": score["preferred_percent"],
                    "matched_required_count": score["matched_required_count"],
                    "total_required": score["total_required"],
                    "matched_preferred_count": score["matched_preferred_count"],
                    "total_preferred": score["total_preferred"],
                    "matched_required_skills": score["matched_required"],
                    "missing_required_skills": score["missing_required"],
                    "matched_preferred_skills": score["matched_preferred"],
                }
            )

        matches.sort(
            key=lambda m: (
                m["percent"],
                m["matched_required_count"],
                -m["total_required"],
                m["job_title"].lower(),
            ),
            reverse=True,
        )

    return render_template(
        "job_match.html",
        user_skills_input=user_skills_input,
        user_skills=user_skills,
        matches=matches,
    )



#COMPANIES
#Create
@app.route("/companies/create", methods = ["POST"])
def companies_create():
    company_name = request.form["company_name"]
    industry = request.form.get("industry")
    website = request.form.get("website")
    city = request.form.get("city")
    state = request.form.get("state")
    notes = request.form.get("notes")

    website = normalize_url(website)


    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        '''
        INSERT INTO companies (company_name, industry, website, city, state, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''',
        (company_name, industry, website, city, state, notes)
        )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("companies_read"))

#Read
@app.route("/companies", methods=["GET"])
def companies_read():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies ORDER BY company_id ASC")
    companies = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("companies.html", companies=companies)

#Update
@app.route("/companies/<int:company_id>/update", methods=["POST"])
def companies_update(company_id):
    company_name = request.form["company_name"]
    industry = request.form.get("industry")
    website = request.form.get("website")
    city = request.form.get("city")
    state = request.form.get("state")
    notes = request.form.get("notes")
    website = normalize_url(website)

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE companies
        SET company_name=%s, industry=%s, website=%s, city=%s, state=%s, notes=%s
        WHERE company_id=%s
        """,
        (company_name, industry, website, city, state, notes, company_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("companies_read"))


#Delete
@app.route("/companies/<int:company_id>/delete", methods=["POST"])
def companies_delete(company_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM companies WHERE company_id=%s", (company_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("companies_read"))

#JOBS
#Create
@app.route("/jobs/create", methods=["POST"])
def jobs_create():
    company_id = request.form.get("company_id")
    job_title = request.form.get("job_title")
    job_type = request.form.get("job_type")
    salary_min = request.form.get("salary_min")
    salary_max = request.form.get("salary_max")
    job_url = request.form.get("job_url")
    date_posted = request.form.get("date_posted")
    requirements = request.form.get("requirements")
    job_url = normalize_url(job_url)
    try:
        requirements_payload = parse_requirements_value(requirements)
        validate_requirements_payload(requirements_payload)
    except ValueError as ex:
        return render_jobs_page_with_error(str(ex))

    requirements_json = json.dumps(requirements_payload)
    
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        '''
        INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements_json)
        )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("jobs_read"))

#Read
@app.route("/jobs", methods=["GET"])
def jobs_read():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs ORDER BY job_id ASC")
    jobs = cursor.fetchall()
    cursor.close()
    connection.close()
    jobs = format_jobs_requirements_for_display(jobs)
    return render_template("jobs.html", jobs=jobs)

#Update
@app.route("/jobs/<int:job_id>/update", methods=["POST"])
def jobs_update(job_id):
    company_id = request.form.get("company_id")
    job_title = request.form.get("job_title")
    job_type = request.form.get("job_type")
    salary_min = request.form.get("salary_min")
    salary_max = request.form.get("salary_max")
    job_url = request.form.get("job_url")
    date_posted = request.form.get("date_posted")
    requirements = request.form.get("requirements")
    job_url = normalize_url(job_url)
    try:
        requirements_payload = parse_requirements_value(requirements)
        validate_requirements_payload(requirements_payload)
    except ValueError as ex:
        return render_jobs_page_with_error(str(ex))

    requirements_json = json.dumps(requirements_payload)

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE jobs
        SET company_id=%s, job_title=%s, job_type=%s, salary_min=%s, salary_max=%s, job_url=%s, date_posted=%s, requirements=%s
        WHERE job_id=%s
        """,
        (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements_json, job_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("jobs_read"))


#Delete
@app.route("/jobs/<int:job_id>/delete", methods=["POST"])
def jobs_delete(job_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM jobs WHERE job_id=%s", (job_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("jobs_read"))

#APPLICATIONS
#Create
@app.route("/applications/create", methods=["POST"])
def applications_create():
    job_id = request.form.get("job_id")
    application_date = request.form.get("application_date")
    status = request.form.get("status")
    resume_version = request.form.get("resume_version")
    cover_letter_sent = request.form.get("cover_letter_sent")
    interview_data = request.form.get("interview_data")
    
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        '''
        INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''',
        (job_id, application_date, status, resume_version, cover_letter_sent, interview_data)
        )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("applications_read"))

#Read
@app.route("/applications", methods=["GET"])
def applications_read():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applications ORDER BY application_id ASC")
    applications = cursor.fetchall()
    cursor.close()
    connection.close()
    applications = format_applications_interview_data_for_display(applications)
    return render_template("applications.html", applications=applications)

#Update
@app.route("/applications/<int:application_id>/update", methods=["POST"])
def applications_update(application_id):
    job_id = request.form.get("job_id")
    application_date = request.form.get("application_date")
    status = request.form.get("status")
    resume_version = request.form.get("resume_version")
    cover_letter_sent = request.form.get("cover_letter_sent")
    interview_data = request.form.get("interview_data")

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE applications
        SET job_id=%s, application_date=%s, status=%s, resume_version=%s, cover_letter_sent=%s, interview_data=%s
        WHERE application_id=%s
        """,
        (job_id, application_date, status, resume_version, cover_letter_sent, interview_data, application_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("applications_read"))


#Delete
@app.route("/applications/<int:application_id>/delete", methods=["POST"])
def applications_delete(application_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM applications WHERE application_id=%s", (application_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("applications_read"))

#CONTACTS
#Create
@app.route("/contacts/create", methods=["POST"])
def contacts_create():
    company_id = request.form.get("company_id")
    contact_name = request.form.get("contact_name")
    title = request.form.get("title")
    email = request.form.get("email")
    phone = request.form.get("phone")
    linkedin_url = request.form.get("linkedin_url")
    notes = request.form.get("notes")
    linkedin_url = normalize_url(linkedin_url)
    
    # Validate LinkedIn URL
    is_valid, error_msg = validate_linkedin_url(linkedin_url)
    if not is_valid:
        # Get all contacts to re-render the form
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM contacts ORDER BY contact_id ASC")
        contacts = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("contacts.html", contacts=contacts, error=error_msg)
    
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        '''
        INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''',
        (company_id, contact_name, title, email, phone, linkedin_url, notes)
        )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("contacts_read"))

#Read
@app.route("/contacts", methods=["GET"])
def contacts_read():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contacts ORDER BY contact_id ASC")
    contacts = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("contacts.html", contacts=contacts)

#Update
@app.route("/contacts/<int:contact_id>/update", methods=["POST"])
def contacts_update(contact_id):
    company_id = request.form.get("company_id")
    contact_name = request.form.get("contact_name")
    title = request.form.get("title")
    email = request.form.get("email")
    phone = request.form.get("phone")
    linkedin_url = request.form.get("linkedin_url")
    notes = request.form.get("notes")
    linkedin_url = normalize_url(linkedin_url)
    
    # Validate LinkedIn URL
    is_valid, error_msg = validate_linkedin_url(linkedin_url)
    if not is_valid:
        # Get all contacts to re-render the form
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM contacts ORDER BY contact_id ASC")
        contacts = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("contacts.html", contacts=contacts, error=error_msg)

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE contacts
        SET company_id=%s, contact_name=%s, title=%s, email=%s, phone=%s, linkedin_url=%s, notes=%s
        WHERE contact_id=%s
        """,
        (company_id, contact_name, title, email, phone, linkedin_url, notes, contact_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("contacts_read"))


#Delete
@app.route("/contacts/<int:contact_id>/delete", methods=["POST"])
def contacts_delete(contact_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM contacts WHERE contact_id=%s", (contact_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("contacts_read"))

if __name__ == '__main__':
    app.run(debug=True)