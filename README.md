B2c : The snippet below has two bugs related to document lifecycle. Identify both and write the corrected version in README_internals.md:

def validate(self):
    self.services_total = sum(r.line_total for r in self.service_lines)
    self.save()
    pet = frappe.get_doc("Pet", self.pet)
    pet.total_stays += 1
    pet.save()

ans: Calling self.save() inside validate() can trigger the same process again and  cause recursive validation or save behavior.

B2D : In README_internals.md: why would you see a "Document has been modified after you have opened it" error, and how does Frappe prevent concurrent overwrites? (One paragraph.)

ans: Another user changed the document after it was opened.Frappe uses optimistic locking to prevent overwriting newer changes.

C3-In README_internals.md: rename a test Attendant record. Does assigned_attendant on linked Stay Cards update automatically? Why or why not?

ans : No, Link fields store the document name,there they do not update automatically when linked.

D2-In README_internals.md: why is frappe.get_all dangerous in a whitelisted method exposed to low-privilege users?

ans: get_all() can pass normal permission-based filters. We can use frappe.get_list() when user permissions must apply.

E1 : Call self.save() inside on_update and observe what breaks. Explain it and correct the pattern in README_internals.md.

ans: No we should not  call self.save() inside on_update, it triggers on_update again and causes recursive saving. Instead, we can modify fields directly or use frappe.db.set_value()

H1 : In README_internals.md: why does a frappe.call inside the validate client event not work, and why must async fetches happen in onload/refresh instead?

ans : frappe.call() is asynchronous, but the validate event expects validation to finish immediately. So fetch the required data in onload/refresh, store it in the form, and let validate use that already-fetched value.

I1: In README_internals.md: show the f-string version side by side with the parameterized version, and explain why the latter is always preferred.

ans: Formatted string makes direct changes into sql leading to sql injection while parameterized version treats value separately and avoids security concerns

J1 : In README_internals.md: explain the difference between putting a frappe.get_all() call directly inside the Jinja template versus pre-computing in before_print() and referencing doc.precomputed_field.

ans: frappe.get_all() inside jinja directly blends with the presentation layer but before_print() which is defined separately increases optimization and separation of concern by allowing to re-fetch everytime.

N1 : Explain in README_internals.md why hiding a
field in JavaScript is not a security measure.

ans : Hiding a field in javascript only hides in an UI level still an user can see the field using api call  and can retrieve it from the database which raises a security concern.

