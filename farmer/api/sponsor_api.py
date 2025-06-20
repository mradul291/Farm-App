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

#Create Debit note on Sales Invoice Submission
def update_sponsor_quantities_on_invoice_submit(doc, method):
	for item in doc.items:
		if not item.item_code:
			continue

		sponsor_row = frappe.get_all(
			"Sponsored Equipments Table",
			filters={"equipment_name": item.item_code},
			fields=["name", "parent", "equipment_name", "initial_quantity", "availed_quantity", "quantity", "discount"],
			order_by="modified asc",
			limit_page_length=1
		)

		if not sponsor_row:
			continue

		row = sponsor_row[0]
		row_name = row["name"]
		apply_qty = item.qty

		new_availed = row["availed_quantity"] + apply_qty
		frappe.db.set_value("Sponsored Equipments Table", row_name, "availed_quantity", new_availed)

		remaining_qty = (row["quantity"] or 0) - new_availed
		frappe.db.set_value("Sponsored Equipments Table", row_name, "remaining_quantity", remaining_qty)

		frappe.get_doc({
			"doctype": "Sponsor Equipments Logs",
			"equipment_name": row["equipment_name"],
			"quantity": apply_qty,
			"discount": row["discount"],
			"operation": "Debited",
			"user": frappe.session.user,
			"reference_type": doc.doctype,
			"reference_name": doc.name,
			"remarks": "Sponsor discount used on Sales Invoice"
		}).insert(ignore_permissions=True)
  
		recalculate_total_value(row["parent"])
	
	frappe.db.commit()

#Remove Debit Note if Sales Invoice Get Cancel
def reverse_sponsor_usage_on_invoice_cancel(doc, method):
	for item in doc.items:
		if not item.item_code:
			continue

		sponsor_row = frappe.get_all(
			"Sponsored Equipments Table",
			filters={"equipment_name": item.item_code},
			fields=["name", "parent", "availed_quantity", "remaining_quantity"],
			order_by="modified asc",
			limit_page_length=1
		)

		if not sponsor_row:
			continue

		row = sponsor_row[0]
		row_name = row["name"]
		reverse_qty = item.qty

		# Step 1: Reverse availed_quantity
		new_availed = max((row["availed_quantity"] or 0) - reverse_qty, 0)
		frappe.db.set_value("Sponsored Equipments Table", row_name, "availed_quantity", new_availed)

		# Step 2: Update remaining_quantity
		new_remaining = (row["remaining_quantity"] or 0) + reverse_qty
		frappe.db.set_value("Sponsored Equipments Table", row_name, "remaining_quantity", new_remaining)
  
		recalculate_total_value(row["parent"])

		# Step 3: Add reversal log
		frappe.get_doc({
			"doctype": "Sponsor Equipments Logs",
			"equipment_name": item.item_code,
			"quantity": reverse_qty,
			"discount": item.discount_percentage,
			"operation": "Cancelled",
			"user": frappe.session.user,
			"reference_type": doc.doctype,
			"reference_name": doc.name,
			"remarks": "Sponsor usage reversed on Sales Invoice cancellation"
		}).insert(ignore_permissions=True)

	frappe.db.commit()

#After transection Reduce the Total Value field data
def recalculate_total_value(pue_sponsor_name):
	total_value = 0

	sponsor_doc = frappe.get_doc("PUE Sponsor", pue_sponsor_name)

	for row in sponsor_doc.sponsored_equipments:
		if not row.equipment_name or not row.remaining_quantity:
			continue

		price = frappe.db.get_value("Item Price", {"item_code": row.equipment_name}, "price_list_rate")
		if not price:
			continue

		total_value += float(price) * float(row.remaining_quantity)

	sponsor_doc.total_value = total_value
	sponsor_doc.save(ignore_permissions=True)

#Debit Log creation on the Loan Payment
def apply_sponsor_discount_on_payment(doc, method):
	for ref in doc.references:
		if ref.reference_doctype != "Sales Invoice" or not ref.reference_name:
			continue

		invoice = frappe.get_doc("Sales Invoice", ref.reference_name)

		if invoice.status == "Partly Paid":
			log_exists = frappe.db.exists("Sponsor Equipments Logs", {
				"reference_type": "Sales Invoice",
				"reference_name": invoice.name,
				"operation": "Debited"
			})
			if not log_exists:
				update_sponsor_quantities_on_invoice_submit(invoice, method=None)

#Handling multiple hooks
def handle_payment_entry_submit(doc, method):
    from farmer.api.loan_api import loan_payment_update
    from farmer.api.sponsor_api import apply_sponsor_discount_on_payment

    # Call both functions
    loan_payment_update(doc, method)
    apply_sponsor_discount_on_payment(doc, method)


#Fetch List of Loans who Availed Discount on Loan 
@frappe.whitelist()
def get_qualified_loan_applications(sponsor_name):
    sponsor = frappe.get_doc("PUE Sponsor", sponsor_name)

    # Step 1: Build a map of item_code → discount
    item_discount_map = {
        row.equipment_name: float(row.discount or 0)
        for row in sponsor.sponsored_equipments
        if row.equipment_name and row.discount is not None
    }

    if not item_discount_map:
        return []

    item_codes = list(item_discount_map.keys())

    # Step 2: Get Loan Applications with item_code in sponsored items
    loan_apps = frappe.get_all("Loan Application",
        filters={"item_code": ["in", item_codes]},
        fields=["name", "item_code", "sales_invoice"]
    )

    qualified_loans = []

    # Step 3: For each Loan Application, check if its Sales Invoice has item with matching discount
    for loan in loan_apps:
        if not loan.sales_invoice:
            continue

        try:
            invoice = frappe.get_doc("Sales Invoice", loan.sales_invoice)
        except frappe.DoesNotExistError:
            continue

        for item in invoice.items:
            if item.item_code == loan.item_code:
                expected_discount = item_discount_map.get(loan.item_code)
                if float(item.discount_percentage or 0) == expected_discount:
                    qualified_loans.append(loan.name)
                    break

    return qualified_loans
