import frappe

INSURER_ROLE = "Insurer"

def has_insurer_role(user_doc) -> bool:
    return any(role.role == INSURER_ROLE for role in user_doc.roles)

def map_user_to_insurer_fields(user_doc) -> dict:
    return {
        "user": user_doc.name,
        "contact_phone": user_doc.mobile_no or user_doc.phone or "",
        "insurer_name": user_doc.full_name or user_doc.first_name or user_doc.username,
        "status": "Active",
    }

def create_insurer_from_user(user_doc, method=None):
    if not has_insurer_role(user_doc):
        return

    if frappe.db.exists("Insurer", {"user": user_doc.name}):
        return

    insurer = frappe.new_doc("Insurer")
    insurer.update(map_user_to_insurer_fields(user_doc))
    insurer.insert(ignore_permissions=True)
    frappe.db.commit()

def sync_insurer_from_user(user_doc, method=None):
    if not has_insurer_role(user_doc):
        return

    insurer_name = frappe.db.get_value("Insurer", {"user": user_doc.name})
    if not insurer_name:
        create_insurer_from_user(user_doc)
        return

    insurer = frappe.get_doc("Insurer", insurer_name)
    insurer.update(map_user_to_insurer_fields(user_doc))
    insurer.save(ignore_permissions=True)
    frappe.db.commit()


# Notifications

def send_email(recipients, subject, message):
    """Utility function to send emails."""
    if not recipients:
        return
    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=message
    )

# --- Insurance Enrollment ---
def enrollment_submitted(doc, method):
    """Notify insured user and insurer when enrollment is confirmed."""
    if doc.docstatus != 1:
        return
    subject = f"Insurance Enrollment Confirmed - {doc.name}"
    message = f"""
    Dear User,<br><br>
    Your insurance enrollment <b>{doc.name}</b> has been successfully confirmed.<br>
    Thank you.
    """
    send_email([doc.insured_user, doc.insurer_email], subject, message)

# --- Insurance Claim ---
def claim_status_changed(doc, method):
    """Notify insured user when claim status changes to Approved/Rejected."""
    if not doc.has_value_changed("claim_status"):
        return
    if doc.claim_status in ["Approved", "Rejected"]:
        subject = f"Your Insurance Claim {doc.name} has been {doc.claim_status}"
        message = f"""
        Dear User,<br><br>
        Your claim <b>{doc.name}</b> has been {doc.claim_status.lower()}.
        """
        send_email([doc.insured_user], subject, message)
