frappe.ui.form.on('Store Transfer', {
    item(frm) {
        if (frm.doc.item) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Item Default",
                    filters: {
                        parent: frm.doc.item
                    },
                    fields: ["default_warehouse"],
                    limit_page_length: 1
                },
                callback(r) {
                    if (r.message && r.message.length > 0) {
                        frm.set_value("from_warehouse", r.message[0].default_warehouse);
                    }
                }
            });
        }
    }
});
