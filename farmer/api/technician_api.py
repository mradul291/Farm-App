import frappe

TECHNICIAN_ROLE = "Technician"


def has_technician_role(user_doc) -> bool:
    """Return True only if the saved User has the custom ‘Technician’ role."""
    return any(role.role == TECHNICIAN_ROLE for role in user_doc.roles)


def map_user_to_technician_fields(user_doc) -> dict:
    """Central place to map User → TECHNICIAN field values."""
    return {
        "user": user_doc.name,                       # Link field you just added
        "full_name": user_doc.full_name,
        "email": user_doc.email or user_doc.name,    # fallback to login id
        "contact_number": user_doc.mobile_no or user_doc.phone or "",
        "status": "Active",                          # sensible default
    }


def create_technician_from_user(user_doc, method=None):
    if not has_technician_role(user_doc):
        return

    if frappe.db.exists("Technician", {"user": user_doc.name}):
        # Avoid duplicate profile
        return

    tech = frappe.new_doc("Technician")
    tech.update(map_user_to_technician_fields(user_doc))
    tech.insert(ignore_permissions=True)
    frappe.db.commit()   # ensure record is written before further logic


def sync_technician_from_user(user_doc, method=None):
    if not has_technician_role(user_doc):
        return

    tech_name = frappe.db.get_value("Technician", {"user": user_doc.name})
    if not tech_name:
        # Profile missing (maybe role added later) → create it now
        create_technician_from_user(user_doc)
        return

    tech = frappe.get_doc("Technician", tech_name)
    tech.update(map_user_to_technician_fields(user_doc))
    tech.save(ignore_permissions=True)
    frappe.db.commit()

def send_assignment_email(doc, method=None):
    if not doc.technician_email:
        return

    is_new_doc = not doc.flags.in_insert_after_submit and not doc.flags.in_insert
    email_changed = False

    try:
        previous = doc.get_doc_before_save()
        if previous and previous.technician_email != doc.technician_email:
            email_changed = True
    except Exception:
        previous = None

    # Send on first time assignment (creation with email), or if changed later
    if not previous or email_changed:
        subject = f"New Technician Task Assigned: {doc.name}"
        message = f"""
        Dear Technician,<br><br>

        A new task has been assigned to you.<br><br>

        <b>Task Type:</b> {doc.task_type or 'Not Specified'}<br>
        <b>Scheduled Visit Date:</b> {doc.scheduled_date or 'Not Scheduled'}<br>
        <b>Site:</b> {doc.site or 'Not Provided'}<br>
        <b>Priority:</b> {doc.priority or 'Not Marked'}<br>
        <b>Description:</b> {doc.issue_description or 'N/A'}<br><br>

        Please login to the system to view and update the task.<br><br>

        Regards,<br>
        Support Team
        """

        try:
            frappe.sendmail(
                recipients=[doc.technician_email],
                subject=subject,
                message=message
            )
        except Exception as e:
            frappe.log_error(str(e), "Technician Task Email Sending Failed")

        if frappe.db.exists("User", doc.technician_email):
            try:
                frappe.publish_realtime(
                    event="msgprint",
                    message=f"You have been assigned a new task: {doc.name}",
                    user=doc.technician_email
                )
            except Exception as e:
                frappe.log_error(str(e), "Realtime Notification Failed")
                
        # After sending email, update stats if technician exists
        if doc.assigned_technician:
            update_technician_task_stats(doc.assigned_technician)


def update_technician_task_stats(technician_name):
    if not technician_name:
        return

    # Count current active assignments
    assigned_count = frappe.db.count("Technician Task", {
        "assigned_technician": technician_name,
        "status": ["!=", "Completed"]
    })

    # Count completed tasks
    completed_count = frappe.db.count("Technician Task", {
        "assigned_technician": technician_name,
        "status": "Completed"
    })

    # Update values in Technician Doc
    frappe.db.set_value("Technician", technician_name, {
        "current_assignments": assigned_count,
        "completed_jobs": completed_count
    })
