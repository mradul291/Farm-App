frappe.ui.form.on('Farmer Master', {
    refresh: function(frm) {
        console.log("Farmer Master Form Refreshed...");
        
        // Fetch Website Items for the Farmer
        if (frm.doc.farmer) {
            console.log("Fetching Website Items for farmer:", frm.doc.farmer);
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Website Item",
                    filters: { owner: frm.doc.farmer },
                    fields: ["name", "item_name"]
                },
                callback: function(response) {
                    console.log("Website Items Response:", response);

                    if (response.message && response.message.length > 0) {
                        frm.clear_table("product_section");

                        response.message.forEach(item => {
                            let row = frm.add_child("product_section");
                            row.product_id = item.name;
                            row.product_name = item.item_name;
                        });

                        frm.refresh_field("product_section");
                        console.log("Product Section Updated Successfully.");
                    } else {
                        console.log("No Website Items found for this farmer.");
                    }
                },
                error: function(error) {
                    console.error("Error fetching Website Items:", error);
                }
            });
        } else {
            console.warn("No farmer email found in the 'farmer' field.");
        }
    }
});


frappe.ui.form.on('Farmer Master', {
    refresh: function(frm) {
        if (frm.is_new()) return;

        // Get farmer email from linked User
        frappe.db.get_value('User', frm.doc.farmer, 'email', (r) => {
            if (!r || !r.email) return;

            const farmer_email = r.email;

            // Clear existing loan_table
            frm.clear_table('loan_table');

            // Fetch loan applications owned by this email
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Loan Application',
                    filters: {
                        owner: farmer_email
                    },
                    fields: ['name', 'status', 'creation'], // Add more fields as needed
                    limit_page_length: 100
                },
                callback: function(res) {
                    const loans = res.message || [];

                    loans.forEach(loan => {
                        let row = frm.add_child('loan_table');
                        row.loan_id = loan.name;
                        row.status = loan.status;
                        row.date = frappe.datetime.str_to_obj(loan.creation);
                    });

                    frm.refresh_field('loan_table');
                }
            });
        });
    }
});

frappe.ui.form.on('Farmer Master', {
    refresh: function(frm) {
        if (frm.is_new()) return;

        // Step 1: Get farmer email from linked User
        frappe.db.get_value('User', frm.doc.farmer, 'email', (r) => {
            if (!r || !r.email) return;

            const farmer_email = r.email;

            // Step 2: Clear existing order table
            frm.clear_table('farmer_order');

            // Step 3: Fetch Sales Orders owned by the same farmer email
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Sales Order',
                    filters: {
                        owner: farmer_email  // You can also add `farmer: frm.doc.name` if field exists
                    },
                    fields: ['name'],  // Add more if needed
                    limit_page_length: 100
                },
                callback: function(res) {
                    const orders = res.message || [];

                    orders.forEach(order => {
                        let row = frm.add_child('farmer_order');
                        row.order_id = order.name;
                    });

                    frm.refresh_field('farmer_order');
                }
            });
        });
    }
});
