import frappe
import math
import json
from frappe import _
from frappe.utils import flt,cint
from datetime import datetime, timedelta
from erpnext.accounts.doctype.payment_request import payment_request
from frappe.utils import nowdate


@frappe.whitelist(allow_guest=True)
def create_invoice_from_sales_order(sales_order):
    if not sales_order:
        frappe.throw("Sales Order ID is required.")

    # Import ERPNext utility to generate Sales Invoice                                                                              
    from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice

    # Create and submit invoice
    si = make_sales_invoice(sales_order, ignore_permissions=True)
    si.allocate_advances_automatically = True
    si.insert(ignore_permissions=True)
     
    loan_app = frappe.get_all("Loan Application", filters={"sales_order": sales_order}, fields=["name"], limit=1)

    if loan_app:
        loan_doc = frappe.get_doc("Loan Application", loan_app[0].name)
        loan_doc.sales_invoice = si.name
        loan_doc.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "success",
        "invoice": si.name
    }


@frappe.whitelist(allow_guest=True)
def get_payment_url(pr_name):
    pr = frappe.get_doc("Payment Request", pr_name)
    return pr.get_payment_url()

#Down Payment Process 

@frappe.whitelist(allow_guest=True)
def make_loan_payment_request(dn, dt="Sales Invoice", submit_doc=1, order_type="Shopping Cart"):
    ref_doc = frappe.get_doc(dt, dn)

    # 1. Check if Payment Entry already exists (means payment is done)
    payment_entries = frappe.get_all("Payment Entry", filters={
        "reference_doctype": dt,
        "reference_name": dn,
        "docstatus": 1
    })

    if payment_entries:
        return {
            "error": 1,
            "message": "Payment Entry already created. Payment completed."
        }

    # 2. Check if a Payment Request already exists
    existing_request = frappe.get_all("Payment Request", filters={
        "reference_doctype": dt,
        "reference_name": dn,
        "docstatus": 1,
        "status": ["in", ["Initiated", "Requested", "Paid"]]
    }, fields=["name", "status"], order_by="creation desc", limit=1)

    if existing_request:
        request_doc = frappe.get_doc("Payment Request", existing_request[0].name)
        
        # If Payment Request is paid, don't allow retry
        if request_doc.status == "Paid":
            return {
                "error": 1,
                "message": "Payment already completed.",
                "payment_request": request_doc.name,
                "payment_url": request_doc.get_payment_url()
            }

        # Otherwise, return the current payment request link
        return {
            "payment_request": request_doc.name,
            "payment_url": request_doc.get_payment_url()
        }
    
    # Step 3: Find linked Loan Application
    loan_apps = frappe.get_all("Loan Application", filters={"sales_invoice": dn}, fields=["name", "down_payment_amount"])

    if not loan_apps:
        frappe.throw(_("No Loan Application linked to Sales Invoice {0}").format(dn))

    loan_app = loan_apps[0]
    down_payment_amount = loan_app.down_payment_amount

    if not down_payment_amount or float(down_payment_amount) <= 0:
        frappe.throw(_("Please Add Remark and Save the Loan Application."))
        # frappe.throw(_("Down Payment Amount is not set in the Loan Application {0}").format(loan_app.name))

    # Step 4: Prepare Payment Request
    args = {
        "dn": dn,   
        "dt": dt,
        "submit_doc": cint(submit_doc),
        "order_type": order_type,
        "mode_of_payment": "Paystack",
        "recipient_id": ref_doc.get("contact_email") or ref_doc.owner,
        "party_type": "Customer",
        "party": ref_doc.customer,
        "amount": down_payment_amount,
        "return_doc": True,
        "mute_email": 1,
    }

    original_get_amount = payment_request.get_amount

    def get_custom_amount(doc, account=None):
        return down_payment_amount

    payment_request.get_amount = get_custom_amount
    
    result = payment_request.make_payment_request(**args)
    payment_request.get_amount = original_get_amount

    if result.docstatus == 0:
        result.flags.ignore_permissions = True
        result.submit()

    if frappe.local.response.get("type") == "redirect":
        del frappe.local.response["type"]
        del frappe.local.response["location"]

    return {
        "payment_request": result.name,
        "amount": down_payment_amount,
        "payment_url": result.get_payment_url()
    }

