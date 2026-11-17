from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from crud import *
from datetime import datetime
import json, math

app = Flask(__name__, template_folder="templates", static_folder="static")

bootstrap = Bootstrap5(app)

# JSON

def parse_json(rows, field):
    """Turns a JSON column (which MySQL returns as a string) into a dict/list, for one row or a list of rows."""
    for row in rows if isinstance(rows, list) else [rows]:
        if row and isinstance(row.get(field), (str, bytes)):
            row[field] = json.loads(row[field])
    return rows

def read_requirements(req):
    """A job's requirements as a dict. Older rows stored only a list of required skills."""
    if isinstance(req, list):
        return {"required_skills": req}
    return req or {}

def split_list(text, sep=","):
    return [s.strip() for s in (text or "").split(sep) if s.strip()]

def build_requirements(form):
    return json.dumps({
        "required_skills": split_list(form.get("required_skills")),
        "preferred_skills": split_list(form.get("preferred_skills")),
        "education": form.get("education") or None,
        "experience_years": int(form["experience_years"]) if form.get("experience_years") else None,
        "remote_option": "remote_option" in form,
    })

def build_interview_data(form):
    return json.dumps({
        "interview_rounds": int(form["interview_rounds"]) if form.get("interview_rounds") else None,
        "interviewers": split_list(form.get("interviewers")),
        "technical_questions": split_list(form.get("technical_questions"), "\n"),
        "feedback": split_list(form.get("feedback"), "\n"),
        "next_steps": form.get("next_steps") or None,
        "rating": int(form["rating"]) if form.get("rating") else None,
    })


def normalize(raw_form):
    for key in raw_form.keys():
        value = raw_form[key]
        
        if value == '':
            raw_form[key] = None
            
    return raw_form
            

def evaluate_skills(skills):
    skills = [skill.lower() for skill in skills]
    
    jobs = parse_json(show_all_jobs(), 'requirements')

    report = []

    for job in jobs:
        if 'requirements' not in job or job['requirements'] is None:
            continue
        requirements = read_requirements(job['requirements'])

        # The match score only counts required skills; preferred skills are reported separately.
        skills_needed = requirements.get('required_skills') or []
        preferred_missing = [skill for skill in requirements.get('preferred_skills') or []
                             if skill.lower() not in skills]

        company = get_one_company(job['company_id'])
        
        title = f"{job['job_title']} at {company['company_name']}"
        
        if len(skills_needed) == 0:
            continue
        
        total = len(skills_needed)  
        

        matches = 0
        missing_arr = []
        
        for skill in skills_needed:
            if skill.lower() in skills:
                matches += 1
            else:
                missing_arr.append(skill)
                
        value = matches / total
        
        report.append({
            "title": title,
            "total": total,
            "matches": matches,
            "value": value,
            "percent": math.ceil(value * 100),
            "missing": missing_arr,
            "preferred_missing": preferred_missing,
            "remote_option": requirements.get('remote_option'),
            "experience_years": requirements.get('experience_years'),
            "education": requirements.get('education')
        })
        
    report.sort(key=lambda x: x['value'], reverse=True)
        
    # for i, job in enumerate(report):
    #     value = job["value"]
    #     percent = math.ceil(value * 100)
    #     print(f"{i + 1}. {job["title"]} - {percent}% ({job["matches"]}/{job["total"]})")
    #     if percent != 100:
    #         print(f"Missing: {job['missing']}")
    
    return report
            
@app.route("/")
def home_page():
    return render_template("dashboard.html",
                           applications=parse_json(show_all_applications(), 'interview_data'),
                           companies=show_all_companies(),
                           jobs=parse_json(show_all_jobs(), 'requirements'),
                           contacts=show_all_contacts())

@app.route("/apps")
def app_page():
    all_apps = parse_json(show_all_applications(), 'interview_data')
    
    return render_template("applications.html", applications=all_apps, jobs=show_all_jobs(), companies=show_all_companies())

@app.route("/company")
def company_page():
    companies = show_all_companies()
    
    return render_template("companies.html", companies=companies)

