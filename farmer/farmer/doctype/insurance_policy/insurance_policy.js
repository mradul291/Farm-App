frappe.ui.form.on('Insurance Policy', {
    after_save: function(frm) {
        if (!frm.doc.policy_id) {
            frm.set_value('policy_id', frm.doc.name);
            frm.save(); 
        }
    }
});
