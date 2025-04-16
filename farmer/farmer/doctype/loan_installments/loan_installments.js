frappe.ui.form.on('Loan Installment Breakdown', {
    paid_status: function(frm, cdt, cdn) {
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
    }
});
