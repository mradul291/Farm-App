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

    onload: function (frm) {
        // Trigger calculations based on initial data available in the fields
        if (frm.doc.loan_amount && frm.doc.down_payment_percentage) {
            calculate_down_payment(frm);
        }
        if (frm.doc.loan_amount && frm.doc.interest_rate && frm.doc.repayment_period) {
            calculate_total_amount_with_interest(frm);
        }
    },

    refresh: function (frm) {
        if (!frm.doc.__islocal) {
            // If the document is not new, trigger calculations
            if (frm.doc.loan_amount && frm.doc.interest_rate && frm.doc.repayment_period) {
                calculate_total_amount_with_interest(frm);
            }
            if (frm.doc.down_payment_percentage) {
                calculate_down_payment(frm);
            }
        }
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
            frappe.throw(__('Please refresh the page and try again.'));
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
        let r = annual_rate / 100 / 12;
        let n = frm.doc.repayment_period;

        let emi = (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
        emi = Math.round(emi);
        let total_emi = emi * n;

        let down_payment = frm.doc.down_payment_amount || 0;
        let total = total_emi + down_payment;

        frm.set_value('total_amount_after_interest', parseInt(total));
    }
}


frappe.ui.form.on('Loan Application', {
    refresh: function (frm) {
        if (frm.doc.tier_name) {
            fetch_and_set_tier_details(frm);
        }
    },
    repayment_period: function (frm) {
        update_interest_rate(frm);
    }
});

// Function to fetch Tier Details and set Repayment Period options
function fetch_and_set_tier_details(frm) {
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Tier Master",
            name: frm.doc.tier_name
        },
        callback: function (tierResponse) {
            if (tierResponse && tierResponse.message) {
                let tierMaster = tierResponse.message;
                let tierDetails = tierMaster.tier_details || [];

                console.log("Fetched Tier Details (Child Table):", tierDetails);

                frm.doc._tier_details = tierDetails; // temporarily store for later use

                // Prepare Repayment Period options
                let tenureOptions = tierDetails
                    .map(entry => entry.tenure_months)
                    .filter(months => months)
                    .map(String);

                tenureOptions = [...new Set(tenureOptions)]; // remove duplicates

                console.log("Setting Repayment Period Options:", tenureOptions);

                frm.set_df_property("repayment_period", "options", tenureOptions);
                frm.refresh_field("repayment_period");
            }
        }
    });
}

// Function to update Interest Rate based on selected Repayment Period
function update_interest_rate(frm) {
    if (frm.doc.repayment_period && frm.doc._tier_details) {
        let selectedTenure = frm.doc.repayment_period;

        // Find matching record
        let match = frm.doc._tier_details.find(entry =>
            String(entry.tenure_months) === String(selectedTenure)
        );

        if (match) {
            frm.set_value("interest_rate", match.interest_rate || 0);
        } else {
            frm.set_value("interest_rate", 0);
        }
    }
}

frappe.ui.form.on('Loan Application', {
    refresh(frm) {
        add_cash_down_payment_button(frm);
    },
    onload_post_render(frm) {
        add_cash_down_payment_button(frm);
    }
});

function add_cash_down_payment_button(frm) {
    frm.clear_custom_buttons();

    if(frm.doc.down_payment_check || frm.doc.status === "Rejected" ){
        return;
    }

    frm.add_custom_button('Cash Down Payment', async function () {

        // Ensure Sales Invoice is linked
        if (!frm.doc.sales_invoice) {
            frappe.msgprint(__('Please select a Sales Invoice before proceeding.'));
            return;
        }

        try {
            frappe.call({
                method: "farmer.api.loan_api.make_loan_payment_request",
                args: {
                    dn: frm.doc.sales_invoice,
                    dt: "Sales Invoice",
                    submit_doc: 1,
                    order_type: "Shopping Cart"
                },
                callback(r) {
                    if (r.message?.payment_request) {
                        // Proceed to create payment entry
                        frappe.call({
                            method: "erpnext.accounts.doctype.payment_request.payment_request.make_payment_entry",
                            args: {
                                docname: r.message.payment_request
                            },
                            callback: function (res) {
                                if (res.message) {
                                    // Sync the Payment Entry
                                    frappe.model.sync(res.message);

                                    // Set mode_of_payment to "Cash" (only if the doc is not submitted)
                                    if (res.message.docstatus === 0) {
                                        frappe.model.set_value(res.message.doctype, res.message.name, "mode_of_payment", "Cash");
                                    }

                                    // Redirect to the Payment Entry form
                                    frappe.set_route("Form", res.message.doctype, res.message.name);

                                    // Update the Loan Application field as Cash and refresh the button
                                    frm.set_value("mode_of_down_payment", "Cash");
                                    frm.save().then(() => {
                                        add_cash_down_payment_button(frm);  // Optional: your custom function to re-render the button
                                    });
                                }
                            }

                        });
                    } else if (r.message?.error) {
                        frappe.msgprint(__(r.message.message));
                    }
                }
            });

        } catch (err) {
            frappe.msgprint(__('An error occurred while saving the form.'));
        }
    });
}



//Test 

frappe.ui.form.on('Loan Application', {
    refresh: function(frm) {
        if (frm.doc.name) {
            fetch_installments_and_populate_emis(frm);
        }
    }
});

async function fetch_installments_and_populate_emis(frm) {
    // Clear existing EMI rows
    frm.clear_table('emis');

    try {
        const result = await frappe.db.get_list('Loan Installments', {
            filters: {
                applicant: frm.doc.name
            },
            fields: ['name']
        });

        if (result.length === 0) {
            return;
        }

        // Assuming one-to-one relationship (fetching first match)
        const installment_doc = await frappe.db.get_doc('Loan Installments', result[0].name);

        if (installment_doc.installments && installment_doc.installments.length > 0) {
            installment_doc.installments.forEach(installment => {
                const row = frm.add_child('emis');
                row.installment_id     = installment.installment_id;
                row.installment_number = installment.installment_number;
                row.due_date           = installment.due_date;
                row.installment_amount = installment.installment_amount;
                row.principal_amount   = installment.principal_amount;
                row.interest_amount    = installment.interest_amount;
                row.paid_status        = installment.paid_status;
                row.payment_date       = installment.payment_date;
                row.payment_link       = installment.payment_link;
                row.payment_request    = installment.payment_request;
                row.mode_of_payment    = installment.mode_of_payment;
            });

            frm.refresh_field('emis');
        }
    } catch (error) {
        console.error(error);
    }
}


frappe.ui.form.on('Loan Application', {
    before_save: function(frm) {
        if (
            frm.doc.status === 'Under Review' &&
            frm.doc.remarks &&
            frm.doc.remarks.trim() !== ''
        ) {
            frm.set_value('status', 'Make Down Payment');
        }
    }
});
