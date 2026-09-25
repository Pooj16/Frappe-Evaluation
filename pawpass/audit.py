import frappe
def log_change(doc, method):
    if method == "on_update":
        action = "Updated"

    elif method == "on_submit":
        action = "Submitted"
    elif method == "on_cancel":
        action = "Cancelled"
    else:
        action = "Unknown Action"
    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": doc.doctype,
        "document_name": doc.name,
        "action": action,
        "user": frappe.session.user,
        "timestamp": frappe.utils.now(),
    }).insert(ignore_permissions=True)