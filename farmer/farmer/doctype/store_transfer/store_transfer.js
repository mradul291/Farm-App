frappe.ui.form.on('Store Transfer', {
    item(frm) {
        if (frm.doc.item) {
            frappe.call({
                method: "farmer.api.warehouse_api.get_default_warehouse_for_item",
                args: {
                    item: frm.doc.item
                },
                callback(r) {
                    if (r.message) {
                        frm.set_value("from_warehouse", r.message);
                    }
                }
            });
        }
    }
});
