frappe.ui.form.on("PUE Sponsor", {
    refresh: function (frm) {
        calculate_total_quantity(frm);
        no_of_equipments(frm);
    },
    sponsored_equipments_add: function (frm) {
        calculate_total_quantity(frm);
        no_of_equipments(frm);
    },
    sponsored_equipments_remove: function (frm) {
        calculate_total_quantity(frm);
        no_of_equipments(frm);
    }
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
    },
    quantity: function (frm, cdt, cdn) {
        calculate_row_value_and_total(frm, cdt, cdn);
    }
});

// Function to calculate value for one row and total
function calculate_row_value_and_total(frm, cdt, cdn) {
    const row = locals[cdt][cdn];

    if (!row.equipment || !row.quantity) {
        return;
    }

    // Step 1: Fetch item_code from Website Item
    frappe.call({
        method: 'frappe.client.get',
        args: {
            doctype: "Website Item",
            name: row.equipment
        },
        callback: function (res) {
            if (res.message && res.message.item_code) {
                const item_code = res.message.item_code;

                // Step 2: Fetch price_list_rate from Item Price
                frappe.call({
                    method: 'frappe.client.get_value',
                    args: {
                        doctype: "Item Price",
                        filters: {
                            item_code: item_code
                        },
                        fieldname: "price_list_rate"
                    },
                    callback: function (res2) {
                        if (res2.message && res2.message.price_list_rate) {
                            const rate = parseFloat(res2.message.price_list_rate);
                            const qty = parseFloat(row.quantity || 0);
                            const row_value = rate * qty;

                            // Set a temporary field if you want to show row total (optional)
                            frappe.model.set_value(cdt, cdn, "row_value", row_value);

                            // Step 3: Recalculate total of all rows
                            let total = 0;
                            frm.doc.sponsored_equipments.forEach(function (r) {
                                if (r.equipment && r.quantity) {
                                    total += (r.row_value || 0);
                                }
                            });

                            frm.set_value("total_value", total);
                            frm.refresh_field("total_value");
                        } else {
                            frappe.msgprint(`Price not found for item: ${item_code}`);
                        }
                    }
                });
            } else {
                frappe.msgprint(`Item Code not found in Website Item: ${row.equipment}`);
            }
        }
    });
}
