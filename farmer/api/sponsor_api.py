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


def update_sponsor_discount_usage(doc, method=None):
	"""Reduce PUE Sponsor quantities based on items sold with discount"""

	pue_sponsor = frappe.get_all("PUE Sponsor", limit=1, order_by="modified desc")
	if not pue_sponsor:
		return

	sponsor_doc = frappe.get_doc("PUE Sponsor", pue_sponsor[0].name)
	discount_map = {row.equipment_name: row for row in sponsor_doc.sponsored_equipments}

	changed = False
	for item in doc.items:
		row = discount_map.get(item.item_code)
		if row and row.quantity > 0 and item.discount_percentage:
			# Calculate how many units used from sponsor stock
			used_qty = min(item.qty, row.quantity)
			row.quantity -= used_qty
			changed = True

	if changed:
		sponsor_doc.save(ignore_permissions=True)
		frappe.db.commit()
