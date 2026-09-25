import frappe
from frappe.query_builder import DocType
from frappe.utils import today, add_days
@frappe.whitelist()
def get_upcoming_checkouts():
    SC= DocType("Stay Card")
    return (
        frappe.qb.from_(SC).select(SC.name,SC.pet,SC.owner_name,SC.expected_checkout_date).where(SC.status.isin(["Checked In", "In Service"]) and SC.expected_checkout_date <= add_days(today(), 2)).orderby(SC.expected_checkout_date).run(as_dict=True)
    )
@frappe.whitelist()
def transfer_stays(from_attendant, to_attendant):
    try:
        frappe.db.sql("""
            UPDATE `tabStay Card` SET assigned_attendant = %s WHERE assigned_attendant = %s
        """, (to_attendant, from_attendant))

        frappe.db.commit()
        return "Stays transferred successfully"
    except Exception :
        print("hi")

@frappe.whitelist()
def after_install():
     settings = frappe.get_doc('Pawpass Settings')
     frappe.db.set_value('Pawpass Settings', settings.name, 'shop_name','Naturals')
     frappe.db.set_value('Pawpass Settings', settings.name, 'manager_email','pooja16.shivk@gmail.com')
     frappe.db.set_value('Pawpass Settings', settings.name, 'vaccination_grace_days',2)
     frappe.db.set_value('Pawpass Settings', settings.name, 'reminder_days_before_checkout',2)
     frappe.db.set_value('Pawpass Settings', settings.name, 'default_boarding_rate',100)
     if frappe.db.count('RESOURCE') == 0:
         frappe.get_doc({
             'doctype': 'RESOURCE',
             'resource_name': 'Default Resource1',
             'capacity': 10
         }).insert()
         frappe.get_doc({
             'doctype': 'RESOURCE',
             'resource_name': 'Default Resource2',
             'capacity': 20
         }).insert()
         frappe.get_doc({
             'doctype': 'RESOURCE',
             'resource_name': 'Default Resource3',
             'capacity': 30
         }).insert()
@frappe.whitelist()
def get_stay_summary(stay_card_name):
    stay_card = frappe.get_doc("Stay Card", stay_card_name)
    if not stay_card:
        frappe.local.response["http_status_code"] = 404
        return {"error": "Not found"}
    return {
        "name": stay_card.name,
        "pet": stay_card.pet,
        "owner_name": stay_card.owner_name,
        "checkin_date": stay_card.checkin_date,
        "expected_checkout_date": stay_card.expected_checkout_date,
    }
# http://127.0.0.1:8000/api/method/pawpass.api.get_stay_summary?PC-2026-00021