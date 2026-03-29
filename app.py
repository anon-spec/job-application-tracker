from flask import Flask, render_template, redirect, request, url_for
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host ='localhost', user='root',
        password='YOUR_PASSWORD', database = 'job_application_tracker'
    )


@app.route('/')
def dashboard():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT COUNT(*) as count FROM applications')
    stats = cursor.fetchone()
    connection.close()
    return render_template('dashboard.html', stats=stats)



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
    return redirect(url_for("companies_list"))

#Read
@app.route("/companies", methods=["GET"])
def companies_read():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies ORDER BY company_id DESC")
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
    return redirect(url_for("companies_list"))


#Delete
@app.route("/companies/<int:company_id>/delete", methods=["POST"])
def companies_delete(company_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM companies WHERE company_id=%s", (company_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("companies_list"))

#JOBS
#Create
@app.route("/jobs/create", methods=["POST"])
def jobs_create():
    company_id = request.form["company_id"]
    job_title = request.form.get("job_title")
    job_type = request.form.get("job_type")
    salary_min = request.form.get("salary_min")
    salary_max = request.form.get("salary_max")
    job_url = request.form.get("job_url")
    date_posted = request.form.get("date_posted")
    requirements = request.form.get("requirements")
    
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        '''
        INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements)
        )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("jobs_list"))

#Read
@app.route("/jobs", methods=["GET"])
def jobs_read():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs ORDER BY job_id DESC")
    jobs = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("jobs.html", jobs=jobs)

#Update
@app.route("/jobs/<int:job_id>/update", methods=["POST"])
def jobs_update(job_id):
    company_id = request.form["company_id"]
    job_title = request.form.get("job_title")
    job_type = request.form.get("job_type")
    salary_min = request.form.get("salary_min")
    salary_max = request.form.get("salary_max")
    job_url = request.form.get("job_url")
    date_posted = request.form.get("date_posted")
    requirements = request.form.get("requirements")

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE jobs
        SET company_id=%s, job_title=%s, job_type=%s, salary_min=%s, salary_max=%s, job_url=%s, date_posted=%s, requirements=%s
        WHERE job_id=%s
        """,
        (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements, job_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("jobs_list"))


#Delete
@app.route("/jobs/<int:job_id>/delete", methods=["POST"])
def jobs_delete(job_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM jobs WHERE job_id=%s", (job_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("jobs_list"))

#APPLICATIONS
#Create
@app.route("/applications/create", methods=["POST"])
def applications_create():
    job_id = request.form["job_id"]
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
    return redirect(url_for("applications_list"))

#Read
@app.route("/applications", methods=["GET"])
def applications_read():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applications ORDER BY application_id DESC")
    applications = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("applications.html", applications=applications)

#Update
@app.route("/applications/<int:application_id>/update", methods=["POST"])
def applications_update(application_id):
    job_id = request.form["job_id"]
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
    return redirect(url_for("applications_list"))


#Delete
@app.route("/applications/<int:application_id>/delete", methods=["POST"])
def applications_delete(application_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM applications WHERE application_id=%s", (application_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("applications_list"))

#CONTACTS
#Create
@app.route("/contacts/create", methods=["POST"])
def contacts_create():
    company_id = request.form["company_id"]
    contact_name = request.form.get("contact_name")
    title = request.form.get("title")
    email = request.form.get("email")
    phone = request.form.get("phone")
    linkedin_url = request.form.get("linkedin_url")
    
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        '''
        INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''',
        (company_id, contact_name, title, email, phone, linkedin_url)
        )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("contacts_list"))

#Read
@app.route("/contacts", methods=["GET"])
def contacts_read():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contacts ORDER BY contact_id DESC")
    contacts = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("contacts.html", contacts=contacts)

#Update
@app.route("/contacts/<int:contact_id>/update", methods=["POST"])
def contatcs_update(contact_id):
    company_id = request.form["company_id"]
    contact_name = request.form.get("contact_name")
    title = request.form.get("title")
    email = request.form.get("email")
    phone = request.form.get("phone")
    linkedin_url = request.form.get("linkedin_url")

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE contacts
        SET company_id=%s, contact_name=%s, title=%s, email=%s, phone=%s, linkedin_url=%s
        WHERE contact_id=%s
        """,
        (company_id, contact_name, title, email, phone, linkedin_url, contact_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("contacts_list"))


#Delete
@app.route("/contacts/<int:contact_id>/delete", methods=["POST"])
def contacts_delete(contact_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM contacts WHERE contact_id=%s", (contact_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("contacts_list"))

if __name__ == '__main__':
    app.run(debug=True)