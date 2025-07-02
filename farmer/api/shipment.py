import frappe
from erpnext.stock.doctype.shipment.shipment import Shipment as ERPNextShipment

class CustomShipment(ERPNextShipment):
    def validate(self):
        super().validate()  # Preserve original validation
        self.set_delivery_pincode()  # Add your custom logic
        self.auto_assign_delivery_agent()

    def set_delivery_pincode(self):
        if self.delivery_address_name and not self.delivery_pincode:
            try:
                address = frappe.get_doc("Address", self.delivery_address_name)
                if address.pincode:
                    self.delivery_pincode = address.pincode
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Shipment.validate → Pincode Fetch Failed")

    def auto_assign_delivery_agent(self):
        if self.custom_agent or self.custom_delivery_status == "Assigned to Agent":
            return  
        
        if not self.delivery_pincode:
            return

        matching_agents = frappe.get_all(
            "Delivery Agent",
            filters={
                "service_pincode": self.delivery_pincode,
                "status": "Active"
            },
            fields=["name"]
        )

        if matching_agents:
            selected_agent = frappe.get_doc("Delivery Agent", matching_agents[0].name)
            
            self.custom_agent = selected_agent.name
            self.custom_agent_email = selected_agent.email
            self.custom_agent_name = selected_agent.full_name
            self.custom_delivery_status = "Assigned to Agent"
            
            if self.flags.in_insert:
                frappe.msgprint(f"Auto-assigned Delivery Agent: {selected_agent.full_name}")
        else:
            if self.flags.in_insert:
                frappe.msgprint("No active delivery agent available for this PIN code.")