# Copyright (c) 2025, chirag and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class LoanInstallments(WebsiteGenerator):
	def after_insert(self):
		if not self.route:
			self.db_set('route', f'loan-installment/{self.name}')
		if not self.published:
			self.db_set('published', 1)

	def get_context(self, context):
        # Attach the document itself
		context.doc = self

        # Main fields from parent
		context.name = self.name
		context.applicant = self.applicant
		context.applicant_name = self.applicant_name
		context.loan_amount = self.loan_amount
		context.repayment_period = self.repayment_period
		context.interest_rate = self.interest_rate
		context.total_amount_after_interest = self.total_amount_after_interest
		context.compounding_frequency = self.compounding_frequency
		context.status = self.status
		context.remarks = self.remarks

        # Fetch child table data (Loan Installment Breakdown)
		context.installments = []
		if self.installments:
			for row in self.installments:
				context.installments.append({
                    "installment_number": row.installment_number,
                    "due_date": row.due_date,
                    "installment_amount": row.installment_amount,
                    "principal_amount": row.principal_amount,
                    "interest_amount": row.interest_amount,
                    "paid_status": row.paid_status,
                    "payment_date": row.payment_date,
                    "payment_link": row.payment_link
                })

        # Optional: Page title
		context.title = f"Loan Installments for {self.applicant_name or self.name}"

		return context
