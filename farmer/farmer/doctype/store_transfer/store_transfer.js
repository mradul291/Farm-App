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
                    method: 'farmer.api.store_api.make_return',   // keep your path
                    args: { docname: frm.doc.name },
                    freeze: true,                                 // spinner while processing
                    callback(r) {
                        if (!r.exc) {
                            frm.reload_doc();                     // update status to "Returned"
                            // Success toast for user feedback
                            frappe.show_alert({
                                message: __('Stock successfully returned.'),
                                indicator: 'green'
                            }, 5);                                // visible for 5 seconds
                        }
                    }
                });
            }).addClass('btn-primary');
        }
    }
});

