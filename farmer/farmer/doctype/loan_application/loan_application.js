frappe.ui.form.on('Loan Application', {

    down_payment_percentage: function(frm) {
        calculate_down_payment(frm);
    },
    total_amount: function(frm) {
        calculate_down_payment(frm);
    },
    status: function(frm) {
        frm.refresh();
    }
});

// Function to calculate down payment and loan amount
function calculate_down_payment(frm) {
    if (frm.doc.total_amount && frm.doc.down_payment_percentage) {
        let down_payment = (frm.doc.total_amount * frm.doc.down_payment_percentage) / 100;
        let loan_amount = frm.doc.total_amount - down_payment;

        frm.set_value('down_payment_amount', down_payment);
        frm.set_value('loan_amount', loan_amount);  // Storing remaining amount in 'loan_amount' field
    }
}

frappe.ui.form.on('Loan Application', {
    loan_amount: function(frm) {
        calculate_total_amount_with_interest(frm);
    },
    interest_rate: function(frm) {
        calculate_total_amount_with_interest(frm);
    },
    repayment_period: function(frm) {
        calculate_total_amount_with_interest(frm);
    },
    compounding_frequency: function(frm) {
        calculate_total_amount_with_interest(frm);
    }
});

function calculate_total_amount_with_interest(frm) {
    if (frm.doc.loan_amount && frm.doc.interest_rate && frm.doc.repayment_period && frm.doc.compounding_frequency) {
        let P = frm.doc.loan_amount;
        let r = frm.doc.interest_rate / 100;  // Convert percentage to decimal
        let t = frm.doc.repayment_period / 12;  // Convert months to years

        // Extract numeric value from the selected compounding frequency
        let n = 12;

        if (n > 0) {
            let A = P * Math.pow(1 + (r / n), n * t);  // Compound Interest Formula
            frm.set_value('total_amount_after_interest', A.toFixed(2));  // Store rounded value
        }
    }
}

frappe.ui.form.on('Loan Application', {
    before_save: function(frm) {
        if (!frm.doc.route) {
            frm.set_value('route', 'loan-application/' + frm.doc.name);
        }

        // Automatically publish
        if (!frm.doc.published) {
            frm.set_value('published', 1);
        }
    },

    validate: function(frm) {
        // Ensure 'remarks' field is filled
        if (!frm.doc.remarks || frm.doc.remarks.trim() === "") {
            frappe.throw(__('Please add remarks for the loan application before saving.'));
        }
        if (!frm.doc.down_payment_percentage) {
            frappe.throw(__('Please enter Down Payment Percentage to proceed.'));
        }
        if (!frm.doc.interest_rate) {
            frappe.throw(__('Please enter Interest Rate to proceed.'));
        }
    }
});


