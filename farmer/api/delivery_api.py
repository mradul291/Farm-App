from frappe.utils import now_datetime
import frappe
from frappe.utils import now


@frappe.whitelist()
def get_shipments_by_agent(agent_name):
    if not agent_name:
        return {}

    # Draft Shipments
    draft = frappe.get_all(
        "Shipment",
        filters={
            "custom_agent": agent_name,
            "docstatus": 0
        },
        fields=["name", "status", "pickup_date"]
    )

    # Submitted Shipments
    submitted = frappe.get_all(
        "Shipment",
        filters={
            "custom_agent": agent_name,
            "docstatus": 1
        },
        fields=["name", "status", "pickup_date"]
    )

    return {
        "draft_shipments": draft,
        "submitted_shipments": submitted
    }

def before_submit(self, method):
    if self.custom_delivery_status != "In Transit":
        frappe.throw("Shipment must be picked up before submission.")
    
    if not self.custom_proof_of_delivery:
        frappe. throw("Proof of Delivery is required.")

    if not self.pickup_to:
        self.pickup_to = now_datetime()

    self.custom_delivery_status = "Delivered"


def on_submit(self):
    recipients = []

    if self.delivery_contact_email:
        recipients.append(self.delivery_contact_email)
    if self.pickup_contact_person:
        recipients.append(self.pickup_contact_person)

    if recipients:
        frappe.sendmail(
            recipients=recipients,
            subject=f"Shipment {self.name} Delivered",
            message="Your order has been successfully delivered. Thank you for choosing our service."
        )


def notify_agent_on_assignment(doc, method):
    if not doc.custom_agent_email:
        return

    subject = f"Order Assigned - Shipment {doc.name}"
    message = f"""
    Dear Delivery Agent,<br><br>
    You have been assigned a new shipment.<br><br>
    <b>Shipment ID:</b> {doc.name}<br>
    <b>Status:</b> {doc.custom_delivery_status}<br><br>
    Please check your dashboard for further details.<br><br>
    Regards,<br>
    Logistics Team
    """

    frappe.sendmail(
        recipients=[doc.custom_agent_email],
        subject=subject,
        message=message
    )