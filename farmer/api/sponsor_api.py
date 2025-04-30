import frappe

@frappe.whitelist()
def mark_financing_available(website_item):
    if not website_item:
        return {"status": "failed", "message": "No Website Item provided"}

    try:
        doc = frappe.get_doc("Website Item", website_item)

        if doc.financing_available == 1:
            # Already marked, no need to update
            return {
                "status": "skipped",
                "message": f"'{website_item}' is already available for Financing."
            }

        doc.financing_available = 1
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {
            "status": "success",
            "message": f"Financing enabled for '{website_item}'."
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to update Website Item")
        return {"status": "error", "message": str(e)}
