frappe.ui.form.on('Insurance Product', {
    before_save: function(frm) {
        if (!frm.doc.insurer) {
            frm.set_value('insurer', frappe.session.user);
        }
    }
});
