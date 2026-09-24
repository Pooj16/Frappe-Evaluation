import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate, add_days, flt

class StayCard(Document):
    def validate(self):
        vaccination_expiry = frappe.db.get_value("Pet", self.pet, "vaccination_expiry")
        grace_days = frappe.db.get_single_value("Pawpass Settings","vaccination_grace_days") or 0
        if vaccination_expiry:
            expiry_date = add_days( getdate(vaccination_expiry),int(grace_days))
            if expiry_date < getdate(today()):
                self.vaccination_status = "Expired"
                if self.status != "Draft":
                    frappe.throw("The pet's vaccination has expired.")
            else:
                self.vaccination_status = "Valid"
        else:
            self.vaccination_status = "Not Checked"
        if "Boarding" in self.purpose:
            if not self.expected_checkout_date:
                frappe.throw("Expected checkout date is required.")
            if getdate(self.expected_checkout_date) <= getdate(self.checkin_date):
                frappe.throw("Expected checkout date must be after checkin date.")
        self.services_total = 0
        for row in self.service_lines:
            row.line_total = (flt(row.rate) * flt(row.quantity))
            self.services_total += row.line_total
        self.final_amount = self.services_total
    def before_submit(self):
        if self.status not in ["Ready for Pickup", "Picked Up"]:
            frappe.throw("Stay Card must be Ready for Pickup.")
        if not self.service_lines:
            frappe.throw("At least one service line is required.")
        vaccination_expiry = frappe.db.get_value("Pet", self.pet, "vaccination_expiry")
        grace_days = frappe.db.get_single_value("Pawpass Settings","vaccination_grace_days") or 0
        if vaccination_expiry:
            expiry_date = add_days(getdate(vaccination_expiry),int(grace_days))
            if expiry_date < getdate(today()):
                self.vaccination_status = "Expired"
                frappe.throw("The pet's vaccination has expired.")
            self.vaccination_status = "Valid"
    def on_submit(self):
        total = frappe.db.get_value("Pet",self.pet,"total_stays") or 0
        frappe.db.set_value("Pet",self.pet,
            {
                "last_visit_date": today(),
                "total_stays": total + 1
            }
        )
        if not frappe.db.exists("Invoice",{"stay_card": self.name}):
            invoice = frappe.new_doc("Invoice")
            invoice.stay_card = self.name
            invoice.insert()
        frappe.enqueue(
            send_stay_email,
            queue="short",
            timeout=300,
            stay_card_name=self.name,
            is_async=True,
            enqueue_after_commit=True,
        )
    def on_cancel(self):
        self.db_set("status", "Cancelled")
        total = frappe.db.get_value("Pet",self.pet,"total_stays") 
        frappe.db.set_value("Pet",self.pet,"total_stays",total - 1)
        invoice = frappe.db.get_value("Invoice",{"stay_card": self.name},"name")
        if invoice:
            frappe.get_doc("Invoice", invoice).cancel()
    def on_trash(self):
        if self.status not in ["Draft", "Cancelled"]:
            frappe.throw("Only Draft or Cancelled Stay Cards can be deleted.")
    def on_update(self):
        pass

def send_stay_email(stay_card_name):
    if not frappe.db.exists("Stay Card", stay_card_name):
        return
    doc = frappe.get_doc("Stay Card", stay_card_name)
    email = frappe.db.get_value("Pet",doc.pet,"owner_email")
    if email:
        frappe.sendmail(
            recipients=[email],
            subject="Your Pet Stay is Completed",
            message="<p>Hi from Pet Shop</p>"
        )