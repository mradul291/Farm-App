frappe.ui.form.on("Case", {
    onload: function (frm) {
        frm.set_query("user_type", () => {
            return {
                filters: {
                    name: ["in", ["Farmer Master", "Supplier", "Financier", "Insurer"]],
                },
            };
        });

        if (frm.is_new() && !frm.doc.assigned_by) {
            frm.set_value("assigned_by", frappe.session.user);
        }
    },

    assigned_to: function (frm) {
        if (frm.doc.user_type && frm.doc.assigned_to) {
            let field_to_fetch =
                frm.doc.user_type === "Financier" ? "user"
                : frm.doc.user_type === "Farmer Master" ? "farmer"
                : frm.doc.user_type === "Supplier" ? "supplier"
                : frm.doc.user_type === "Insurer" ? "user"
                : null;

            if (field_to_fetch) {
                frappe.call({
                    method: "frappe.client.get_value",
                    args: {
                        doctype: frm.doc.user_type,
                        filters: { name: frm.doc.assigned_to },
                        fieldname: [field_to_fetch, "owner"]
                    },
                    callback: function (r) {
                        if (r.message) {
                            let user_email = r.message[field_to_fetch] || r.message.owner;
                            frm.set_value("assigned_user_email", user_email);
                        }
                    }
                });
            }
        }
    },
});
