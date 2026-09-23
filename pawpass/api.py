import frappe
from frappe.query_builder import DocType
from frappe.utils import today, add_days
@frappe.whitelist()
def get_upcoming_checkouts():
    SC= DocType("Stay Card")
    return (
        frappe.qb.from_(SC).select(SC.name,SC.pet,SC.owner_name,SC.expected_checkout_date).where(SC.status.isin(["Checked In", "In Service"]) and SC.expected_checkout_date <= add_days(today(), 2)).orderby(SC.expected_checkout_date).run(as_dict=True)
    )
# @frappe.whitelist()
# def transfer_stays(from_attendant,to_attendant):
#     try:
#         data=frappe.db.sql("""UPDATE stay_card.attendant""")