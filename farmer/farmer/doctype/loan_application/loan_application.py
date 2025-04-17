from frappe.website.website_generator import WebsiteGenerator
import frappe
from frappe.website.utils import get_sidebar_items
from frappe.utils import flt


class LoanApplication(WebsiteGenerator):
    
	def get_context(self, context):
        # Attach the document to context

		context.doc = self
		context.title = self.loan_title if hasattr(self, "loan_title") else self.name

		context.show_sidebar = True
		context.breadcrumbs = True
		context.show_portal_menu = True

		if hasattr(frappe.local, "request"):
			path = frappe.local.request.path
		if "/loan-application" in path:
			context.sidebar_items = get_sidebar_items("") 

			context.parents = [
			{"label": "Loan Applications", "route": "/loan-application"},]
		
        # Assign all required fields to context
		context.name = self.name
		context.applicant = self.applicant
		context.applicant_name = self.applicant_name
		context.product_name = self.product_name
		context.total_amount = self.total_amount
		context.loan_amount = self.loan_amount
		context.repayment_period = self.repayment_period
		context.interest_rate = self.interest_rate
		context.annual_income = self.annual_income
		context.down_payment_percentage = self.down_payment_percentage
		context.down_payment_amount = self.down_payment_amount
		context.compounding_frequency = self.compounding_frequency
		context.total_amount_after_interest = self.total_amount_after_interest
		context.loan_purpose = self.loan_purpose
		context.status = self.status
		context.sales_order = self.sales_order
		context.remarks = self.remarks

		return context
	

	def before_save(self):
		if not self.sales_invoice and self.sales_order:
			inv = frappe.get_all("Sales Invoice", filters={"sales_order": self.sales_order}, fields=["name"])
			if inv:
				self.sales_invoice = inv[0].name
				

	def on_update(self):
		if self.sales_invoice and self.total_amount_after_interest:
			try:
				si = frappe.get_doc("Sales Invoice", self.sales_invoice)
            
            	# Only update if different
				if flt(si.grand_total) != flt(self.total_amount_after_interest):
					new_total = flt(self.total_amount_after_interest)
					si.grand_total = new_total
					si.rounded_total = new_total
					si.outstanding_amount = new_total
					si.base_grand_total = new_total
					si.base_rounded_total = new_total

					si.set_onload("ignore_validate_update_after_submit", True)
					si.flags.ignore_validate_update_after_submit = True
					si.flags.ignore_validate = True
					si.flags.ignore_mandatory = True
					si.flags.ignore_permissions = True
					si.save()
					frappe.msgprint(f"Sales Invoice {si.name} updated with new total amount: {new_total}")
			except Exception as e:
				frappe.log_error(frappe.get_traceback(), "Error Updating Sales Invoice from Loan Application")
