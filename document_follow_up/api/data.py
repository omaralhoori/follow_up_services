from document_follow_up.api.upload import upload_data
import frappe
from frappe.defaults import get_user_permissions


@frappe.whitelist()
def get_services(search="", start=0, limit=20):
    allowed_entities = get_user_allowed_entities()
    services = frappe.db.sql("""
        select * from
            `tabServices`
        where related_entity in ({allowed_entities}) and name like %(txt)s
        order by creation desc
        limit {start},{limit}
        """.format(
            allowed_entities=",".join([f"'{ent}'" for ent in allowed_entities]),
            limit=limit,
            start=start
            ),
        {"txt": "%%%s%%" % search, '_txt': search}, as_dict=True)
    for service in services:
        service['files'] = frappe.db.get_all("Service Attachments", {"parent": service['name']}, ['attached_file', "notes"])
    return services

@frappe.whitelist()
def get_user_allowed_entities():
    allowed_entities = []
    # return frappe.db.get_all("Related Entity", ["name"], pluck="name")
    permissions = get_user_permissions()
    allowed_entities = [perm.doc for perm in permissions.get("Related Entity", [])]
    return allowed_entities


@frappe.whitelist()
def add_service():
    #service_data = get_service_request_data(frappe.form_dict)
    service_doc = frappe.get_doc({
        "doctype": "Services",
        **frappe.form_dict   
    })
    files = upload_data()
    for file in files:
        attachment = service_doc.append("service_attachments")
        attachment.attached_file = file
    service_doc.save()
    frappe.db.commit()
    return service_doc.name

@frappe.whitelist()
def share_service(service_name):
    service = frappe.get_doc("Services", service_name)
    service.serivce_shared = 1
    service.create_service_processing()
    frappe.db.commit()

# def get_service_request_data(form_data):
#     return {
#         ""
#     }
