import frappe

FINANCIER_ROLE = "Financier"

def has_financier_role(user_doc) -> bool:
    """Return True only if the saved User has the custom ‘Financier’ role."""
    return any(role.role == FINANCIER_ROLE for role in user_doc.roles)

def map_user_to_financier_fields(user_doc) -> dict:
    """Central place to map User → FINANCIER field values."""
    return {
        "user": user_doc.name,
        "contact_email": user_doc.email or user_doc.name,
        "contact_phone": user_doc.mobile_no or user_doc.phone or "",
        "status": "Active",
    }
    
def create_financier_from_user(user_doc, method=None):
    if not has_financier_role(user_doc):
        return

    if frappe.db.exists("Financier", {"user": user_doc.name}):
        return  # Avoid duplicates

    fin = frappe.new_doc("Financier")
    fin.update(map_user_to_financier_fields(user_doc))
    fin.insert(ignore_permissions=True)
    frappe.db.commit()

def sync_financier_from_user(user_doc, method=None):
    if not has_financier_role(user_doc):
        return

    fin_name = frappe.db.get_value("Financier", {"user": user_doc.name})
    if not fin_name:
        create_financier_from_user(user_doc)
        return

    fin = frappe.get_doc("Financier", fin_name)
    fin.update(map_user_to_financier_fields(user_doc))
    fin.save(ignore_permissions=True)
    frappe.db.commit()

def sync_financier_loan_catalog(doc, method=None):
    # Get current user
    current_user = frappe.session.user

    # Get Financiers linked to this user only
    financiers = frappe.get_all(
        "Financier",
        filters={
            "status": "Active",
            "user": current_user
        },
        pluck="name"
    )

    for fin_name in financiers:
        fin_doc = frappe.get_doc("Financier", fin_name)

        # Check if Website Item exists in child table
        matched_rows = [
            item for item in fin_doc.loan_product_catalog
            if item.loan_product_name == doc.name
        ]

        if doc.financing_available:
            if not matched_rows:
                fin_doc.append("loan_product_catalog", {
                    "loan_product_name": doc.name
                })
        else:
            for row in matched_rows:
                fin_doc.remove(row)

        if doc.financing_available or matched_rows:
            fin_doc.save(ignore_permissions=True)

    frappe.db.commit()


@frappe.whitelist()
def get_total_recovered_amount():
    total = frappe.db.sql("""
        SELECT SUM(loan_amount_after_interest)
        FROM `tabLoan Installments`
        WHERE status = 'Completed'
    """, as_dict=0)[0][0] or 0

    return {
        "value": total,
        "fieldtype": "Currency"
    }
