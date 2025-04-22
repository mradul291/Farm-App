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
    mode_of_payment: function (frm, cdt, cdn) {
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
                callback: function (response) {
                    if (response.message) {
                        frappe.model.sync(response.message);
                        row.paid_status = "Paid";
                        row.payment_date = frappe.datetime.get_today();

                        const installmentAmount = parseFloat(row.installment_amount || 0);
                        const currentTotalLoan = parseFloat(frm.doc.total_loan_amount || 0);
                        const updatedTotal = currentTotalLoan - installmentAmount;

                        frm.set_value('total_loan_amount', Math.round(updatedTotal));
                        frm.refresh_field('installments');
                        frm.refresh_field('total_loan_amount');

                        frm.save().then(() => {
                            frappe.set_route("Form", response.message.doctype, response.message.name);
                        });
                    }
                }
            });
        }
    }
});

// frappe.ui.form.on('Loan Installments', {
//     onload_post_render(frm) {
//         frm.doc.installments.forEach((row, index) => {
//             if (row.payment_request) {
//                 frappe.call({
//                     method: "frappe.client.get_value",
//                     args: {
//                         doctype: "Payment Request",
//                         filters: { name: row.payment_request },
//                         fieldname: "status"
//                     },
//                     callback: function (r) {
//                         if (r.message && r.message.status === "Paid") {
//                             let updated = false;

//                             if (row.paid_status !== "Paid") {
//                                 row.paid_status = "Paid";
//                                 updated = true;
//                             }

//                             if (!row.payment_date) {
//                                 row.payment_date = frappe.datetime.get_today();
//                                 updated = true;
//                             }

//                             frm.fields_dict["installments"].grid.grid_rows_by_docname[row.name]
//                                 .toggle_editable("payment_link", false);

//                             if (updated) {
//                                 frm.refresh_field("installments");

//                                  const amount = parseFloat(row.installment_amount || 0);
//                                  const currentTotal = parseFloat(frm.doc.total_loan_amount || 0);
//                                  const newTotal = currentTotal - amount;
 
//                                  frm.set_value("total_loan_amount", Math.round(newTotal));
//                                  frm.refresh_field('installments');
//                                  frm.refresh_field("total_loan_amount");

//                                  frm.save().then(() => {
//                                     frappe.set_route("Form", frm.doctype, frm.docname);

//                                 });
//                             }
//                         }
//                     }
//                 });
//             }
//         });
//     }
// });


frappe.ui.form.on('Loan Installments', {
    onload_post_render(frm) {
        frm.doc.installments.forEach((row) => {
            if (row.payment_request && row.paid_status !== "Paid") {
                frappe.call({
                    method: "frappe.client.get_value",
                    args: {
                        doctype: "Payment Request",
                        filters: { name: row.payment_request },
                        fieldname: "status"
                    },
                    callback: function (r) {
                        if (r.message && r.message.status === "Paid") {
                            // Update paid status and payment date
                            row.paid_status = "Paid";
                            row.payment_date = frappe.datetime.get_today();

                            // Prevent editing of payment_link
                            frm.fields_dict["installments"].grid.grid_rows_by_docname[row.name]
                                .toggle_editable("payment_link", false);

                            // Perform loan amount calculation like in mode_of_payment
                            const installmentAmount = parseFloat(row.installment_amount || 0);
                            const currentTotalLoan = parseFloat(frm.doc.total_loan_amount || 0);
                            const updatedTotal = currentTotalLoan - installmentAmount;

                            frm.set_value('total_loan_amount', Math.round(updatedTotal));
                            frm.refresh_field('installments');
                            frm.refresh_field('total_loan_amount');

                            // Save and stay on same form
                            frm.save().then(() => {
                                frappe.set_route("Form", frm.doctype, frm.docname);
                            });
                        }
                    }
                });
            }
        });
    }
});
