frappe.ui.form.on('Delivery Agent', {
    refresh(frm) {
        frm.add_custom_button("View Assigned Shipments", () => {
            const route = `/app/shipment?custom_agent=${frm.doc.name}`;
            window.open(route, '_blank');
            });
    }   
});

frappe.ui.form.on('Delivery Agent', {
    refresh(frm) {
        if (frm.doc.__islocal) return;

        frappe.call({
            method: "farmer.api.delivery_api.get_shipments_by_agent",
            args: {
                agent_name: frm.doc.name
            },
            callback: function (r) {
                if (!r.message) return;

                const { draft_shipments, submitted_shipments } = r.message;

                // Clear existing rows
                frm.clear_table("current_assignments");
                frm.clear_table("completed_deliveries");

                // Fill current assignments (draft)
                draft_shipments.forEach(row => {
                    let entry = frm.add_child("current_assignments");
                    entry.shipment = row.name;
                    entry.status = row.status;
                    entry.pickup_date = row.pickup_date;
                });

                // Fill completed deliveries (submitted)
                submitted_shipments.forEach(row => {
                    let entry = frm.add_child("completed_deliveries");
                    entry.shipment = row.name;
                    entry.status = row.status;
                    entry.pickup_date = row.pickup_date;
                });

                frm.refresh_fields();
            }
        });
    }
});
