frappe.ui.form.on('Loan Application', {
    down_payment_percentage: function (frm) {
        calculate_down_payment(frm);
    },
    total_amount: function (frm) {
        calculate_down_payment(frm);
    },
    loan_amount: function (frm) {
        calculate_total_amount_with_interest(frm);
    },
    interest_rate: function (frm) {
        calculate_total_amount_with_interest(frm);
    },
    repayment_period: function (frm) {
        calculate_total_amount_with_interest(frm);
    },
    compounding_frequency: function (frm) {
        calculate_total_amount_with_interest(frm);
    },
    status: function (frm) {
        frm.refresh();
    },

    validate: function (frm) {
        if (!frm.doc.remarks || frm.doc.remarks.trim() === "") {
            frappe.throw(__('Please add remarks for the loan application before saving.'));
        }
        if (!frm.doc.down_payment_percentage) {
            frappe.throw(__('Please enter Down Payment Percentage to proceed.'));
        }
        if (!frm.doc.interest_rate) {
            frappe.throw(__('Please enter Interest Rate to proceed.'));
        }
        if (frm.doc.status === "Approved" && !frm.doc.down_payment_check) {
            frappe.throw(__('Cannot approve the application until Down Payment is done.'));
        }
    },

    before_save: function (frm) {
        if (!frm.doc.route) {
            frm.set_value('route', 'loan-application/' + frm.doc.name);
        }
        if (!frm.doc.published) {
            frm.set_value('published', 1);
        }
    },

    before_workflow_action: function (frm) {
        const action = frm.selected_workflow_action;
        if (action === "Approve" && !frm.doc.down_payment_check) {
            frappe.throw(__('Cannot approve the application until Down Payment is done.'));
        }
    }
});

function calculate_down_payment(frm) {
    if (frm.doc.total_amount && frm.doc.down_payment_percentage) {
        let down_payment = parseInt((frm.doc.total_amount * frm.doc.down_payment_percentage) / 100);
        let loan_amount = frm.doc.total_amount - down_payment;

        frm.set_value('down_payment_amount', down_payment);
        frm.set_value('loan_amount', loan_amount);

        calculate_total_amount_with_interest(frm);
    }
}

function calculate_total_amount_with_interest(frm) {
    if (frm.doc.loan_amount && frm.doc.interest_rate && frm.doc.repayment_period) {
        let P = frm.doc.loan_amount;
        let annual_rate = frm.doc.interest_rate;
        let r = annual_rate / 100 / 12;  // Monthly rate
        let n = frm.doc.repayment_period;

        let emi = (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
        emi = parseFloat(emi.toFixed(2));  // ✅ Round exactly like Python
        let total_emi = emi * n;

        let down_payment = frm.doc.down_payment_amount || 0;
        let total = total_emi + down_payment;

        frm.set_value('total_amount_after_interest', parseInt(total));
    }
}
