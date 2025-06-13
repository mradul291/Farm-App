frappe.ui.form.on("PUE Sponsor", {
    refresh: function (frm) {
        calculate_total_quantity(frm);
        no_of_equipments(frm);
    },
});

frappe.ui.form.on("Sponsored Equipments", {
    quantity: function (frm, cdt, cdn) {
        calculate_total_quantity(frm);
    },
    equipment: function (frm, cdt, cdn) {
        calculate_total_quantity(frm);
        no_of_equipments(frm);
    }
});

// Function to calculate total quantity
function calculate_total_quantity(frm) {
    let total_qty = 0;
    let item_totals = {}; // Store total quantity per equipment

    // Loop through child table and sum up quantity
    frm.doc.sponsored_equipments.forEach(row => {
        total_qty += row.quantity || 0;

        // Sum quantity for each unique item
        if (row.equipment) {
            if (!item_totals[row.equipment]) {
                item_totals[row.equipment] = 0;
            }
            item_totals[row.equipment] += row.quantity || 0;
        }
    });

    // Set the calculated value in the total_quantity field of the main doctype
    frm.set_value("total_quantity", total_qty);

    // Update total_for_item field in each row of the child table
    frm.doc.sponsored_equipments.forEach(row => {
        if (row.equipment) {
            frappe.model.set_value(row.doctype, row.name, "total_for_item", item_totals[row.equipment]);
        }
    });

    frm.refresh_field("sponsored_equipments"); // Refresh the child table to show updated values
}

// Function to calculate the number of unique equipments
function no_of_equipments(frm) {
    let equipments = new Set();

    (frm.doc.sponsored_equipments || []).forEach(row => {
        if (row.equipment) {
            equipments.add(row.equipment);
        }
    });

    frm.set_value('equipments', equipments.size);
    frm.refresh_field('equipments');
    
}

// Client Script (Doctype: PUE Sponsor)
frappe.ui.form.on('Sponsored Equipments Table', {
    equipment: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.equipment) {
            frappe.call({
                method: 'farmer.api.sponsor_api.mark_financing_available',
                args: {
                    website_item: row.equipment
                },
                callback: function (r) {
                    if (r.message && r.message.status === "success") {
                        frappe.msgprint(__('Financing enabled for: ') + row.equipment);
                    }
                }
            });

            // Second: Fetch tier from linked Item via Website Item
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: "Website Item",
                    name: row.equipment
                },
                callback: function (res) {
                    if (res.message && res.message.item_code) {
                        const item_code = res.message.item_code;

                        frappe.call({
                            method: 'frappe.client.get_value',
                            args: {
                                doctype: "Item",
                                filters: {
                                    name: item_code
                                },
                                fieldname: "tier"
                            },
                            callback: function (res2) {
                                if (res2.message && res2.message.tier) {
                                    frappe.model.set_value(cdt, cdn, "tier", res2.message.tier);
                                }
                            }
                        });
                    }
                }
            });
        }
    }
});



frappe.ui.form.on('Sponsored Equipments Table', {
    equipment: function (frm, cdt, cdn) {
        calculate_row_value_and_total(frm, cdt, cdn);
        no_of_equipments(frm);
        
    },
    quantity: function (frm, cdt, cdn) {
        calculate_row_value_and_total(frm, cdt, cdn);
        calculate_total_quantity(frm);
    }
});

// Function to calculate value for one row and total

function calculate_row_value_and_total(frm, cdt, cdn) {
	const row = locals[cdt][cdn];

	if (!row.equipment_name || !row.quantity) return;

	const item_code = row.equipment_name;

	frappe.call({
		method: 'frappe.client.get_value',
		args: {
			doctype: "Item Price",
			filters: { item_code: item_code },
			fieldname: "price_list_rate"
		},
		callback: function (res2) {
			if (!res2.message || !res2.message.price_list_rate) {
				frappe.msgprint(`Price not found for item: ${item_code}`);
				return;
			}

			const rate = parseFloat(res2.message.price_list_rate);
			const qty = parseFloat(row.quantity || 0);
			const row_value = rate * qty;

			frappe.model.set_value(cdt, cdn, "row_value", row_value);

			// Recalculate total after a brief wait
			setTimeout(() => {
				let total = 0;
				let completed = 0;
				const rows = frm.doc.sponsored_equipments || [];

				if (rows.length === 0) {
					frm.set_value("total_value", 0);
					return;
				}

				rows.forEach((r) => {
					if (!r.equipment_name || !r.quantity) {
						completed++;
						if (completed === rows.length) frm.set_value("total_value", total);
						return;
					}

					frappe.call({
						method: 'frappe.client.get_value',
						args: {
							doctype: "Item Price",
							filters: { item_code: r.equipment_name },
							fieldname: "price_list_rate"
						},
						callback: function (res_price) {
							const price = parseFloat(res_price.message?.price_list_rate || 0);
							const qty = parseFloat(r.quantity || 0);
							total += price * qty;

							completed++;
							if (completed === rows.length) {
								frm.set_value("total_value", total);
							}
						}
					});
				});
			}, 200);
		}
	});
}




frappe.ui.form.on('PUE Sponsor', {
    refresh: function(frm) {
        if (frm.is_new()) return;

        // Step 1: Extract item codes from sponsored_equipments
        let itemCodes = [];

        const getItemCodes = frm.doc.sponsored_equipments.map(row => {
            return new Promise(resolve => {
                frappe.db.get_value('Website Item', row.equipment, 'item_code', (r) => {
                    if (r && r.item_code) {
                        itemCodes.push(r.item_code);
                    }
                    resolve();
                });
            });
        });

        // Step 2: After all item_codes are fetched, find Loan Applications
        Promise.all(getItemCodes).then(() => {
            if (!itemCodes.length) return;

            // Clear the existing sponsor_loans table
            frm.clear_table('sponsor_loans');

            // Step 3: Fetch Loan Applications with matching item_code
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Loan Application',
                    filters: [
                        ['item_code', 'in', itemCodes]
                    ],
                    fields: ['name'],
                    limit_page_length: 100
                },
                callback: function(res) {
                    const loans = res.message || [];

                    loans.forEach(loan => {
                        let row = frm.add_child('sponsor_loans');
                        row.loan_id = loan.name;
                    });

                    frm.refresh_field('sponsor_loans');
                }
            });
        });
    }
});