def loan_payment_update(doc, method):
    for ref in doc.references:
        if ref.reference_doctype == "Sales Invoice" and ref.reference_name:
            loan_apps = frappe.get_all("Loan Application", filters={"sales_invoice": ref.reference_name})

            for la in loan_apps:
                loan_doc = frappe.get_doc("Loan Application", la.name)

                if not loan_doc.down_payment_check:
                    loan_doc.db_set("down_payment_check", 1)
                if loan_doc.status != "Loan Sanctioned":
                    loan_doc.db_set("status", "Loan Sanctioned")

                new_mode = "Cash" if doc.mode_of_payment == "Cash" else "Paystack"
                if loan_doc.mode_of_down_payment != new_mode:
                    loan_doc.db_set("mode_of_down_payment", new_mode)

#####################################################################################################

def create_loan_installments(doc, method):
    """
    Triggered when a Loan Application is approved.
    Creates a Loan Installments record and generates installment breakdowns.
    """
    if doc.status == "Approved":
        # Check if a Loan Installments record already exists
        if frappe.db.exists("Loan Installments", {"applicant": doc.name}):
            frappe.msgprint("Loan Installments already created for this application.", alert=True)
            return

        # Ensure numeric fields are converted properly
        loan_amount = float(doc.loan_amount) if doc.loan_amount else 0.0
        interest_rate = float(doc.interest_rate) if doc.interest_rate else 0.0
        repayment_period = int(doc.repayment_period) if doc.repayment_period else 0
        total_amount_after_interest = float(doc.total_amount_after_interest) if doc.total_amount_after_interest else 0.0
        applicant_name = doc.applicant_name
        applicant_id = doc.applicant
        sales_order = doc.sales_order
        sales_invoice = doc.sales_invoice
        down_payment = doc.down_payment_amount
        
        # Create a new Loan Installments record
        loan_installment = frappe.new_doc("Loan Installments")
        loan_installment.applicant = doc.name
        loan_installment.applicant_name = applicant_name
        loan_installment.applicant_id = applicant_id
        loan_installment.loan_amount = loan_amount
        loan_installment.repayment_period = repayment_period
        loan_installment.interest_rate = interest_rate
        loan_installment.compounding_frequency = doc.compounding_frequency
        loan_installment.status = "Active"
        loan_installment.sales_order = sales_order
        loan_installment.sales_invoice = sales_invoice
        loan_installment.down_payment = down_payment
        
        # Calculate total amount after interest
        loan_installment.total_amount_after_interest = total_amount_after_interest
        loan_installment.loan_amount_after_interest = total_amount_after_interest - down_payment
        loan_installment.total_loan_amount = total_amount_after_interest - down_payment

        # Generate Installments
        generate_installment_breakdown(loan_installment, loan_amount, interest_rate, repayment_period)

        # Save Loan Installments document
        loan_installment.insert()

         # 3. Now set proper route
        loan_installment.db_set("route", f"loan-installment/{loan_installment.name}")

        # 4. Set published
        loan_installment.db_set("published", 1)

        try:
            frappe.db.set_value("Loan Application", doc.name, "loan_installment", loan_installment.name, update_modified=False)
            frappe.db.commit()
            # frappe.msgprint(f"Loan Installment ID {loan_installment.name} linked to Loan Application {doc.name}.", alert=True)
        except Exception as e:
            frappe.log_error(title="Loan Application Update Failed", message=frappe.get_traceback())
            frappe.msgprint("Failed to link Loan Installment to Loan Application. Check error logs.", alert=True)

        make_installment_payment_request(sales_invoice)

        frappe.msgprint(f"Loan Installments created successfully for {doc.applicant}.", alert=True)
        frappe.msgprint(f"Loan Installments created successfully for {doc.applicant}.", alert=True)

