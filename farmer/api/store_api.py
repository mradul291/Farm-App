import frappe
from frappe.utils import get_link_to_form

# ----------------------------------------------------------------------
#  MOVE  (fires via doc_events → on_submit)
# ----------------------------------------------------------------------
def on_submit_store_transfer(doc, method):
    """Auto‑create Material Transfer when Store Transfer is submitted."""
    _validate_fields(doc)

    se = _build_stock_entry(
        source=doc.from_warehouse,
        target=doc.to_warehouse,
        doc=doc
    )

    doc.db_set("stock_entry", se.name)
    doc.db_set("status", "Moved")

    frappe.msgprint(
        f"Stock moved: {get_link_to_form('Stock Entry', se.name)}",
        alert=True, indicator="green"
    )

# ----------------------------------------------------------------------
#  RETURN  (called from client button)
# ----------------------------------------------------------------------
@frappe.whitelist()
def make_return(docname):
    """
    Reverse a Store Transfer and create the return Stock Entry.
    Whitelisted for JS call.
    """
    doc = frappe.get_doc("Store Transfer", docname)

    if doc.status != "Moved":
        frappe.throw("Return is allowed only after the first move.")

    se = _build_stock_entry(
        source=doc.to_warehouse,
        target=doc.from_warehouse,
        doc=doc
    )

    doc.db_set("return_stock_entry", se.name)
    doc.db_set("status", "Returned")

    frappe.msgprint(
        f"Stock returned: {get_link_to_form('Stock Entry', se.name)}",
        alert=True, indicator="blue"
    )
    return se.name

# ----------------------------------------------------------------------
#  Helpers
# ----------------------------------------------------------------------
def _validate_fields(doc):
    if not (doc.item and doc.from_warehouse and doc.to_warehouse and doc.qty):
        frappe.throw("Item, Source, Target and Quantity are mandatory.")

def _build_stock_entry(source, target, doc):
    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = se.purpose = "Material Transfer"
    se.company = frappe.db.get_value("Warehouse", source, "company")
    se.from_warehouse, se.to_warehouse = source, target

    uom = frappe.db.get_value("Item", doc.item, "stock_uom")
    se.append("items", {
        "item_code": doc.item,
        "s_warehouse": source,
        "t_warehouse": target,
        "qty": doc.qty,
        "uom": uom,
        "stock_uom": uom,
        "conversion_factor": 1
    })

    se.insert(ignore_permissions=True)
    se.submit()
    return se
