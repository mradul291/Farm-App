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
	"""Reduce sponsored item quantities and update total_value using item_code directly"""

	modified_parents = set()

	for item in doc.items:
		if not item.discount_percentage or not item.item_code:
			continue

		remaining_qty_to_deduct = item.qty

		# Get all matching rows across all sponsors with available qty
		rows = frappe.get_all(
			"Sponsored Equipments Table",
			fields=["name", "parent", "quantity", "equipment_name"],
			filters={"equipment_name": item.item_code, "quantity": [">", 0]},
			order_by="modified asc"
		)

		for row in rows:
			if remaining_qty_to_deduct <= 0:
				break

			qty_to_deduct = min(row.quantity, remaining_qty_to_deduct)
			sponsor_doc = frappe.get_doc("PUE Sponsor", row.parent)

			for child in sponsor_doc.sponsored_equipments:
				if child.name == row.name:
					child.quantity -= qty_to_deduct
					remaining_qty_to_deduct -= qty_to_deduct
					break

			modified_parents.add(sponsor_doc.name)
			sponsor_doc.save(ignore_permissions=True)

	# Recalculate total_value for all modified docs
	for parent in modified_parents:
		sponsor_doc = frappe.get_doc("PUE Sponsor", parent)
		total = 0

		for row in sponsor_doc.sponsored_equipments:
			if not row.quantity or not row.equipment_name:
				continue

			# Directly use equipment_name (item_code) to get price
			price = frappe.db.get_value("Item Price", {"item_code": row.equipment_name}, "price_list_rate")
			if not price:
				continue

			total += price * row.quantity

		sponsor_doc.total_value = total
		sponsor_doc.save(ignore_permissions=True)

	frappe.db.commit()
