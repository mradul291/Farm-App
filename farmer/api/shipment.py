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

           
    # def auto_assign_delivery_agent(self):
    #     if self.custom_agent or self.custom_delivery_status == "Assigned to Agent":
    #         return

    #     if not self.delivery_pincode:
    #         return

    #     # Get all active delivery agents
    #     matching_agents = frappe.get_all(
    #         "Delivery Agent",
    #         filters={"status": "Active"},
    #         fields=["name", "service_pincode", "email", "full_name"]
    #     )

    #     selected_agent = None

    #     for agent in matching_agents:
    #         if not agent.service_pincode:
    #             continue

    #         # Split and clean pincode list
    #         pincodes = [p.strip() for p in agent.service_pincode.split(",") if p.strip()]
    #         if self.delivery_pincode in pincodes:
    #             selected_agent = agent
    #             break

    #     if selected_agent:
    #         self.custom_agent = selected_agent.name
    #         self.custom_agent_email = selected_agent.email
    #         self.custom_agent_name = selected_agent.full_name
    #         self.custom_delivery_status = "Assigned to Agent"

    #         if self.flags.in_insert:
    #             frappe.msgprint(f"Auto-assigned Delivery Agent: {selected_agent.full_name}")
    #     else:
    #         if self.flags.in_insert:
    #             frappe.msgprint("No active delivery agent available for this PIN code.")
             
    def auto_assign_delivery_agent(self):
        if self.custom_agent or self.custom_delivery_status == "Assigned to Agent":
            return

        if not self.delivery_pincode:
            return

        all_agents = frappe.get_all(
            "Delivery Agent",
            filters={"status": "Active"},
            fields=["name", "service_pincode", "email", "full_name"]
        )

        suitable_agents = []

        for agent in all_agents:
            if not agent.service_pincode:
                continue

            pincodes = [p.strip() for p in agent.service_pincode.split(",") if p.strip()]
            if self.delivery_pincode in pincodes:
                suitable_agents.append(agent)

        if suitable_agents:
            # Build a list with current assignment counts
            agent_loads = []
            for agent in suitable_agents:
                count = frappe.db.count("Shipment", {
                    "custom_agent": agent.name,
                    "custom_delivery_status": ["in", ["Draft", "In Transit"]]
                })
                agent_loads.append((agent, count))

            # Sort agents by least number of assignments
            agent_loads.sort(key=lambda x: x[1])
            selected_agent = agent_loads[0][0]

            self.custom_agent = selected_agent.name
            self.custom_agent_email = selected_agent.email
            self.custom_agent_name = selected_agent.full_name
            self.custom_delivery_status = "Assigned to Agent"

            if self.flags.in_insert:
                frappe.msgprint(f"Auto-assigned to {selected_agent.full_name} (Least busy agent)")
        else:
            if self.flags.in_insert:
                frappe.msgprint("No active delivery agent found for this PIN code.")
             
                
                