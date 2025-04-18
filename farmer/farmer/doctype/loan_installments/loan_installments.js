frappe.ui.form.on('Loan Installment Breakdown', {
    paid_status: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (row.paid_status === "Paid" && !row.payment_date) {
            row.payment_date = frappe.datetime.get_today();
            frm.refresh_field("installments");
        }

        // Optional: Clear payment_date if status is changed back to Pending
        else if (row.paid_status !== "Paid" && row.payment_date) {
            row.payment_date = null;
            frm.refresh_field("installments");
        }
    },
    mode_of_payment: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (row.mode_of_payment === 'Cash') {
            if (!row.payment_request) {
                frappe.msgprint(__('No Payment Request found in this row.'));
                return;
            }

            // Correct call using `docname` to create mapped Payment Entry from Payment Request
            frappe.call({
                method: "erpnext.accounts.doctype.payment_request.payment_request.make_payment_entry",
                args: {
                    docname: row.payment_request
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.model.sync(response.message);
                        frappe.set_route("Form", response.message.doctype, response.message.name);
                    }
                }
            });
        }
    }

});

frappe.ui.form.on('Loan Installments', {
    onload_post_render(frm) {
        // Loop through each installment row
        frm.doc.installments.forEach(row => {
            if (row.payment_request) {
                frappe.call({
                    method: "frappe.client.get_value",
                    args: {
                        doctype: "Payment Request",
                        filters: { name: row.payment_request },
                        fieldname: "status"
                    },
                    callback: function(r) {
                        if (r.message && r.message.status === "Paid" && row.paid_status !== "Paid") {
                            row.paid_status = "Paid";
                            frm.refresh_field("installments");
                        }
                    }
                });
            }
        });
    }
});

