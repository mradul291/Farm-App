import frappe

# def create_warehouses_for_business(doc, method):

#     for row in doc.create_warehouses:
#         # Check if warehouse already exists
#         if not frappe.db.exists("Warehouse", {"warehouse_name": row.warehouse_name}):
#             warehouse = frappe.get_doc({
#                 "doctype": "Warehouse",
#                 "warehouse_name": row.warehouse_name,
#                 "is_group": 0,
#                 "custom_business": doc.name,
#                 "parent_warehouse": "All Warehouses - FWH",
#                 "company": "Farmwarehouse",
#             })
#             warehouse.insert(ignore_permissions=True)
#             frappe.db.set_value("Warehouse", warehouse.name, "owner", doc.email)
#             frappe.db.commit()

def create_warehouses_for_business(doc, method):
    # Fetch phone and location from User
    user_email = doc.email
    phone_no, location = frappe.db.get_value("User", user_email, ["phone", "location"])

    for row in doc.create_warehouses:
        if not frappe.db.exists("Warehouse", {"warehouse_name": row.warehouse_name}):
            warehouse = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": row.warehouse_name,
                "is_group": 0,
                "custom_business": doc.name,
                "parent_warehouse": "All Warehouses - FWH",
                "company": "Farmwarehouse",
                "phone_no": phone_no,
                "city": location
            })
            warehouse.insert(ignore_permissions=True)
            frappe.db.set_value("Warehouse", warehouse.name, "owner", doc.email)
            frappe.db.commit()


def link_warehouse_to_business(doc, method):
    if frappe.flags.in_import or frappe.flags.in_patch or frappe.flags.in_test:
        return

    owner_email = doc.owner

    # Try to find Business linked to this email
    business = frappe.get_all("Business", filters={"email": owner_email}, fields=["name"])
    if not business:
        return

    business_doc = frappe.get_doc("Business", business[0].name)

    # Check if this warehouse already exists in child table
    existing = [
        row.warehouse_name for row in business_doc.create_warehouses
    ]
    if doc.warehouse_name not in existing:
        business_doc.append("create_warehouses", {
            "warehouse_name": doc.warehouse_name
        })
        business_doc.save(ignore_permissions=True)
        frappe.db.commit()