# import frappe
# from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry

# class CustomPaymentEntry(PaymentEntry):

# 	def validate_reference_documents(self):
# 		for ref in self.references:
# 			if ref.reference_doctype == "Sales Order":
# 				# Completely skip default Sales Order validation
# 				continue
# 		# For other doctypes, keep the default checks
# 		super().validate_reference_documents()

# 	def validate_allocated_amount_with_latest_data(self):
# 		# Optional: also skip payment limit validation
# 		for ref in self.references:
# 			if ref.reference_doctype == "Sales Order":
# 				continue
# 		super().validate_payment_against_order()

# 	def validate_allocated_amount(self):
# 		# Optional: if validation errors on allocation vs total
# 		pass
