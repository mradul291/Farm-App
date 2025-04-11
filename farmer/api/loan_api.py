import frappe
from frappe import _
from frappe.utils import cint

@frappe.whitelist(allow_guest=True)
def get_payment_url(pr_name):
    pr = frappe.get_doc("Payment Request", pr_name)
    return pr.get_payment_url()

@frappe.whitelist(allow_guest=True)
def make_loan_payment_request(dn, dt="Sales Order", submit_doc=1, order_type="Shopping Cart"):
    ref_doc = frappe.get_doc(dt, dn)

    # Step 2: Find linked Loan Application
    loan_apps = frappe.get_all("Loan Application", filters={"sales_order": dn}, fields=["name", "down_payment_amount"])

    if not loan_apps:
        frappe.throw(_("No Loan Application linked to Sales Order {0}").format(dn))

    loan_app = loan_apps[0]
    down_payment_amount = loan_app.down_payment_amount

    frappe.logger().info(f"[Loan API] Found Loan Application {loan_app.name} for Sales Order {dn} with down_payment_amount {down_payment_amount}")

    if not down_payment_amount or float(down_payment_amount) <= 0:
        frappe.throw(_("Down Payment Amount is not set in the Loan Application {0}").format(loan_app.name))

    # Step 3: Prepare args for Payment Request
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

    # Step 4: Monkey patch amount
    from erpnext.accounts.doctype.payment_request import payment_request
    original_get_amount = payment_request.get_amount

    def get_custom_amount(doc, account=None):
        return down_payment_amount

    payment_request.get_amount = get_custom_amount
    result = payment_request.make_payment_request(**args)
    payment_request.get_amount = original_get_amount

    # Step 5: Clear HTML redirect if set
    if frappe.local.response.get("type") == "redirect":
        del frappe.local.response["type"]
        del frappe.local.response["location"]

    # Step 6: Get payment URL
    payment_url = result.get_payment_url()

    # Step 7: Return combined result
    return {
        "payment_request": result.name,
        "amount": down_payment_amount,
        "payment_url": payment_url
    }

