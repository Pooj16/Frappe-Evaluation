// Copyright (c) 2026, Pooja and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stay Card", {
	setup(frm){
        frm.set_query("assigned_attendant",()=>{
            return{
                filter:{
                    status:'Active'
                }
            }
        })
    }
});
frappe.ui.form.on("Stay Card", {
	refresh(frm){
        let colors={
            "Draft":"gray",
            "Checked In":"blue",
            "In Service":"orange",
            "Ready for Pickup":"green",
            "Picked Up":"green",   
            "Cancelled":"red",     
        }
        if(frm.doc.status){
            frm.dashboard.add_indicator(
            frm.doc.status,
            colors[frm.doc.status]
        );
        if(frm.doc.status==='Ready for Pickup' && frm.doc.docstatus===1){
            frm.add_custom_button('Know status',function(){
                frappe.msgprint('Marked as '+frm.doc.status);
            });
        }
    }
    },
    assigned_attendant(frm){
        frappe.db.get_value("Attendant",frm.doc.specialization,"specialization")
        
    }
});
frappe.ui.form.on("Stay Card", {
    refresh(frm) {
        frm.add_custom_button("Cancel Stay", function() {
            let d = new frappe.ui.Dialog({
                title: "Enter details",
                fields: [
                    {
                        label: "Cancellation Reason",
                        fieldname: "remarks",
                        fieldtype: "Data",
                        reqd: 1
                    }
                ],
                size: "small",
                primary_action_label: "Submit",
                primary_action(values) {
                    frm.set_value("remarks", values.remarks);
                    d.hide();
                }
            }); 
            d.show();
        });
        frm.add_custom_button("Reassign Attendant", function() {
            frappe.prompt(
                [
                    {
                        label: "Attendant",
                        fieldname: "attendant",
                        fieldtype: "Link",
                        options: "Attendant",
                        reqd: 1
                    }
                ],
                function(values) {
                    frappe.confirm("Are you sure you want to reassign the attendant?",
                        () => {
                            frappe.db.set_value("Stay Card", frm.doc.name, "assigned_attendant", values.attendant);
                            frappe.msgprint("Attendant reassigned successfully"
                            );
                        },
                        () => {
                            frappe.msgprint("Attendant reassignment cancelled"
                            );
                        }
                    );
                },
            );
        });
        frm.trigger("assigned_attendant");
    },
});