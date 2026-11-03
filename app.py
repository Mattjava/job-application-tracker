from flask import Flask, jsonify, request
from db import grab_all, grab_one, create_entry, delete_entry, engine
from datetime import datetime

# Database Set-Up

app = Flask(__name__)

# Create

@app.route("/api/applications", methods=["POST"])
def create_application():
    body = request.get_json()
        
    raw = (body['job_id'] if 'job_id' in body else None, 
            body['application_date'] if 'application_date' in body else datetime.now().isoformat(),
            body['status'] if 'status' in body else None,
            body['resume_version'] if 'resume_version' in body else None,
            body['cover_letter_sent'] if 'cover_letter_sent' in body else 0,
            body['response_date'] if 'response_date' in body else None,
            body['interview_date'] if 'interview_date' in body else None,
            body['notes'] if 'notes' in body else None,
            body['created_at'] if 'created_at' in body else datetime.now().isoformat())
    
    try:
        create_entry("applications", raw)
    except Exception as e:
        return jsonify(str(e)), 500
    else:
        return jsonify({"msg": "Entry saved"}), 200
    
@app.route("/api/contacts", methods=["POST"])
def create_contact():
    body = request.get_json()
        
    raw = ( body['company_id'] if 'company_id' in body else None,
            body['first_name'] if 'first_name' in body else None,
            body['last_name'] if 'last_name' in body else None,
            body['email'] if 'email' in body else None,
            body['phone'] if 'phone' in body else None,
            body['job_title'] if 'job_title' in body else None,
            body['linkedin_url'] if 'linkedin_url' in body else None,
            body['notes'] if 'notes' in body else None,
            body['created_at'] if 'created_at' in body else datetime.now())
    
    try:
        create_entry("contacts", raw)
    except Exception as e:
        return jsonify(str(e)), 500
    else:
        return jsonify({"msg": "Entry saved"}), 200

@app.route("/api/jobs", methods=["POST"])
def create_job():
    body = request.get_json()
    
    
    raw = (body['company_id'] if 'company_id' in body else None, 
           body['job_title'] if 'job_title' in body else None, 
           body['job_description'] if 'job_description' in body else None, 
           body['salary_min'] if 'salary_min' in body else None, 
           body['salary_max'] if 'salary_max' in body else None, 
           body['job_type'] if 'job_type' in body else None, 
           body['posting_url'] if 'posting_url' in body else None, 
           body['date_posted'] if 'date_posted' in body else None, 
           body['is_active'] if 'is_active' in body else 0, 
           body['created_at'] if 'created_at' in body else datetime.now())
    
    print(raw)
    
    try:
        create_entry("jobs", raw)
    except Exception as e:
        return jsonify(str(e)), 500
    else:
        return jsonify({"msg": "Entry saved"}), 200
    

@app.route("/api/companies", methods=["POST"])
def create_company():
    body = request.get_json()
        
    raw = (body['company_name'] if 'company_name' in body else None, 
            body['industry'] if 'industry' in body else None,
            body['website'] if 'website' in body else None,
            body['city'] if 'city' in body else None,
            body['state'] if 'state' in body else None,
            body['notes'] if 'notes' in body else None,
            body['created_at'] if 'created_at' in body else datetime.now().isoformat())
        
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

@app.route("/api/applications/<int:app_id>",  methods=["DELETE"])
def delete_application(app_id):
    try:
        entity = delete_entry("applications", app_id)
    except Exception as e:
        return jsonify(str(e)), 500
    
    if not entity:
        return jsonify({"msg": "Not found"}), 400
    
    return jsonify(entity), 200

@app.route("/api/jobs/<int:job_id>",  methods=["DELETE"])
def delete_job(job_id):
    try:
        entity = delete_entry("jobs", job_id)
    except Exception as e:
        return jsonify(str(e)), 500
    
    if not entity:
        return jsonify({"msg": "Not found"}), 400
    
    return jsonify(entity), 200

@app.route("/api/companies/<int:company_id>",  methods=["DELETE"])
def delete_company(company_id):
    try:
        entity = delete_entry("companies", company_id)
    except Exception as e:
        return jsonify(str(e)), 500
    
    if not entity:
        return jsonify({"msg": "Not found"}), 400
    
    return jsonify(entity), 200

@app.route("/api/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    try:
        entity = delete_entry("contacts", contact_id)
    except Exception as e:
        return jsonify(str(e)), 500
    
    if not entity:
        return jsonify({"msg": "Not found"}), 400
    
    return jsonify(entity), 200

if __name__ == '__main__':
    app.run()
    engine.close()