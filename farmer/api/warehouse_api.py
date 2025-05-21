import frappe

def create_warehouses_for_business(doc, method):

    for row in doc.create_warehouses:
        # Check if warehouse already exists
        if not frappe.db.exists("Warehouse", {"warehouse_name": row.warehouse_name}):
            warehouse = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": row.warehouse_name,
                "is_group": 0,
                "custom_business": doc.name,
                "parent_warehouse": "All Warehouses - FWH",
                "company": "Farmwarehouse",
            })
            warehouse.insert(ignore_permissions=True)
            frappe.db.set_value("Warehouse", warehouse.name, "owner", doc.email)
            frappe.db.commit()
