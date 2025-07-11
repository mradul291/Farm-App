# import frappe
from frappe.model.document import Document

class StoreTransfer(Document):
    pass

#     def on_submit(self):
#         self.create_stock_entry()

#     def create_stock_entry(self):
#         if not (self.item and self.from_warehouse and self.to_warehouse and self.qty):
#             frappe.throw("All fields (Item, Source Warehouse, Target Warehouse, Quantity) are required.")

#         stock_entry = frappe.new_doc("Stock Entry")
#         stock_entry.stock_entry_type = "Material Transfer"
#         stock_entry.purpose = "Material Transfer"
#         stock_entry.company = frappe.db.get_value("Warehouse", self.from_warehouse, "company")  # Assumes both warehouses belong to same company
#         stock_entry.from_warehouse = self.from_warehouse
#         stock_entry.to_warehouse = self.to_warehouse

#         stock_entry.append("items", {
#             "item_code": self.item,
#             "s_warehouse": self.from_warehouse,
#             "t_warehouse": self.to_warehouse,
#             "qty": self.qty,
#             "uom": frappe.db.get_value("Item", self.item, "stock_uom"),
#             "stock_uom": frappe.db.get_value("Item", self.item, "stock_uom"),
#             "conversion_factor": 1.0
#         })

#         stock_entry.insert(ignore_permissions=True)
#         stock_entry.submit()

#         self.db_set("stock_entry", stock_entry.name)
#         self.db_set("status", "Moved")

#         frappe.msgprint(f"Stock Entry <b>{stock_entry.name}</b> created and submitted successfully.")