@app.route("/jobs")
def job_page():
    jobs = parse_json(show_all_jobs(), 'requirements')
    
    return render_template("jobs.html", jobs=jobs, companies=show_all_companies())

@app.route("/contacts")
def contact_page():
    contacts = show_all_contacts()
    
    return render_template("contacts.html", contacts=contacts, companies=show_all_companies())

@app.route("/job-match", methods=["GET", "POST"])
def job_match():
    body = request.args
    skills = body.get('skills').split(', ') if 'skills' in body else []
    report = evaluate_skills(skills)
    return render_template("job_match.html", report=report, skills=skills)

@app.route("/jobs/add", methods=["GET", "POST"])
def add_job():
    if request.method == "GET":
        return render_template('job_form.html', companies=show_all_companies())
    
    body = normalize(dict(request.form))

    raw = (body['company_id'] if 'company_id' in body else None, 
               body['job_title'] if 'job_title' in body else None, 
               body['job_description'] if 'job_description' in body else None, 
               body['salary_min'] if 'salary_min' in body else None, 
               body['salary_max'] if 'salary_max' in body else None, 
               body['job_type'] if 'job_type' in body else None, 
               body['posting_url'] if 'posting_url' in body else None, 
               body['date_posted'] if 'date_posted' in body else None, 
               body['is_active'] if 'is_active' in body else 0,
               build_requirements(body),
               body['created_at'] if 'created_at' in body else datetime.now())
    
    create_job(raw)
    
    return redirect(url_for('job_page'))

@app.route("/company/add", methods=["GET", "POST"])
def add_company():
    if request.method == "GET":
        return render_template("company_form.html")
    
    body = normalize(dict(request.form))
    
    
    
    raw = (body['company_name'] if 'company_name' in body else None, 
        body['industry'] if 'industry' in body else None,
        body['website'] if 'website' in body else None,
        body['city'] if 'city' in body else None,
        body['state'] if 'state' in body else None,
        body['notes'] if 'notes' in body else None,
        body['created_at'] if 'created_at' in body else datetime.now().isoformat())
    
    create_company(raw)
    
    return redirect(url_for('company_page'))
        
    
@app.route("/contacts/add", methods=["GET", "POST"])
def add_contact():
    if request.method == "GET":
        return render_template("contact_form.html", companies=show_all_companies())
    
    body = normalize(dict(request.form))
    
    raw = ( body['company_id'] if 'company_id' in body else None,
                body['first_name'] if 'first_name' in body else None,
                body['last_name'] if 'last_name' in body else None,
                body['email'] if 'email' in body else None,
                body['phone'] if 'phone' in body else None,
                body['job_title'] if 'job_title' in body else None,
                body['linkedin_url'] if 'linkedin_url' in body else None,
                body['notes'] if 'notes' in body else None,
                body['created_at'] if 'created_at' in body else datetime.now())
    
    create_contact(raw)
    
    return redirect(url_for('contact_page'))
    
@app.route("/apps/add", methods=["GET", "POST"])
def add_app():
    if request.method == "GET":
        return render_template("application_form.html", jobs=show_all_jobs(), companies=show_all_companies())
    
    body = normalize(dict(request.form))
    
    raw = (body['job_id'] if 'job_id' in body else None, 
                body['application_date'] if 'application_date' in body else datetime.now().isoformat(),
                body['status'] if 'status' in body else None,
                body['resume_version'] if 'resume_version' in body else None,
                body['cover_letter_sent'] if 'cover_letter_sent' in body else 0,
                body['response_date'] if 'response_date' in body else None,
                body['interview_date'] if 'interview_date' in body else None,
                build_interview_data(body),
                body['notes'] if 'notes' in body else None,
                body['created_at'] if 'created_at' in body else datetime.now().isoformat())
    
    create_application(raw)
        
    return redirect(url_for('app_page'))

@app.route("/jobs/<int:job_id>/delete", methods=["POST"])
def delete_job_route(job_id):
    try:
        delete_job(job_id)
    except Exception as e:
        print("FAILED")
    return redirect(url_for("job_page"))
        
