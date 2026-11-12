from flask import Flask, jsonify, render_template
from crud import *
from datetime import datetime
import json, math

app = Flask(__name__, template_folder="templates")

def evaluate_skills(skills):
    print(f"Your skills: {skills}\n")
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
        
        report.append({
            "title": title,
            "total": total,
            "matches": matches,
            "value": matches / total,
            "missing": missing_arr
        })
        
    report.sort(key=lambda x: x['value'], reverse=True)
        
    for i, job in enumerate(report):
        value = job["value"]
        percent = math.ceil(value * 100)
        print(f"{i + 1}. {job["title"]} - {percent}% ({job["matches"]}/{job["total"]})")
        if percent != 100:
            print(f"Missing: {job['missing']}")
            
@app.route("/")
def home_page():
    return render_template("dashboard.html")
            
@app.route("/apps")
def app_page():
    apps = show_all_applications()
    
    print(apps)
    
    return render_template("applications.html")

@app.route("/company")
def company_page():
    companies = show_all_companies()
    
    print(companies)
    
    return render_template("companies.html")

@app.route("/jobs")
def job_page():
    jobs = show_all_jobs()
    
    print(jobs)
    
    return render_template("jobs.html")

@app.route("/contacts")
def contact_page():
    contacts = show_all_contacts()
    
    print(contacts)
    
    return render_template("contacts.html")

@app.route("/job-match")
def test_func():
    evaluate_skills(['Python', 'HTML', 'SQL'])
    return render_template("job_match.html")
    

if __name__ == '__main__':
    app.run(debug=True)
    engine.close()