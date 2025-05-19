# Copyright (c) 2025, chirag and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class Business(Document):
	def autoname(self):
		prefix = self.business_type.upper()
		entity_abbr = self.reference_entity[:3].upper()
		self.name = f"{prefix}-{entity_abbr}-{make_autoname('####.')}"
		self.business = self.name

