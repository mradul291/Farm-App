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
