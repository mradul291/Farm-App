# Copyright (c) 2025, chirag and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import _
from frappe.model.document import Document


class PUESponsor(Document):
	
	def validate(self):
		used_items = set()

	# Get all equipment_name already used across all other PUE Sponsor docs
		existing_rows = frappe.get_all(
			"Sponsored Equipments Table",
			fields=["equipment_name", "parent"],
			filters={"parenttype": "PUE Sponsor"}
		)

		for row in existing_rows:
			# Exclude current document from the check
			if row.parent != self.name:
				used_items.add(row.equipment_name)

	# Check for duplicates in the current doc
		local_items = set()
		for row in self.sponsored_equipments:
			# Check if already exists in other docs
			if row.equipment_name in used_items:
				frappe.throw(_(f"Item '{row.equipment_name}' is already used in another PUE Sponsor document. Remove it there first."))

		# Check duplicate in same doc
			if row.equipment_name in local_items:
				frappe.throw(_(f"Item '{row.equipment_name}' is duplicated in this document. Please use it only once."))
			else:
				local_items.add(row.equipment_name)

	def on_update(self):
		for row in self.sponsored_equipments:
			current_qty = row.quantity or 0
			original_row = row.get("__original") or {}
			original_qty = original_row.get("quantity") or 0
   
			# Set initial_quantity only once on first credit
			if not row.get("__islocal") and not row.initial_quantity:
				row.initial_quantity = original_qty or current_qty
    
				frappe.db.set_value("Sponsored Equipments Table", row.name, "initial_quantity", row.initial_quantity)
   
			# Skip if quantity not changed
			if current_qty == original_qty and row.is_logged:
				continue

			# Case 1: New row added
			if not row.is_logged and current_qty > 0:
				if not row.availed_quantity:
					row.availed_quantity = 0  # Reset on first credit

				frappe.get_doc({
					"doctype": "Sponsor Equipments Logs",
					"equipment_name": row.equipment_name,
					"quantity": current_qty,
					"discount": row.discount,
					"operation": "Credited",
					"user": frappe.session.user,
					"reference_type": self.doctype,
					"reference_name": self.name,
					"sponsor": self.name,
					"remarks": "Sponsor equipment added to pool"
				}).insert(ignore_permissions=True)

				row.is_logged = 1

			# Case 2: Row was already logged, but quantity increased
			elif row.is_logged and current_qty > original_qty:
				additional_qty = current_qty - original_qty
				row.initial_quantity += additional_qty

				frappe.get_doc({
					"doctype": "Sponsor Equipments Logs",
					"equipment_name": row.equipment_name,
					"quantity": additional_qty,
					"discount": row.discount,
					"operation": "Credited",
					"user": frappe.session.user,
					"reference_type": self.doctype,
					"reference_name": self.name,
					"sponsor": self.name,
					"remarks": f"Additional quantity credited: {additional_qty}"
				}).insert(ignore_permissions=True)
