# import frappe
# from frappe.model.document import Document

# class StoreTransfer(Document):

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



import frappe
from frappe.model.document import Document

class StoreTransfer(Document):
    # original move
    def on_submit(self):
        self.create_stock_entry()

    def create_stock_entry(self):
        self._validate_fields()
        se = self._build_stock_entry(
            source=self.from_warehouse,
            target=self.to_warehouse
        )
        self.db_set("stock_entry", se.name)
        self.db_set("status", "Moved")

    # ---------- NEW: reverse transfer ---------- #
    @frappe.whitelist()
    def make_return(docname):
        """Called from the client button to reverse the move"""
        doc = frappe.get_doc("Store Transfer", docname)
        return doc.create_return_stock_entry()

    def create_return_stock_entry(self):
        if self.status != "Moved":
            frappe.throw("Return is allowed only after the first move.")

        se = self._build_stock_entry(
            source=self.to_warehouse,     # swapped
            target=self.from_warehouse    # swapped
        )
        self.db_set("return_stock_entry", se.name)
        self.db_set("status", "Returned")
        frappe.msgprint(f"Return Stock Entry <b>{se.name}</b> created.")
        return se.name                   # lets JS open it

    # ---------- helpers ---------- #
    def _validate_fields(self):
        if not (self.item and self.from_warehouse and self.to_warehouse and self.qty):
            frappe.throw("Item, Source, Target and Quantity are mandatory.")

    def _build_stock_entry(self, source, target):
        se = frappe.new_doc("Stock Entry")
        se.stock_entry_type = "Material Transfer"
        se.purpose = "Material Transfer"
        se.company = frappe.db.get_value("Warehouse", source, "company")
        se.from_warehouse = source
        se.to_warehouse = target
        uom = frappe.db.get_value("Item", self.item, "stock_uom")

        se.append("items", {
            "item_code": self.item,
            "s_warehouse": source,
            "t_warehouse": target,
            "qty": self.qty,
            "uom": uom,
            "stock_uom": uom,
            "conversion_factor": 1
        })

        se.insert(ignore_permissions=True)
        se.submit()
        return se
