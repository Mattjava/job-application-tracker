from dotenv import load_dotenv
import mysql.connector, os

load_dotenv()

config = {
    "host": "localhost",
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": "job_tracker"
}

TABLE_NAME = ["companies", "jobs", "contacts", "applications"]

try:
    engine = mysql.connector.connect(**config)
except Exception:
    raise Exception("Failed to connect to database")

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

def create_entry(table_name: str, data: tuple):
    queries = {
        "applications": "INSERT INTO applications(job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
        "jobs": "INSERT INTO jobs(company_id, job_title, job_description, salary_min, salary_max, job_type, posting_url, date_posted, is_active, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
        "contacts": "INSERT INTO contacts(company_id, first_name, last_name, email, phone, job_title, linkedin_url, notes, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);",
        "companies": "INSERT INTO companies(company_name, industry, website, city, state, notes, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    }
    
    if table_name not in queries:
        raise Exception("Invalid table name")
    
    try:
        cursor = engine.cursor()
        query = queries[table_name]
        
        cursor.execute(query, data)
        
        engine.commit()
        
        cursor.close()
        
        return True
    except Exception as e:
        cursor.close()
        raise Exception(f"Database error: {e}")
    
def update_entry(table_name: str, data: tuple):    
    queries = {
        "contacts": "UPDATE contacts SET company_id = %s, first_name = %s, last_name = %s, email = %s, phone = %s, job_title = %s, linkedin_url = %s, notes = %s WHERE contact_id = %s",
        "companies": "UPDATE companies SET company_name = %s, industry = %s, website = %s, city = %s, state = %s, notes = %s WHERE company_id = %s",
        "jobs": "UPDATE jobs SET company_id = %s, job_title = %s, job_description = %s, salary_min = %s, salary_max = %s, job_type = %s, posting_url = %s, date_posted = %s, is_active = %s WHERE job_id = %s",
        "applications": "UPDATE applications SET job_id = %s, application_date = %s, status = %s, resume_version = %s, cover_letter_sent = %s, response_date = %s, interview_date = %s, notes = %s WHERE application_id = %s"
    }
    
    try:
        cursor = engine.cursor()
        
        query = queries[table_name]
        
        cursor.execute(query, data)
        engine.commit()
        cursor.close()
    except Exception as e:
        cursor.close()
        raise Exception(f"Database error: {e}")    
    

def delete_entry(table_name: str, id: int):
    keys = {
        "contacts": "contact_id",
        "companies": "company_id",
        "jobs": "job_id",
        "applications": "application_id"
    }
    
    try:
        cursor = engine.cursor(dictionary=True)
        query = f"DELETE * FROM {table_name} where {keys[table_name]} = %s"
        cursor.execute(query, (id,))
        cursor.close()
        return "Successfully deleted"
    except Exception as e:
        if cursor:
            cursor.close()
            
        raise Exception(f"Database error: {e}")