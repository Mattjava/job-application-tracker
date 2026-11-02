from flask import Flask, jsonify
from dotenv import load_dotenv
import mysql.connector, os

# Database Set-Up

load_dotenv()

config = {
    "host": "localhost",
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": "job_tracker"
}

try:
    engine = mysql.connector.connect(**config)
except Exception:
    raise Exception("Failed to connect to database")

# Boilerplate code

def grab_all(table_name):
    try:
        cursor = engine.cursor(dictionary=True)
        
        cursor.execute(f"SELECT * FROM {table_name}")
        
        return cursor.fetchall()
    except Exception as e:
        if cursor:
            cursor.close()
        raise Exception(f'Failed to connect to database: {e}')
    finally:
        if cursor:
            cursor.close()
        
def grab_one(table_name, id):
    keys = {
        "contacts": "contact_id",
        "companies": "company_id",
        "jobs": "job_id",
        "applications": "application_id"
    }
    
    try:
        cursor = engine.cursor(dictionary=True)
        query = f"SELECT * FROM {table_name} where {keys[table_name]} = %s"
        cursor.execute(query, (id,))
        value = cursor.fetchone()
        cursor.close()
        return value
    except Exception as e:
        if cursor:
            cursor.close()
            
        raise Exception(f"Database error: {e}")

app = Flask(__name__)

# Create

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