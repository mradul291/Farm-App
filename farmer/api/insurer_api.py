import frappe

INSURER_ROLE = "Insurer"

def has_insurer_role(user_doc) -> bool:
    return any(role.role == INSURER_ROLE for role in user_doc.roles)

def map_user_to_insurer_fields(user_doc) -> dict:
    return {
        "user": user_doc.name,
        "contact_phone": user_doc.mobile_no or user_doc.phone or "",
        "insurer_name": user_doc.full_name or user_doc.first_name or user_doc.username,
        "status": "Active",
    }

def create_insurer_from_user(user_doc, method=None):
    if not has_insurer_role(user_doc):
        return

    if frappe.db.exists("Insurer", {"user": user_doc.name}):
        return

    insurer = frappe.new_doc("Insurer")
    insurer.update(map_user_to_insurer_fields(user_doc))
    insurer.insert(ignore_permissions=True)
    frappe.db.commit()

def sync_insurer_from_user(user_doc, method=None):
    if not has_insurer_role(user_doc):
        return

    insurer_name = frappe.db.get_value("Insurer", {"user": user_doc.name})
    if not insurer_name:
        create_insurer_from_user(user_doc)
        return

    insurer = frappe.get_doc("Insurer", insurer_name)
    insurer.update(map_user_to_insurer_fields(user_doc))
    insurer.save(ignore_permissions=True)
    frappe.db.commit()
