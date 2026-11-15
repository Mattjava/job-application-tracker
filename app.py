from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from crud import *
from datetime import datetime
import json, math

app = Flask(__name__, template_folder="templates", static_folder="static")

bootstrap = Bootstrap5(app)

def normalize(raw_form):
    for key in raw_form.keys():
        value = raw_form[key]
        
        if value == '':
            raw_form[key] = None
        elif key == "requirements":
            value = value.split(', ')
            raw_form[key] = json.dumps(value)
            
    return raw_form
            

def evaluate_skills(skills):
    skills = [skill.lower() for skill in skills]
    
    jobs = show_all_jobs()
    
    report = []
    
    for job in jobs:
        if 'requirements' not in job or job['requirements'] is None:
            continue
        req = json.loads(job['requirements'])
        
        company = get_one_company(job['company_id'])
        
        title = f"{job['job_title']} at {company['company_name']}"
        
        if len(req) == 0:
            continue
        
        total = len(req)  
        

        matches = 0
        missing_arr = []
        
        for skill in req:
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
            "missing": missing_arr
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
                           applications=show_all_applications(),
                           companies=show_all_companies(),
                           jobs=show_all_jobs(),
                           contacts=show_all_contacts())
            
@app.route("/apps")
def app_page():
    all_apps = show_all_applications()
    
    return render_template("applications.html", applications=all_apps, jobs=show_all_jobs(), companies=show_all_companies())

@app.route("/company")
def company_page():
    companies = show_all_companies()
    
    return render_template("companies.html", companies=companies)

@app.route("/jobs")
def job_page():
    jobs = show_all_jobs()
    
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
               body['requirements'] if 'requirements' in body else None,
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
        return render_template("application_form.html", jobs=show_all_jobs())
    
    body = normalize(dict(request.form))
    
    raw = (body['job_id'] if 'job_id' in body else None, 
                body['application_date'] if 'application_date' in body else datetime.now().isoformat(),
                body['status'] if 'status' in body else None,
                body['resume_version'] if 'resume_version' in body else None,
                body['cover_letter_sent'] if 'cover_letter_sent' in body else 0,
                body['response_date'] if 'response_date' in body else None,
                body['interview_date'] if 'interview_date' in body else None,
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
        job_details = get_one_job(job_id)
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
           body['requirements'] if 'requirements' in body else None,
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
        app_details = get_one_application(app_id)
        return render_template("application_form.html", application=app_details, jobs=show_all_jobs())
    
    body = normalize(dict(request.form))
    
    raw = (body['job_id'] if 'job_id' in body else None, 
            body['application_date'] if 'application_date' in body else datetime.now().isoformat(),
            body['status'] if 'status' in body else None,
            body['resume_version'] if 'resume_version' in body else None,
            body['cover_letter_sent'] if 'cover_letter_sent' in body else 0,
            body['response_date'] if 'response_date' in body else None,
            body['interview_date'] if 'interview_date' in body else None,
            body['notes'] if 'notes' in body else None,
            app_id)
    
    update_application(raw)
    
    return redirect(url_for('app_page'))
    
@app.route("/company/<int:company_id>/edit", methods=["GET", "POST"])
def edit_company_page(company_id):
    if request.method == "GET":
        company_details = get_one_company(company_id)
        return render_template("job_form.html", company=company_details)
    
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