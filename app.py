from flask import Flask, jsonify, request
from db import grab_all, grab_one, create_entry, engine
from datetime import datetime

# Database Set-Up

app = Flask(__name__)

# Create

@app.route("/api/applications", methods=["POST"])
def create_application():
    body = request.get_json()
        
    raw = (body['job_id'] if body['job_id'] else None, 
            body['application_date'] if body['application_date'] else None,
            body['status'] if body['status'] else None,
            body['resume_version'] if body['resume_version'] else None,
            body['cover_letter_sent'] if body['cover_letter_sent'] else None,
            body['response_date'] if body['response_date'] else None,
            body['interview_date'] if body['interview_date'] else None,
            body['notes'] if body['notes'] else None,
            body['created_at'] if body['created_at'] else datetime.now())
    
    try:
        create_entry("applications", raw)
    except Exception as e:
        return jsonify(str(e)), 500
    else:
        return jsonify({"msg": "Entry saved"}), 200
    
@app.route("/api/contacts", methods=["POST"])
def create_contact():
    body = request.get_json()
        
    raw = ( body['company_id'] if body['company_id'] else None,
            body['first_name'] if body['first_name'] else None,
            body['last_name'] if body['last_name'] else None,
            body['email'] if body['email'] else None,
            body['phone'] if body['phone'] else None,
            body['job_title'] if body['job_tile'] else None,
            body['linkedin_url'] if body['linkedin_url'] else None,
            body['notes'] if body['notes'] else None,
            body['created_at'] if body['created_at'] else datetime.now())
    
    try:
        create_entry("jobs", raw)
    except Exception as e:
        return jsonify(str(e)), 500
    else:
        return jsonify({"msg": "Entry saved"}), 200

@app.route("/api/jobs", methods=["POST"])
def create_job():
    body = request.get_json()
    
    raw = (body['company_id'] if body['company_id'] else None, 
           body['job_title'] if body['job_title'] else None, 
           body['job_description'] if body['job_description'] else None, 
           body['salary_min'] if body['salary_min'] else None, 
           body['salary_max'] if body['salary_max'] else None, 
           body['job_type'] if body['job_type'] else None, 
           body['posting_url'] if body['posting_url'] else None, 
           body['date_posted'] if body['date_posted'] else None, 
           body['is_active'] if body['is_active'] else None, 
           body['notes'] if body['notes'] else None, 
           body['created_at'] if body['created_at'] else datetime.now())
    
    try:
        create_entry("jobs", raw)
    except Exception as e:
        return jsonify(str(e)), 500
    else:
        return jsonify({"msg": "Entry saved"}), 200
    

@app.route("/api/companies", methods=["POST"])
def create_company():
    body = request.get_json()
        
    raw = (body['company_name'] if body['company_name'] else None, 
            body['industry'] if body['industry'] else None,
            body['website'] if body['website'] else None,
            body['city'] if body['city'] else None,
            body['notes'] if body['notes'] else None,
            body['createdy_at'] if body['created_at'] else datetime.now())
        
    try:
        create_entry("companies", raw)
    except Exception as e:
        return jsonify(str(e)), 500
    else:
        return jsonify({"msg": "Entry saved"}), 200

# Read

@app.route("/api/applications")
def show_all_applications():
    try:
        entities = grab_all('applications')
    except Exception as e:
        return jsonify(str(e)), 500
    
    return jsonify(entities), 200

@app.route("/api/jobs")
def show_all_jobs():
    try:
        entities = grab_all('jobs')
    except Exception as e:
        return jsonify(str(e)), 500
    
    return jsonify(entities), 200

@app.route("/api/contacts")
def show_all_contacts():
    try:
        entities = grab_all('contacts')
    except Exception as e:
        return jsonify(str(e)), 500
    
    return jsonify(entities), 200

@app.route("/api/companies")
def show_all_companies():
    try:
        entities = grab_all('companies')
    except Exception as e:
        return jsonify(str(e)), 500
    
    return jsonify(entities), 200


@app.route("/api/applications/<int:app_id>")
def get_one_application(app_id):
    try:
        entity = grab_one("applications", app_id)
    except Exception as e:
        return jsonify(str(e)), 500
    
    if not entity:
        return jsonify({"msg": "Not found"}), 400
    
    return jsonify(entity), 200

@app.route("/api/jobs/<int:job_id>")
def get_one_job(job_id):
    try:
        entity = grab_one("jobs", job_id)
    except Exception as e:
        return jsonify(str(e)), 500
    
    if not entity:
        return jsonify({"msg": "Not found"}), 400
    
    return jsonify(entity), 200

@app.route("/api/companies/<int:company_id>")
def get_one_company(company_id):
    try:
        entity = grab_one("companies", company_id)
    except Exception as e:
        return jsonify(str(e)), 500
    
    if not entity:
        return jsonify({"msg": "Not found"}), 400
    
    return jsonify(entity), 200

@app.route("/api/contacts/<int:contact_id>")
def get_one_contact(contact_id):
    try:
        entity = grab_one("contacts", contact_id)
    except Exception as e:
        return jsonify(str(e)), 500
    
    if not entity:
        return jsonify({"msg": "Not found"}), 400
    
    return jsonify(entity), 200

# Update

# Delete

if __name__ == '__main__':
    app.run()
    
    
engine.close()