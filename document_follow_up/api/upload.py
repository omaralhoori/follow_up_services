import frappe
import os
import random

def upload_data():
    uploaded_files = frappe.request.files.keys()#['filedata'].read()#base64.b64decode(frappe.form_dict.filedata)    
    files = []
    print(frappe.request.files.keys())
    print(frappe.request.files)
    for key in uploaded_files:
        site_path = frappe.local.site + "/public/files/"
        rand= random.randrange(111111, 999999, 6)
        file_name =  str(rand) + "_" + frappe.request.files[key].filename
        save_file(site_path,file_name, frappe.request.files[key].read())
        files.append("/files/" + file_name )
    return files
    
def save_file(image_path,image_name, image_content):
    # create_path(image_path)
    with open(os.path.join( image_path,image_name), "wb") as f:
        f.write(image_content)
        
def create_path(full_path):
	isExist = os.path.exists(full_path)
	if not isExist:
		os.makedirs(full_path)

def insert_data(data):
    fields = get_data_fields(data)
    if not fields: return
    doc = frappe.get_doc(fields)

    row = doc.append("title")
    row.data = data['name']
    row.t_language = 'ar'
    row = doc.append("title")
    row.data = data['name']
    row.t_language = 'en'
    row = doc.append("title")
    row.data = data['name']
    row.t_language = 'tr'
    try:
        row = doc.append("description")
        row.small_text = '-'
        row.t_language = 'ar'
        row = doc.append("description")
        row.small_text = '-'
        row.t_language = 'en'
        row = doc.append("description")
        row.small_text = '-'
        row.t_language = 'tr'
    except:
        pass
    doc.save(ignore_permissions=True)
    return doc

def get_data_fields(data):
    doctype = get_data_doctype(data['type'])
    if not doctype: return
    fields = {
        "doctype": doctype,
        "city": data['city'],
        "location": data['location']
    }
    if data['type'] == 'cami':
        fields = {
            **fields,
        }
    else:
        fields = {
            **fields,
            "slug": data['city'].replace(" ", "-") + "-" + data['name'].replace(" ", "-"),
            "stars": data['rate'],
            "likes": data['likes']
        }
    return fields

def get_data_doctype(data_type):
    types = {
        "area": "Tourism Area",
        "eczane":  "Tourism Hospital",
        "Lokanta": "Tourism Restaurant",
        "cami": "Tourism Masjid",
        "mall": "Tourism Mall"
    }

    return types.get(data_type)


def add_attachments(dt, dn, files):
    for file in files:
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": file.split("/")[-1],
            "file_url": file,
            "is_private": 0,
            "attached_to_name": dn,
            "attached_to_doctype": dt
        })
        file_doc.save(ignore_permissions=True)
