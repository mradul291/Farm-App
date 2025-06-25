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

//Added Button to Make Cash Downpayment
frappe.ui.form.on('Loan Application', {
    refresh(frm) {
        add_cash_down_payment_button(frm);
    },
    onload_post_render(frm) {
        add_cash_down_payment_button(frm);
    }
});

//Added Button to Make Cash Downpayment
function add_cash_down_payment_button(frm) {

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

//Fetching EMI's and Showing on the EMI Tab
frappe.ui.form.on('Loan Application', {
    refresh: function(frm) {
        if (frm.doc.name) {
            fetch_installments_and_populate_emis(frm);
        }
    }
});

//Fetching EMI's and Showing on the EMI Tab
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

//Loan Status Under Review
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


// Admin Loan Creation Flow

//Fetch Repayment and Interest Dynamically on the basis of Tier
frappe.ui.form.on('Loan Application', {
    tier_name(frm) {
        if (!frm.doc.tier_name) return;

        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Tier Master",
                name: frm.doc.tier_name
            },
            callback: function (tierResponse) {
                if (tierResponse && tierResponse.message) {
                    let tierDetails = tierResponse.message.tier_details || [];
                    frm.tier_details_map = tierDetails;

                    // Extract tenure_months as string, remove duplicates
                    let tenureOptions = [...new Set(
                        tierDetails
                            .map(entry => entry.tenure_months)
                            .filter(Boolean)
                            .map(String)
                    )];

                    // Set repayment_period options
                    frm.set_df_property("repayment_period", "options", tenureOptions);
                    frm.refresh_field("repayment_period");
                }
            }
        });
    },

    repayment_period(frm) {
        if (!frm.doc.repayment_period || !frm.tier_details_map) return;

        let selected = frm.doc.repayment_period;

        let matched = frm.tier_details_map.find(entry => String(entry.tenure_months) === String(selected));

        if (matched) {
            frm.set_value("interest_rate", matched.interest_rate || "");
        } else {
            frm.set_value("interest_rate", "");
        }
    }
});

//Fetching Item Price in the Total Amount field
// frappe.ui.form.on('Loan Application', {
//     item_code(frm) {
//         if (!frm.doc.item_code) return;

//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Item Price",
//                 filters: {
//                     item_code: frm.doc.item_code,
//                     selling: 1
//                 },
//                 fields: ["price_list_rate"],
//                 limit_page_length: 1
//             },
//             callback: function (res) {
//                 if (res && res.message && res.message.length > 0) {
//                     const rate = res.message[0].price_list_rate || 0;
//                     frm.set_value("total_amount", rate);
//                     console.log("Fetched Item Price:", rate);
//                 } else {
//                     frm.set_value("total_amount", 0);
//                     console.warn("No price found for item:", frm.doc.item_code);
//                 }
//             }
//         });
//     }
// });
frappe.ui.form.on('Loan Application', {
    item_code(frm) {
        if (!frm.doc.item_code) return;

        frappe.call({
            method: "farmer.api.loan_api.get_discounted_item_price",
            args: {
                item_code: frm.doc.item_code
            },
            callback: function (res) {
                if (res && res.message) {
                    const rate = res.message.discounted_price || 0;
                    frm.set_value("total_amount", rate);
                    console.log("Final Price:", rate, " (Base:", res.message.base_price, ", Discount:", res.message.discount_percent, ")");
                } else {
                    frm.set_value("total_amount", 0);
                    console.warn("No price found.");
                }
            }
        });
    }
});

//Create Sales Order from Loan Application 
frappe.ui.form.on('Loan Application', {
    refresh(frm) {
        create_sales_order_button(frm);
    },
});

// function create_sales_order_button(frm) {
//     if (!frm.doc.sales_order && frm.doc.docstatus < 2) {
//         frm.add_custom_button("Create Sales Order", function () {
//             frappe.model.with_doctype('Sales Order', function () {
//                 const new_so = frappe.model.get_new_doc('Sales Order');

//                 // Set main fields
//                 new_so.naming_series = "SAL-ORD-.YYYY.-";
//                 new_so.customer = frm.doc.applicant || "Guest"; 
//                 new_so.order_type = "Sales";
//                 new_so.company = "Farmwarehouse";
//                 new_so.selling_price_list = "Standard Selling";
//                 new_so.loan_application_ref = frm.doc.name;

//                 // Add item correctly using add_child
//                 const item_row = frappe.model.add_child(new_so, "Sales Order Item", "items");
//                 item_row.item_code = frm.doc.item_code;
//                 item_row.item_name = frm.doc.product_name
//                 item_row.qty = 1;
//                 item_row.rate = frm.doc.total_amount || 0;

//                 // Sync the doc to register child table properly
//                 frappe.model.sync(new_so);

//                 // Route to the Sales Order form
//                 frappe.set_route('Form', 'Sales Order', new_so.name);
//             });
//         });
//     }
// }   
function create_sales_order_button(frm) {
    if (!frm.doc.sales_order && frm.doc.docstatus < 2) {
        frm.add_custom_button("Create Sales Order", function () {
            frappe.call({
                method: "farmer.api.loan_api.get_discounted_item_price",
                args: {
                    item_code: frm.doc.item_code
                },
                callback: function (res) {
                    const discount_info = res.message || {};
                    const rate = discount_info.discounted_price || frm.doc.total_amount || 0;
                    const discount = discount_info.discount_percent || 0;

                    frappe.model.with_doctype('Sales Order', function () {
                        const new_so = frappe.model.get_new_doc('Sales Order');

                        // Set header values
                        new_so.naming_series = "SAL-ORD-.YYYY.-";
                        new_so.customer = frm.doc.applicant || "Guest";
                        new_so.order_type = "Sales";
                        new_so.company = "Farmwarehouse";
                        new_so.selling_price_list = "Standard Selling";
                        new_so.loan_application_ref = frm.doc.name;

                        // Add item row
                        const item_row = frappe.model.add_child(new_so, "Sales Order Item", "items");
                        item_row.item_code = frm.doc.item_code;
                        item_row.item_name = frm.doc.product_name;
                        item_row.qty = 1;
                        item_row.rate = rate;
                        item_row.discount_percentage = discount;

                        // Sync and route
                        frappe.model.sync(new_so);
                        frappe.set_route('Form', 'Sales Order', new_so.name);
                    });
                }
            });
        });
    }
}

frappe.ui.form.on('Loan Application', {
    onload(frm) {
        const dirtyFlag = localStorage.getItem(`mark_dirty_${frm.doc.name}`);
        if (dirtyFlag) {
            localStorage.removeItem(`mark_dirty_${frm.doc.name}`);
            setTimeout(() => {
                frm.dirty();
            }, 300); // delay to ensure form is fully loaded before marking
        }
    }
});

frappe.ui.form.on("Loan Application", {
    onload: function(frm) {
        frm.set_query("item_code", function() {
            return {
                query: "farmer.api.loan_api.get_financing_enabled_items"
            };
        });
    }
});


