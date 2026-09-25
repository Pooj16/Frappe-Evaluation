# Copyright (c) 2026, Pooja and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    
    return columns, data, None, chart

def get_columns():
    return [
        {
            "label": ("Attendant"), 
            "fieldname": "assigned_attendant", 
            "fieldtype": "Link", 
            "options": "Attendant"
        },
        {
            "label": ("Total Stays"), 
            "fieldname": "total_stays", 
            "fieldtype": "Int"
        },
        {
            "label": ("Completed"), 
            "fieldname": "completed_stays", 
            "fieldtype": "Int"
        },
        {
            "label": ("Average Stay Length (nights)"), 
            "fieldname": "average_stay_length", 
            "fieldtype": "Int"
        },
        {
            "label": ("Revenue"), 
            "fieldname": "revenue", 
            "fieldtype": "Currency"
        },
        {
            "label": ("Completion Rate %"), 
            "fieldname": "completion_rate", 
            "fieldtype": "Percent"
        },
    ]

def get_data(filters=None):
		filters = filters or {}

		query = f"""
			SELECT 
				assigned_attendant,
				COUNT(name) as total_stays,
				SUM(CASE WHEN status = 'Picked Up' THEN 1 ELSE 0 END) as completed_stays,
				ROUND(AVG(DATEDIFF(checkin_date, actual_checkout_date)), 0) as average_stay_length,
				SUM(CASE WHEN status = 'Picked Up' THEN final_amount ELSE 0 END) as revenue,
				ROUND((SUM(CASE WHEN status = 'Picked Up' THEN 1 ELSE 0 END) / COUNT(name)) * 100, 2) as completion_rate
			FROM `tabStay Card`
			GROUP BY assigned_attendant
			ORDER BY assigned_attendant ASC
		"""
		
		return frappe.db.sql(query, filters, as_dict=True)

def get_chart(data):
    if not data:
        return None
        
    labels = [row.get("assigned_attendant") for row in data]
    total_stays = [row.get("total_stays", 0) for row in data]
    completed_stays = [row.get("completed_stays", 0) for row in data]
    
    return {
        "title":("Total vs Completed Stays per Attendant"),
        "type": "bar",
        "height": 300,
        "data": {
            "labels": labels,
            "datasets": [
                {"name": ("Total Stays"), "values": total_stays},
                {"name": ("Completed Stays"), "values": completed_stays}
            ]
        },
        "colors": ["#4F46E5", "#0B9657"] 
    }


