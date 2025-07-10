frappe.ui.form.on('Technician Task', {
    refresh: function(frm) {
        const user = frappe.session.user;
        const isTechnician = frappe.user_roles.includes("Technician");

        if (frm.doc.status === "Open" && isTechnician) {
            frm.add_custom_button("Start Task", () => {
                frm.set_value("status", "In Progress");
                frm.save();
            });
        }

        if (frm.doc.status === "In Progress" && isTechnician) {
            frm.add_custom_button("Complete", () => {
                frm.set_value("status", "Completed");
                frm.set_value("completion_date", frappe.datetime.get_today());
                frm.save();
            });

            frm.add_custom_button("Escalate", () => {
                frm.set_value("status", "Escalated");
                frm.save();
            });
        }
    }
});
