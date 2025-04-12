import frappe
from frappe import _
from frappe.utils import cint
from erpnext.accounts.doctype.payment_request import payment_request


@frappe.whitelist(allow_guest=True)
def get_payment_url(pr_name):
    pr = frappe.get_doc("Payment Request", pr_name)
    return pr.get_payment_url()

#Down Payment Process 

@frappe.whitelist(allow_guest=True)
def make_loan_payment_request(dn, dt="Sales Order", submit_doc=1, order_type="Shopping Cart"):
    ref_doc = frappe.get_doc(dt, dn)

    # Step 1: Check if Payment Entry already created
    existing_pe = frappe.get_all("Payment Entry", filters={
        "reference_doctype": dt,
        "reference_name": dn,
        "docstatus": 1
    })

    if existing_pe:
        return {
            "error": 1,
            "message": "Payment already completed. Cannot initiate again."
        }

    # Step 2: Check for existing Payment Request
    existing_request = frappe.get_all("Payment Request", filters={
        "reference_name": dn,
        "reference_doctype": dt,
        "docstatus": 1,
        "status": ["in", ["Initiated", "Requested"]]
    }, fields=["name"], order_by="creation desc", limit=1)

    if existing_request:
        existing_doc = frappe.get_doc("Payment Request", existing_request[0].name)
        return {
            "payment_request": existing_doc.name,
            "payment_url": existing_doc.get_payment_url()
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
