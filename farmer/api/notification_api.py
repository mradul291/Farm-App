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

#Not Required
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




    