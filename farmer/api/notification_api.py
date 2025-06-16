import frappe

def notify_item_owners(doc, method):
    # Loop through all items in the Sales Order
    for row in doc.items:
        # Get item owner
        item = frappe.get_doc("Item", row.item_code)
        item_owner = item.owner
        email = frappe.db.get_value("User", item_owner, "email") or item_owner

        # Skip if no valid email
        if not email or '@' not in email:
            continue

        # Build and send email
        subject = f"Your product {item.item_name} has been ordered"
        message = f"""
            <h3>Product Ordered Notification</h3>
            <p>Dear {frappe.utils.get_fullname(item_owner)},</p>
            <p>Your product <strong>{item.item_name}</strong> was just purchased in Sales Order <strong>{doc.name}</strong>.</p>
            <ul>
                <li>Quantity: {row.qty}</li>
                <li>Ordered By: {doc.customer}</li>
            </ul>
            <p>Thank you for using the platform.</p>
        """

        frappe.sendmail(
            recipients=[email],
            subject=subject,
            message=message
        )

 
# def notify_shipment_update(doc, method):
#     if not doc.delivery_contact_name:
#         return

#     try:
#         contact = frappe.get_doc("Contact", doc.delivery_contact_name)
#         buyer_email = contact.email_id
#     except frappe.DoesNotExistError:
#         return

#     if not buyer_email or "@" not in buyer_email:
#         return

#     subject = f"Shipment Update: {doc.name}"
#     message = f"""
#         <h3>Shipment Status Update</h3>
#         <p>Dear Customer,</p>
#         <p>Your shipment <strong>{doc.name}</strong> is now in status: <strong>{doc.status}</strong>.</p>
#         <ul>
#             <li><strong>Pickup Contact:</strong> {doc.pickup_contact_person}</li>
#             <li><strong>Pickup Date:</strong> {doc.pickup_date}</li>
#             <li><strong>Pickup From:</strong> {doc.pickup_from}</li>
#             <li><strong>Delivery To:</strong> {doc.pickup_to}</li>
#             <li><strong>Goods Value:</strong> {doc.value_of_goods}</li>
#             <li><strong>Description:</strong> {doc.description_of_content}</li>
#         </ul>
#         <p>We’ll keep you posted as your shipment progresses.</p>
#     """

#     frappe.sendmail(
#         recipients=[buyer_email],
#         subject=subject,
#         message=message
#     )


def notify_shipment_delivery(doc, method):
    recipients = []

    # Customer Email from Contact
    if doc.delivery_contact_name:
        try:
            contact = frappe.get_doc("Contact", doc.delivery_contact_name)
            if contact.email_id:
                recipients.append(contact.email_id)
        except frappe.DoesNotExistError:
            pass

    # Vendor Email (assuming this is also a contact)
    if doc.pickup_contact_person:
        try:
            vendor_contact = frappe.get_doc("Contact", doc.pickup_contact_person)
            if vendor_contact.email_id:
                recipients.append(vendor_contact.email_id)
        except frappe.DoesNotExistError:
            pass

    if not recipients:
        return

    subject = f"Shipment {doc.name} Delivered"
    message = f"""
        <h3>Shipment Delivery Confirmation</h3>
        <p>Dear Recipient,</p>
        <p>Shipment <strong>{doc.name}</strong> has been successfully delivered.</p>
        <ul>
            <li><strong>Delivered To:</strong> {doc.delivery_contact_name}</li>
            <li><strong>Pickup Date:</strong> {doc.pickup_date or "N/A"}</li>
        </ul>
        <p>Thank you for using our service.</p>
        <p>Best regards,<br>Farmwarehouse Team</p>
    """

    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=message
    )

    