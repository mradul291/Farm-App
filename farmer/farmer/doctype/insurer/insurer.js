frappe.ui.form.on('Insurer', {
    after_save: function(frm) {
        // Only set insurer_id if it's not already set
        if (!frm.doc.insurer_id && frm.doc.name) {
            frm.set_value('insurer_id', frm.doc.name);
            frm.save(); 
        }
    }
});
