
# import frappe
import frappe
from frappe import _
from frappe.model.document import Document


class PUESponsor(Document):
	
	def validate(self):
     # --- Step 1: Validate unique usage of equipment_name ---
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


	# # --- Step 2: Handle quantity changes and logging ---
		for row in self.sponsored_equipments:
			if not row.is_logged and row.quantity and row.equipment_name:
				# Initialize credit tracking
				row.initial_quantity = row.quantity
				row.availed_quantity = 0
				row.remaining_quantity = row.quantity
				row.is_logged = 1

			# Create Credit Log
				frappe.get_doc({
					"doctype": "Sponsor Equipments Logs",
					"equipment_name": row.equipment_name,
					"quantity": row.quantity,
					"discount": row.discount,
					"operation": "Credited",
					"user": frappe.session.user,
					"reference_type": self.doctype,
					"reference_name": self.name,
					"remarks": "Sponsor equipment credited on sponsor setup"
				}).insert(ignore_permissions=True)
 

	# def on_update(self):
	# 	for row in self.sponsored_equipments:
	# 		if not row.equipment:
	# 			continue

	# 		try:
	# 			web_item = frappe.get_doc("Website Item", row.equipment)

	# 			# If remaining quantity is zero or less, reset discount to 0
	# 			if row.remaining_quantity <= 0:
	# 				web_item.pue_discount = 0
	# 			else:
	# 				web_item.pue_discount = row.discount or 0

	# 			web_item.save(ignore_permissions=True)

	# 		except frappe.DoesNotExistError:
	# 			frappe.logger().warning(f"Website Item '{row.equipment}' not found.")
	# 		except Exception as e:
	# 			frappe.logger().error(f"Failed to update PUE discount for '{row.equipment}': {e}")
    
	def before_save(self):
		# Store previous equipment items temporarily
		old_items_raw = frappe.db.get_all(
			"Sponsored Equipments Table",
			filters={"parent": self.name, "parenttype": "PUE Sponsor"},
			fields=["equipment"]
		)
		self._previous_equipment_items = {row.equipment for row in old_items_raw if row.equipment}

	def on_update(self):
		# Step 1: Get current items from the updated doc
		current_items = {row.equipment for row in self.sponsored_equipments if row.equipment}

		# Step 2: Get previously cached items from before_save
		old_items = getattr(self, "_previous_equipment_items", set())

		# Step 3: Detect deleted items
		deleted_items = old_items - current_items

		# Step 4: Reset PUE discount for deleted items
		for item in deleted_items:
			try:
				web_item = frappe.get_doc("Website Item", item)
				web_item.pue_discount = 0
				web_item.save(ignore_permissions=True)
			except frappe.DoesNotExistError:
				frappe.logger().warning(f"Website Item '{item}' not found during deletion sync.")
			except Exception as e:
				frappe.logger().error(f"Failed to reset PUE discount for deleted item '{item}': {e}")

		# Step 5: Keep your existing update logic untouched
		for row in self.sponsored_equipments:
			if not row.equipment:
				continue
			try:
				web_item = frappe.get_doc("Website Item", row.equipment)
				web_item.pue_discount = row.discount if row.remaining_quantity > 0 else 0
				web_item.save(ignore_permissions=True)
			except frappe.DoesNotExistError:
				frappe.logger().warning(f"Website Item '{row.equipment}' not found.")
			except Exception as e:
				frappe.logger().error(f"Failed to update PUE discount for '{row.equipment}': {e}")
