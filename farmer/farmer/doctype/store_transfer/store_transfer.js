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



frappe.ui.form.on('Store Transfer', {
    refresh(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.status === "Moved") {
            frm.add_custom_button('Return Stock', () => {
                frappe.call({
                    method: 'farmer.api.store_api.make_return',
                    args: { docname: frm.doc.name },
                    callback(r) {
                        if (!r.exc && r.message) {
                            frm.reload_doc();
                            frappe.set_route('Form', 'Stock Entry', r.message);
                        }
                    }
                });
            }).addClass('btn-primary');
        }
    }
});
