import frappe
import math
import json
from frappe import _
from frappe.utils import flt,cint
from datetime import datetime, timedelta
from erpnext.accounts.doctype.payment_request import payment_request
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry as original_get_payment_entry



@frappe.whitelist(allow_guest=True)
def get_payment_url(pr_name):
    pr = frappe.get_doc("Payment Request", pr_name)
    return pr.get_payment_url()

#Down Payment Process 


@frappe.whitelist(allow_guest=True)
def make_loan_payment_request(dn, dt="Sales Order", submit_doc=1, order_type="Shopping Cart"):
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
    loan_apps = frappe.get_all("Loan Application", filters={"sales_order": dn}, fields=["name", "down_payment_amount"])

    for la in loan_apps:
        loan_doc = frappe.get_doc("Loan Application", la.name)
        if not loan_doc.down_payment_check:
            loan_doc.db_set("down_payment_check", 1)
            frappe.db.commit()

    if not loan_apps:
        frappe.throw(_("No Loan Application linked to Sales Order {0}").format(dn))

    loan_app = loan_apps[0]
    down_payment_amount = loan_app.down_payment_amount

    if not down_payment_amount or float(down_payment_amount) <= 0:
        frappe.throw(_("Down Payment Amount is not set in the Loan Application {0}").format(loan_app.name))

    # Step 4: Prepare Payment Request
    args = {
        "dn": dn,
        "dt": dt,
        "submit_doc": cint(submit_doc),
        "order_type": order_type,
        "mode_of_payment": "Cash",
        "recipient_id": ref_doc.get("contact_email") or ref_doc.owner,
        "party_type": "Customer",
        "party": ref_doc.customer,
        "amount": down_payment_amount,
        "return_doc": True,
        "mute_email": 1,
    }

    from erpnext.accounts.doctype.payment_request import payment_request
    original_get_amount = payment_request.get_amount

    def get_custom_amount(doc, account=None):
        return down_payment_amount

    payment_request.get_amount = get_custom_amount
    
    result = payment_request.make_payment_request(**args)
    payment_request.get_amount = original_get_amount

    if result.docstatus == 0:
        result.submit()

    if frappe.local.response.get("type") == "redirect":
        del frappe.local.response["type"]
        del frappe.local.response["location"]

    return {
        "payment_request": result.name,
        "amount": down_payment_amount,
        "payment_url": result.get_payment_url()
    }


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
        
        # Calculate total amount after interest
        loan_installment.total_amount_after_interest = total_amount_after_interest  

        # Generate Installments
        generate_installment_breakdown(loan_installment, loan_amount, interest_rate, repayment_period)

        # Save Loan Installments document
        loan_installment.insert()

         # 3. Now set proper route
        loan_installment.db_set("route", f"loan-installment/{loan_installment.name}")

        # 4. Set published
        loan_installment.db_set("published", 1)

        make_installment_payment_request(sales_order)

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

    loan_installment.installment_amount = round(emi, 2)

    for i in range(1, repayment_period + 1):
        due_date = datetime.today() + timedelta(days=30 * i)
        interest_amount = loan_amount * monthly_rate
        principal_amount = emi - interest_amount

        unique_note = f"{loan_installment.sales_order}-INST-{i}"
        
        loan_installment.append("installments", {
            "installment_number": i,
            "due_date": due_date.strftime('%Y-%m-%d'),
            "installment_amount": round(emi, 2),
            "principal_amount": round(principal_amount, 2),
            "interest_amount": round(interest_amount, 2),
            "payment_link": "", 
            "installment_id": unique_note,
            "paid_status": ""
        })



@frappe.whitelist(allow_guest=True)
def make_installment_payment_request(dn):
    if not dn:
        frappe.throw("Please pass the Sales Order (dn)")

    ref_doc = frappe.get_doc("Sales Order", dn)
    created_requests = []

    from erpnext.accounts.doctype.payment_request import payment_request
    original_get_amount = payment_request.get_amount

    loan_installment = frappe.get_doc("Loan Installments", {"sales_order": dn})
    if not loan_installment:
        frappe.throw(f"Loan Installments not found for Sales Order {dn}")

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
            "dt": "Sales Order",
            "dn": dn,
            "submit_doc": 1,
            "order_type": "Shopping Cart",
            "mode_of_payment": "Cash",
            "recipient_id": ref_doc.get("contact_email") or ref_doc.owner,
            "party_type": "Customer",
            "party": ref_doc.customer,
            "amount": current_amount,
            "return_doc": True,
            "mute_email": 1,
            "notes": f"Installment {i+1} of {len(loan_installment.installments)} for Sales Order {dn}",
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
        "sales_order": dn,
        "total_requested": len(created_requests),
        "payment_requests": created_requests
    }   

#Loan Installments Payment Status

def update_loan_installment_on_payment_entry(doc, method):
    """
    When a Payment Entry is submitted, find its linked Payment Request,
    and update the corresponding row in Loan Installments to mark it as Paid.
    """
    for ref in doc.references:
        if ref.reference_doctype == "Payment Request":
            payment_request_name = ref.reference_name

            # Get Payment Request
            pr = frappe.get_doc("Payment Request", payment_request_name)

            # Safety check: ensure it's linked to Sales Order
            if pr.reference_doctype != "Sales Order" or not pr.reference_name:
                continue

            try:
                # Get Loan Installments for that Sales Order
                loan_doc = frappe.get_doc("Loan Installments", {"sales_order": pr.reference_name})

                # Find the matching row
                for row in loan_doc.installments:
                    if row.payment_request == payment_request_name:
                        row.db_set("paid_status", "Paid")
                        break

            except Exception as e:
                frappe.log_error(frappe.get_traceback(), "Loan Installment Update Error")


#####################################################################################################

@frappe.whitelist(allow_guest=True)
def get_installment_payment_entry(sales_order, amount):
    """
    This function generates a partial payment entry for installments in Sales Order.
    """
    # Temporarily bypass the 'fully billed' validation check
    frappe.flags.ignore_sales_order_billed_validation = True

    try:
        # Create the payment entry based on the Sales Order and payment amount
        pe = original_get_payment_entry(
            dt="Sales Order",
            dn=sales_order,
            party_amount=amount,
            ignore_permissions=True
        )
        # Set custom partial amount
        pe.paid_amount = amount
        pe.received_amount = amount
        pe.references[0].allocated_amount = amount
        return pe
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Installment Payment Entry Error")
        frappe.throw(str(e))

# This is the core method to override the default behavior for payment entry creation.
def patched_get_payment_entry(*args, **kwargs):
    dt = kwargs.get('dt') or args[0]
    dn = kwargs.get('dn') or args[1]

    doc = frappe.get_doc(dt, dn)
    over_billing_allowance = frappe.db.get_single_value("Accounts Settings", "over_billing_allowance")

    # Only override if we explicitly allow (through custom logic)
    if dt == "Sales Order" and frappe.flags.get("ignore_sales_order_billed_validation"):
        # Skip the "fully billed" validation
        pass
    elif dt == "Sales Order" and flt(doc.per_billed, 2) >= (100.0 + flt(over_billing_allowance)):
        frappe.throw(_("Can only make payment against unbilled {0}").format(_(dt)))

    # Proceed to the original method if no custom logic applies
    return original_get_payment_entry(*args, **kwargs)
