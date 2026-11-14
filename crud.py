from database import grab_all, grab_one, create_entry, update_entry, delete_entry, engine


# Create


def create_application(raw):
    try:
        create_entry("applications", raw)
    except Exception as e:
        raise e
    else:
        return True

def create_contact(raw):
    try:
        create_entry("contacts", raw)
    except Exception as e:
            raise e
    else:
        return True


def create_job(raw):
    try:
        create_entry("jobs", raw)
    except Exception as e:
            raise e
    else:
        return True
    


def create_company(raw):
    try:
        create_entry("companies", raw)
    except Exception as e:
            raise e
    else:
        return True

# Read


def show_all_applications():
    try:
        entities = grab_all('applications')
    except Exception as e:
            raise e
        
    return entities


def show_all_jobs():
    try:
        entities = grab_all('jobs')
    except Exception as e:
            raise e
        
    return entities


def show_all_contacts():
    try:
        entities = grab_all('contacts')
    except Exception as e:
            raise e
        
    return entities


def show_all_companies():
    try:
        entities = grab_all('companies')
    except Exception as e:
        raise e
    
    return entities



def get_one_application(app_id):
    try:
        entity = grab_one("applications", app_id)
    except Exception as e:
            raise e
        
    if not entity:
        return None
    
    return entity


def get_one_job(job_id):
    try:
        entity = grab_one("jobs", job_id)
    except Exception as e:
            raise e
    
    if not entity:
        return None
    
    return entity

def get_one_company(company_id):
    try:
        entity = grab_one("companies", company_id)
    except Exception as e:
        raise e
        
    if not entity:
            return None
        
    return entity


def get_one_contact(contact_id):
    try:
        entity = grab_one("contacts", contact_id)
    except Exception as e:
        raise e
    
    if not entity:
        return None
    
    return entity

# Update


def update_application(raw):    
    try:
        update_entry("applications", raw)
    except Exception as e:
        raise e
    else:
        return True
    

def update_contact(raw):    
    try:
        update_entry("contacts", raw)
    except Exception as e:
        raise e
    else:
        return True


def update_job(raw):
    try:
        update_entry("jobs", raw)
    except Exception as e:
        raise e
    else:
        return True
    


def update_company(raw):
    try:
        update_entry("companies", raw)
    except Exception as e:
        raise e
    else:
        return True

# Delete
def delete_application(app_id):
    try:
        entity = delete_entry("applications", app_id)
    except Exception as e:
        raise e
    
    if not entity:
        return None
    
    return entity

def delete_job(job_id):
    try:
        entity = delete_entry("jobs", job_id)
    except Exception as e:
        raise e
    
    if not entity:
        return None
    
    return entity

def delete_company(company_id):
    try:
        entity = delete_entry("companies", company_id)
    except Exception as e:
        raise e
    
    if not entity:
        return None
    
    return entity

def delete_contact(contact_id):
    try:
        entity = delete_entry("contacts", contact_id)
    except Exception as e:
        raise e
    
    if not entity:
        return None
    
    return entity