@app.route("/apps/<int:app_id>/delete", methods=["POST"])
def delete_app_route(app_id):
    try:
        delete_application(app_id)
    except Exception as e:
        print("FAILED")

    return redirect(url_for("app_page"))
        
@app.route("/company/<int:company_id>/delete", methods=["POST"])
def delete_company_route(company_id):
    try:
        delete_company(company_id)
    except Exception as e:
        print("FAILED")
    return redirect(url_for("company_page"))
        
@app.route("/contacts/<int:contact_id>/delete", methods=["POST"])
def delete_contact_route(contact_id):
    try:
        delete_contact(contact_id)
    except Exception as e:
        print("FAILED")
    return redirect(url_for("contact_page"))
        
@app.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
def edit_job_page(job_id):
    if request.method == "GET":
        job_details = parse_json(get_one_job(job_id), 'requirements')
        return render_template("job_form.html", job=job_details, companies=show_all_companies())
    
    body = normalize(dict(request.form))
    
    print(body)
    
    raw = (body['company_id'] if 'company_id' in body else None, 
           body['job_title'] if 'job_title' in body else None, 
           body['job_description'] if 'job_description' in body else None, 
           body['salary_min'] if 'salary_min' in body else None, 
           body['salary_max'] if 'salary_max' in body else None, 
           body['job_type'] if 'job_type' in body else None, 
           body['posting_url'] if 'posting_url' in body else None, 
           body['date_posted'] if 'date_posted' in body else None, 
           body['is_active'] if 'is_active' in body else 0,
           build_requirements(body),
           job_id)
    
    update_job(raw)
    
    return redirect(url_for('job_page'))
    
    
@app.route("/contacts/<int:contact_id>/edit", methods=["GET", "POST"])
def edit_contact_page(contact_id):
    if request.method == "GET":
        contact_details = get_one_contact(contact_id)
        return render_template("contact_form.html", contact=contact_details, companies=show_all_companies())
    
    body = normalize(dict(request.form))
        
    raw = ( body['company_id'] if 'company_id' in body else None,
            body['first_name'] if 'first_name' in body else None,
            body['last_name'] if 'last_name' in body else None,
            body['email'] if 'email' in body else None,
            body['phone'] if 'phone' in body else None,
            body['job_title'] if 'job_title' in body else None,
            body['linkedin_url'] if 'linkedin_url' in body else None,
            body['notes'] if 'notes' in body else None,
            contact_id)
    
    update_contact(raw)
    
    return redirect(url_for('contact_page'))
    
@app.route("/apps/<int:app_id>/edit", methods=["GET", "POST"])
def edit_application_page(app_id):
    if request.method == "GET":
        app_details = parse_json(get_one_application(app_id), 'interview_data')
        return render_template("application_form.html", application=app_details, jobs=show_all_jobs(), companies=show_all_companies())
    
    body = normalize(dict(request.form))
    
    raw = (body['job_id'] if 'job_id' in body else None, 
            body['application_date'] if 'application_date' in body else datetime.now().isoformat(),
            body['status'] if 'status' in body else None,
            body['resume_version'] if 'resume_version' in body else None,
            body['cover_letter_sent'] if 'cover_letter_sent' in body else 0,
            body['response_date'] if 'response_date' in body else None,
            body['interview_date'] if 'interview_date' in body else None,
            build_interview_data(body),
            body['notes'] if 'notes' in body else None,
            app_id)
    
    update_application(raw)
    
    return redirect(url_for('app_page'))
    
@app.route("/company/<int:company_id>/edit", methods=["GET", "POST"])
def edit_company_page(company_id):
    if request.method == "GET":
        company_details = get_one_company(company_id)
        return render_template("company_form.html", company=company_details)
    
    body = normalize(dict(request.form))
    
    raw = (body['company_name'] if 'company_name' in body else None, 
            body['industry'] if 'industry' in body else None,
            body['website'] if 'website' in body else None,
            body['city'] if 'city' in body else None,
            body['state'] if 'state' in body else None,
            body['notes'] if 'notes' in body else None,
            company_id)
    
    update_company(raw)
    
    return redirect(url_for('company_page'))
    
    
    

if __name__ == '__main__':
    app.run(debug=True)
    engine.close()