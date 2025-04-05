from frappe.website.website_generator import WebsiteGenerator
import frappe

class LoanApplication(WebsiteGenerator):
    
	def get_context(self, context):
        # Attach the document to context
        
		context.doc = self
		context.title = self.loan_title if hasattr(self, "loan_title") else self.name

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
	