def generate_installment_breakdown(loan_installment, loan_amount, interest_rate, repayment_period):
    """
    Generates installment breakdown based on EMI calculation and populates the child table.
    """
    if repayment_period == 0:
        return

    monthly_rate = interest_rate / 100 / 12
    emi = (loan_amount * monthly_rate * math.pow(1 + monthly_rate, repayment_period)) / (math.pow(1 + monthly_rate, repayment_period) - 1)

    loan_installment.installment_amount = int(round(emi))

    for i in range(1, repayment_period + 1):
        due_date = datetime.today() + timedelta(days=30 * i)
        interest_amount = loan_amount * monthly_rate
        principal_amount = emi - interest_amount

        unique_note = f"{loan_installment.sales_order}-INST-{i}"
        
        loan_installment.append("installments", {
            "installment_number": i,
            "due_date": due_date.strftime('%Y-%m-%d'),
            "installment_amount": int(round(emi)),
            "principal_amount": round(principal_amount, 2),
            "interest_amount": round(interest_amount, 2),
            "payment_link": "", 
            "installment_id": unique_note,
            "paid_status": "",
            "mode_of_payment": "Paystack"
        })

@frappe.whitelist(allow_guest=True)
def make_installment_payment_request(dn):
    if not dn:
        frappe.throw("Please pass the Sales Invoice (dn)")

    ref_doc = frappe.get_doc("Sales Invoice", dn)
    created_requests = []

    from erpnext.accounts.doctype.payment_request import payment_request
    original_get_amount = payment_request.get_amount

    loan_installment = frappe.get_doc("Loan Installments", {"sales_invoice": dn})
    if not loan_installment:
        frappe.throw(f"Loan Installments not found for Sales Invoice {dn}")

    def get_custom_amount(doc, account=None):
        # This will be overridden per loop iteration
        return current_amount   

    # Override global method temporarily
    payment_request.get_amount = get_custom_amount

    for i, row in enumerate(loan_installment.installments):
        current_amount = flt(row.installment_amount or 0)
        unique_note = row.installment_id

        if not current_amount:
            continue  # Skip rows with 0 amount

        pr_args = {
            "dt": "Sales Invoice",
            "dn": dn,
            "submit_doc": 1,
            "order_type": "Shopping Cart",
            "mode_of_payment": "Cash",
            "recipient_id": ref_doc.get("contact_email") or ref_doc.owner,
            "party_type": "Customer",
            "party": ref_doc.customer,
            "amount": int(flt(current_amount) * 100),
            "return_doc": True,
            "mute_email": 1,
            "notes": f"Installment {i+1} of {len(loan_installment.installments)} for Sales Invoice {dn}",
            "installment": unique_note,
            "is_installment_payment": 1
        }

        try:
            result = payment_request.make_payment_request(**pr_args)

            if frappe.local.response.get("type") == "redirect":
                del frappe.local.response["type"]
                del frappe.local.response["location"]

            if result.docstatus == 0:
                result.submit()

            # Update corresponding child row
            row.set("payment_request", result.name)
            row.set("payment_link", result.get_payment_url())
            loan_installment.flags.dirty = True

            created_requests.append({
                "installment_id": unique_note,
                "payment_request": result.name,
                "amount": current_amount,
                "payment_url": result.get_payment_url()
            })

        except frappe.ValidationError as e:
            created_requests.append({
                "installment_id": unique_note,
                "error": 1,
                "message": str(e)
            })

    loan_installment.save(ignore_permissions=True)

    # Restore original method
    payment_request.get_amount = original_get_amount

    return {
        "sales_invoice": dn,
        "total_requested": len(created_requests),
        "payment_requests": created_requests
    }   

#Function to refresh the Loan Installment document from web page using id.
@frappe.whitelist(allow_guest=True)
def refresh_loan_installments(loan_name):
    try:
        # Fetch the Loan Installments documentt
        doc = frappe.get_doc("Loan Installments", loan_name)
        updated = False

        # Loop through each installment in the document
        for row in doc.installments:    
            if row.payment_request:
                # Fetch the status of the payment request
                status = frappe.db.get_value("Payment Request", row.payment_request, "status")
                
                # If the payment is marked as "Paid", update the installment details
                if status == "Paid":
                    if row.paid_status != "Paid":
                        row.paid_status = "Paid"
                        updated = True

                        # Subtract installment amount from total_loan_amount
                        if row.installment_amount:
                            doc.total_loan_amount = flt(doc.total_loan_amount) - flt(row.installment_amount)
                            updated = True

                    if not row.payment_date:
                        row.payment_date = nowdate()
                        updated = True
                        

        # Save the document if any changes were made
        if updated: 
            doc.save(ignore_permissions=True)
            return {"status": "Updated"}
        else:
            return {"status": "No Change"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}
    